import Foundation
@testable import App
import Testing
import OmFileFormat

@Suite struct IconHhlTests {
    /// Verifies `readColumnFromStaticFile` against the exact layout `convertHhlHeights` writes:
    /// a 3D `[ny, nx, nlev]` file with the level dimension last, stacked as
    /// `index = (y*nx + x) * nlev + lev`. The column read at a grid point must return all
    /// `nlev` values for that point in level order (top..surface), proving the indexing,
    /// gridpoint→(x,y) mapping and the single-I/O range read.
    @Test func readColumnFromStatic3D() async throws {
        let ny = 2, nx = 3, nlev = 4
        // value(y,x,lev) = lev*1000 + (y*nx + x)  → uniquely identifies level and location
        var data = [Float](repeating: .nan, count: ny * nx * nlev)
        for y in 0..<ny {
            for x in 0..<nx {
                let sp = y * nx + x
                for lev in 0..<nlev {
                    data[sp * nlev + lev] = Float(lev * 1000 + sp)
                }
            }
        }

        let file = "test_hhl_3d.om"
        try FileManager.default.removeItemIfExists(at: file)
        defer { try? FileManager.default.removeItem(atPath: file) }
        try data.writeOmFile(file: file, dimensions: [ny, nx, nlev], chunks: [ny, nx, nlev], compression: .pfor_delta2d, scalefactor: 1)

        let reader = try await OmFileReader(file: file).expectArray(of: Float.self)
        let grid = RegularGrid(nx: nx, ny: ny, latMin: 0, lonMin: 0, dx: 1, dy: 1)

        // grid point (y=1, x=1) → gridpoint 4 → expected [4, 1004, 2004, 3004]
        let column = try await grid.readColumnFromStaticFile(gridpoint: 4, file: reader)
        #expect(column == [4, 1004, 2004, 3004])

        // corner (y=0, x=0) → gridpoint 0 → [0, 1000, 2000, 3000]
        let corner = try await grid.readColumnFromStaticFile(gridpoint: 0, file: reader)
        #expect(corner == [0, 1000, 2000, 3000])

        // last point (y=1, x=2) → gridpoint 5 → [5, 1005, 2005, 3005]
        let last = try await grid.readColumnFromStaticFile(gridpoint: 5, file: reader)
        #expect(last == [5, 1005, 2005, 3005])
    }

    /// Full-level height = mean of the two enclosing half levels (PDF formula).
    /// Pure-arithmetic guard so the derivation contract stays explicit independent of the reader.
    @Test func fullLevelIsMeanOfHalves() {
        let halfAsl: [Float] = [22000, 19402, 18013, 531]   // top..surface
        func fullAsl(_ fullLevel: Int) -> Float { (halfAsl[fullLevel - 1] + halfAsl[fullLevel]) / 2 }
        #expect(fullAsl(1) == (22000 + 19402) / 2)
        #expect(fullAsl(3) == (18013 + 531) / 2)
    }

    /// `hires-temp` is the unified model-level profile: every full level 1…N (top..surface)
    /// carrying exactly the five full-level variables, plus vertical wind W on every half
    /// level 1…N+1. Locks in the FL180-split removal.
    @Test func hiresTempCoversAllLevels() {
        let expectedFullVars: Set<IconModelLevelVariableType> = [
            .wind_u_component, .wind_v_component, .temperature, .specific_humidity, .pressure
        ]
        for domain in [IconDomains.iconD2, .iconEu, .icon] {
            let n = domain.numberOfModelFullLevels
            let nHalf = domain.numberOfModelHalfLevels
            let vars = DownloadIconCommand.VariableGroup.hiresTemp.variables(domain: domain)
            let levelVars = vars.compactMap { $0 as? IconModelLevelVariable }
            // every selected variable is a model-level variable (no surface/pressure leakage)
            #expect(levelVars.count == vars.count)
            #expect(levelVars.count == n * expectedFullVars.count + nHalf)
            let fullVars = levelVars.filter { !$0.variable.isHalfLevel }
            let halfVars = levelVars.filter { $0.variable.isHalfLevel }
            #expect(Set(fullVars.map { $0.level }) == Set(1...n))
            for level in 1...n {
                #expect(Set(fullVars.filter { $0.level == level }.map { $0.variable }) == expectedFullVars)
            }
            // W: exactly one per half level 1…N+1
            #expect(halfVars.allSatisfy { $0.variable == .wind_w })
            #expect(halfVars.map { $0.level }.sorted() == Array(1...nHalf))
        }
    }

    /// `modelLevel` must keep its *upstream* meaning: surface variables flagged `cat == "model-level"`,
    /// NOT the hires profile stack. Regression guard for the merge-back-upstream constraint.
    @Test func modelLevelKeepsUpstreamSemantics() {
        for domain in [IconDomains.iconD2, .iconEu, .icon] {
            let vars = DownloadIconCommand.VariableGroup.modelLevel.variables(domain: domain)
            // not a single IconModelLevelVariable — these are surface vars
            #expect(vars.allSatisfy { ($0 as? IconModelLevelVariable) == nil })
            #expect(vars.allSatisfy { ($0 as? IconSurfaceVariable)?.getVarAndLevel(domain: domain)?.cat == "model-level" })
            // and it is exactly the surface model-level filter
            let expected = IconSurfaceVariable.allCases.filter { $0.getVarAndLevel(domain: domain)?.cat == "model-level" }
            #expect(vars.count == expected.count)
        }
    }

    /// `heidiVars` is the curated 2D surface set: pure single-level surface variables, no model-level
    /// or pressure-level leakage, and a single domain-independent list. Variables DWD does not publish
    /// for a given domain are not filtered out of the list — they are skipped at download time by
    /// `getVarAndLevel` returning nil, which is what keeps Curl from retry-looping on 404s.
    @Test func heidiVarsIsCuratedSurfaceSet() {
        let expected: Set<IconSurfaceVariable> = [
            .wind_gusts_10m, .wind_u_component_10m, .wind_v_component_10m,
            .visibility, .pressure_msl, .weather_code,
            .precipitation, .rain, .showers,
            .snowfall_water_equivalent, .snowfall_convective_water_equivalent, .snowfall_height,
            .temperature_2m, .relative_humidity_2m,
            .cloud_cover, .cloud_cover_low, .cloud_cover_mid, .cloud_cover_high,
            .cloud_base, .freezing_level_height,
            .cape, .convective_inhibition, .lightning_potential,
            .convective_cloud_base, .convective_cloud_top
        ]
        for domain in [IconDomains.iconD2, .iconEu, .icon] {
            let vars = DownloadIconCommand.VariableGroup.heidiVars.variables(domain: domain)
            let surface = vars.compactMap { $0 as? IconSurfaceVariable }
            #expect(surface.count == vars.count)
            #expect(Set(surface) == expected)
            #expect(surface.count == expected.count) // no duplicates
            // never a model-level or pressure-level request
            #expect(surface.allSatisfy { ($0.getVarAndLevel(domain: domain)?.cat ?? "single-level") == "single-level" })
        }

        // CEILING is only published for icon-eu and icon-d2, mapped to the open-meteo `cloud_base` name
        #expect(IconSurfaceVariable.cloud_base.getVarAndLevel(domain: .iconD2)?.variable == "ceiling")
        #expect(IconSurfaceVariable.cloud_base.getVarAndLevel(domain: .iconEu)?.variable == "ceiling")
        #expect(IconSurfaceVariable.cloud_base.getVarAndLevel(domain: .iconD2)?.cat == "single-level")
        #expect(IconSurfaceVariable.cloud_base.getVarAndLevel(domain: .icon) == nil)

        // The group is shared, but what is actually downloadable shrinks on the coarser domains.
        func downloadable(_ domain: IconDomains) -> Int {
            DownloadIconCommand.VariableGroup.heidiVars.variables(domain: domain)
                .filter { $0.getVarAndLevel(domain: domain) != nil }.count
        }
        // global publishes neither ceiling, cin_ml, snowlmt, vis nor lpi
        let notInGlobal: [IconSurfaceVariable] = [.cloud_base, .convective_inhibition, .snowfall_height, .visibility, .lightning_potential]
        #expect(notInGlobal.allSatisfy { $0.getVarAndLevel(domain: .icon) == nil })
        #expect(downloadable(.icon) == expected.count - notInGlobal.count) // 20
        // icon-eu has everything except lpi, which is icon-d2 only
        #expect(IconSurfaceVariable.lightning_potential.getVarAndLevel(domain: .iconEu) == nil)
        #expect(downloadable(.iconEu) == expected.count - 1) // 24
        #expect(downloadable(.iconD2) == expected.count)     // 25
    }

    /// HHL column cache is a reference type: a stored column is shared across value copies of the reader,
    /// so the static `hhl.om` is read once, not per height/RH/dew-point query.
    @Test func hhlColumnCacheMemoisesByReference() {
        let cache = HhlColumnCache()
        #expect(cache.column == nil)
        cache.column = [1, 2, 3]
        let copy = cache                 // reference semantics
        copy.column = [9, 8]
        #expect(cache.column == [9, 8])  // shared mutation visible through the original
    }

    /// Missing `hhl.om` surfaces a descriptive error (model-level heights) instead of silent NaN.
    @Test func hhlMissingFileErrorIsDescriptive() {
        let msg = "\(IconHhlError.staticFileMissing(domain: "dwd_icon"))"
        #expect(msg.contains("hhl.om"))
        #expect(msg.contains("dwd_icon"))
    }

    /// Out-of-range model level surfaces a descriptive error (valid range stated) instead of silent NaN.
    @Test func modelLevelOutOfRangeErrorIsDescriptive() {
        let msg = "\(IconModelLevelError.levelOutOfRange(level: 200, max: 65, domain: "dwd_icon_d2"))"
        #expect(msg.contains("200"))
        #expect(msg.contains("1...65"))
        #expect(msg.contains("dwd_icon_d2"))
    }

    /// Model-level specific humidity is stored logarithmically (constant relative precision over its
    /// 4–5-order range); other model-level vars keep the default int16. Checked through the
    /// `any GenericVariable` existential the write/convert sinks actually use (dynamic dispatch).
    @Test func specificHumidityUsesLogarithmicCompression() {
        let qv: any GenericVariable = IconModelLevelVariable(variable: .specific_humidity, level: 60)
        let t:  any GenericVariable = IconModelLevelVariable(variable: .temperature, level: 60)
        #expect(qv.omFileCompression == .pfor_delta2d_int16_logarithmic)
        #expect(qv.scalefactor == 10000)
        #expect(t.omFileCompression == .pfor_delta2d_int16)
        // default for an unrelated variable
        #expect((IconSurfaceVariable.temperature_2m as any GenericVariable).omFileCompression == .pfor_delta2d_int16)
    }

    /// Round-trip proof of the qv storage fix. The key win: a near-zero stratospheric qv stays
    /// **non-zero** (linear int16 × 1000 rounds 0.0004 g/kg to 0 → dew point becomes NaN aloft).
    /// `log10(1+x)` is near-linear for x≪1, so relative precision is excellent in the mid-level dry
    /// range (qv ≳ 0.05 g/kg, the Stiwoll concern) and degrades gracefully — without truncating — below.
    @Test func logarithmicCompressionPreservesDryLayerQv() async throws {
        let values: [Float] = [0.0004, 0.05, 0.5, 5.0, 25.0]   // g/kg: stratosphere → moist surface
        let file = "test_qv_log.om"
        try FileManager.default.removeItemIfExists(at: file)
        defer { try? FileManager.default.removeItem(atPath: file) }
        try values.writeOmFile(file: file, dimensions: [values.count], chunks: [values.count],
                               compression: .pfor_delta2d_int16_logarithmic, scalefactor: 10000)
        let reader = try await OmFileReader(file: file).expectArray(of: Float.self)
        let back = try await reader.read()
        #expect(back[0] > 0)                      // no truncation to zero (the bug)
        #expect(abs(back[0] - 0.0004) < 3e-4)     // within one log-quantisation step near zero
        for (a, b) in zip(values, back) where a >= 0.05 {
            #expect(abs(a - b) / a < 0.01)        // <1% relative through the meaningful range
        }
    }
}
