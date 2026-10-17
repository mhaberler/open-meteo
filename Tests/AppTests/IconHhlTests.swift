import Foundation
@testable import App
import Testing
import OmFileFormat

@Suite struct IconHhlTests {
    /// `readColumnFromStaticFile` matches the layout `convertHhlHeights` writes:
    /// `[ny, nx, nlev]`, level last, `index = (y*nx + x) * nlev + lev`.
    /// Native ICON grids are `ny = 1`.
    @Test func readColumnFromStatic3D() async throws {
        let ny = 1, nx = 5, nlev = 4
        var data = [Float](repeating: .nan, count: ny * nx * nlev)
        for y in 0..<ny {
            for x in 0..<nx {
                let sp = y * nx + x
                for lev in 0..<nlev {
                    data[sp * nlev + lev] = Float(lev * 1000 + sp)
                }
            }
        }

        let file = FileManager.default.temporaryDirectory.appendingPathComponent("test_hhl_native.om").path
        try FileManager.default.removeItemIfExists(at: file)
        defer { try? FileManager.default.removeItem(atPath: file) }
        try data.writeOmFile(file: file, dimensions: [ny, nx, nlev], chunks: [ny, nx, nlev], compression: .pfor_delta2d, scalefactor: 1)

        let reader = try await OmFileReader(file: file).expectArray(of: Float.self)
        let grid = RegularGrid(nx: nx, ny: ny, latMin: 0, lonMin: 0, dx: 1, dy: 1)

        let column = try await grid.readColumnFromStaticFile(gridpoint: 3, file: reader)
        #expect(column == [3, 1003, 2003, 3003])
        let corner = try await grid.readColumnFromStaticFile(gridpoint: 0, file: reader)
        #expect(corner == [0, 1000, 2000, 3000])
        let last = try await grid.readColumnFromStaticFile(gridpoint: 4, file: reader)
        #expect(last == [4, 1004, 2004, 3004])
    }

    /// Full-level height is the mean of the enclosing half levels.
    @Test func fullLevelIsMeanOfHalves() {
        let halfAsl: [Float] = [22000, 19402, 18013, 531]
        func fullAsl(_ fullLevel: Int) -> Float { (halfAsl[fullLevel - 1] + halfAsl[fullLevel]) / 2 }
        #expect(fullAsl(1) == (22000 + 19402) / 2)
        #expect(fullAsl(3) == (18013 + 531) / 2)
    }

    @Test func levelNamesRoundTrip() {
        let column = ForecastHeightVariable(rawValue: "temperature_level65")
        #expect(column?.modelLevel == true)
        #expect(column?.rawValue == "temperature_level65")
        let fixed = ForecastHeightVariable(rawValue: "temperature_80m")
        #expect(fixed?.modelLevel == false)
        #expect(fixed?.rawValue == "temperature_80m")
        #expect(ForecastVariable(rawValue: "wind_w_level66")?.rawValue == "wind_w_level66")
    }

    /// `hiresTemp` is the full column. `modelLevel` stays the 80/120/180 m surface fields.
    @Test func hiresTempCoversAllLevels() {
        let expectedFullVars: Set<IconModelLevelVariableType> = [
            .wind_u_component, .wind_v_component, .temperature, .specific_humidity, .pressure,
            .cloud_water, .cloud_ice, .cloud_cover
        ]
        for domain in [IconDownloadDomains.iconD2, .iconEu, .icon] {
            let n = domain.numberOfModelFullLevels
            let nHalf = domain.numberOfModelHalfLevels
            let vars = DownloadIconCommand.VariableGroup.hiresTemp.variables(domain: domain)
            let levelVars = vars.compactMap { $0 as? IconModelLevelVariable }
            #expect(levelVars.count == vars.count)
            #expect(levelVars.count == n * expectedFullVars.count + nHalf)
            let fullVars = levelVars.filter { !$0.variable.isHalfLevel }
            let halfVars = levelVars.filter { $0.variable.isHalfLevel }
            #expect(Set(fullVars.map { $0.level }) == Set(1...n))
            for level in 1...n {
                #expect(Set(fullVars.filter { $0.level == level }.map { $0.variable }) == expectedFullVars)
            }
            #expect(halfVars.allSatisfy { $0.variable == .wind_w })
            #expect(halfVars.map { $0.level }.sorted() == Array(1...nHalf))
        }
    }

    @Test func modelLevelKeepsUpstreamSemantics() {
        #expect(DownloadIconCommand.VariableGroup.modelLevel.siblingRealm == nil)
        #expect(DownloadIconCommand.VariableGroup.hiresTemp.siblingRealm == "hires-temp")
        for domain in [IconDownloadDomains.iconD2, .iconEu, .icon] {
            let vars = DownloadIconCommand.VariableGroup.modelLevel.variables(domain: domain)
            #expect(vars.allSatisfy { ($0 as? IconModelLevelVariable) == nil })
            #expect(vars.allSatisfy { domain.getVarAndLevel($0)?.cat == "model-level" })
            let expected = IconSurfaceVariable.allCases.filter { domain.getVarAndLevel($0)?.cat == "model-level" }
            #expect(vars.count == expected.count)
        }
    }

    @Test func heidiVarsIsCuratedSurfaceSet() {
        let expected = DownloadIconCommand.VariableGroup.heidiSurface
        #expect(expected.count == 31)
        for domain in [IconDownloadDomains.iconD2, .iconEu, .icon] {
            let vars = DownloadIconCommand.VariableGroup.heidiVars.variables(domain: domain)
            let surface = vars.compactMap { $0 as? IconSurfaceVariable }
            #expect(surface.count == vars.count)
            #expect(Set(surface) == expected)
            #expect(surface.allSatisfy {
                let cat = domain.getVarAndLevel($0)?.cat ?? "single-level"
                return cat == "single-level" || cat == "soil-level"
            })
        }

        #expect(IconDownloadDomains.iconD2.getVarAndLevel(IconSurfaceVariable.cloud_base)?.variable == "ceiling")
        #expect(IconDownloadDomains.iconEu.getVarAndLevel(IconSurfaceVariable.cloud_base)?.variable == "ceiling")
        #expect(IconDownloadDomains.icon.getVarAndLevel(IconSurfaceVariable.cloud_base) == nil)
        #expect(IconDownloadDomains.iconD2.getVarAndLevel(IconSurfaceVariable.model_elevation) == nil)
        #expect(IconDownloadDomains.iconD2.getVarAndLevel(IconSurfaceVariable.visibility) == nil)

        func downloadable(_ domain: IconDownloadDomains) -> Int {
            DownloadIconCommand.VariableGroup.heidiVars.variables(domain: domain)
                .filter { domain.getVarAndLevel($0) != nil }.count
        }
        // VIS is not in the v1 feed, and model_elevation is written from the static file.
        #expect(downloadable(.icon) == 25)
        #expect(downloadable(.iconEu) == 28)
        #expect(downloadable(.iconD2) == 29)
        #expect(IconDownloadDomains.iconD2.getVarAndLevel(IconSurfaceVariable.surface_pressure_model)?.variable == "ps")
        #expect(IconDownloadDomains.iconEps.getVarAndLevel(IconSurfaceVariable.surface_pressure_model) == nil)
        #expect(IconDownloadDomains.iconEuEps.getVarAndLevel(IconSurfaceVariable.surface_pressure_model) == nil)
        #expect(IconDownloadDomains.iconD2Eps.getVarAndLevel(IconSurfaceVariable.surface_pressure_model) == nil)
    }

    @Test func heidiVarsOnlyExcludedFromAllCasesGroups() {
        for domain in [IconDownloadDomains.iconD2, .iconEu, .icon] {
            for group: DownloadIconCommand.VariableGroup in [.all, .surface, .surfaceAndPressure] {
                let surface = group.variables(domain: domain).compactMap { $0 as? IconSurfaceVariable }
                #expect(!surface.contains(.model_elevation))
                #expect(!surface.contains(.surface_pressure_model))
            }
        }
    }

    /// Only sibling names are diverted to the model-level writer.
    @Test func divertedNames() {
        #expect(IconModelLevelVariable(rawValue: "temperature_level65")?.kind == .level(.temperature, 65))
        #expect(IconModelLevelVariable(rawValue: "temperature_80m")?.kind == .surface(.temperature_80m))
        #expect(IconModelLevelVariable(rawValue: "freezing_level_height") == nil)
        #expect(IconModelLevelVariable(rawValue: "temperature_850hPa") == nil)
        #expect(IconModelLevelVariable(rawValue: "temperature_2m") == nil)
    }

    @Test func hhlColumnCacheMemoisesByReference() {
        let cache = HhlColumnCache()
        #expect(cache.column == nil)
        cache.column = [1, 2, 3]
        let copy = cache
        copy.column = [9, 8]
        #expect(cache.column == [9, 8])
    }

    /// The SDK has no model-level field. A level must not be reported as an altitude in metres.
    @Test func flatBuffersDoesNotMapLevelToAltitude() throws {
        let level = try #require(ForecastHeightVariable(rawValue: "temperature_level65"))
        #expect(level.getFlatBuffersMeta().variable == .undefined)
        #expect(level.getFlatBuffersMeta().altitude == 0)
        let fixed = try #require(ForecastHeightVariable(rawValue: "temperature_80m"))
        #expect(fixed.getFlatBuffersMeta().variable == .temperature)
        #expect(fixed.getFlatBuffersMeta().altitude == 80)
    }

    /// heidiVars and the parent surface job both run on the parent. They must not share spatial files.
    @Test func spatialRealmsDoNotClash() {
        #expect(DownloadIconCommand.VariableGroup.heidiVars.realm == "heidi")
        #expect(DownloadIconCommand.VariableGroup.surface.realm == nil)
        #expect(DownloadIconCommand.VariableGroup.hiresTemp.realm == nil)
        #expect(DownloadIconCommand.VariableGroup.hiresTemp.siblingRealm == "hires-temp")
    }

    @Test func hhlMissingFileErrorIsDescriptive() {
        let msg = "\(IconModelLevelError.staticFileMissing(domain: "icon-d2-native"))"
        #expect(msg.contains("hhl.om"))
        #expect(msg.contains("icon-d2-native"))
    }

    @Test func modelLevelOutOfRangeErrorIsDescriptive() {
        let msg = "\(IconModelLevelError.levelOutOfRange(level: 200, max: 65, domain: "icon-d2-native"))"
        #expect(msg.contains("200"))
        #expect(msg.contains("1...65"))
        #expect(msg.contains("icon-d2-native"))
    }

    @Test func specificHumidityUsesLogarithmicCompression() {
        let qv: any GenericVariable = IconModelLevelVariable(variable: .specific_humidity, level: 60)
        let water: any GenericVariable = IconModelLevelVariable(variable: .cloud_water, level: 60)
        let ice: any GenericVariable = IconModelLevelVariable(variable: .cloud_ice, level: 60)
        let t: any GenericVariable = IconModelLevelVariable(variable: .temperature, level: 60)
        #expect(qv.omFileCompression == .pfor_delta2d_int16_logarithmic)
        #expect(water.omFileCompression == .pfor_delta2d_int16_logarithmic)
        #expect(ice.omFileCompression == .pfor_delta2d_int16_logarithmic)
        #expect(qv.scalefactor == 10000)
        #expect(t.omFileCompression == .pfor_delta2d_int16)
        #expect((IconSurfaceVariable.temperature_2m as any GenericVariable).omFileCompression == .pfor_delta2d_int16)
    }

    @Test func logarithmicCompressionPreservesDryLayerQv() async throws {
        let values: [Float] = [0.0004, 0.05, 0.5, 5.0, 25.0]
        let file = FileManager.default.temporaryDirectory.appendingPathComponent("test_qv_log.om").path
        try FileManager.default.removeItemIfExists(at: file)
        defer { try? FileManager.default.removeItem(atPath: file) }
        try values.writeOmFile(file: file, dimensions: [values.count], chunks: [values.count], compression: .pfor_delta2d_int16_logarithmic, scalefactor: 10000)
        let reader = try await OmFileReader(file: file).expectArray(of: Float.self)
        let back = try await reader.read()
        #expect(back[0] > 0)
        #expect(abs(back[0] - 0.0004) < 3e-4)
        for (a, b) in zip(values, back) where a >= 0.05 {
            #expect(abs(a - b) / a < 0.01)
        }
    }
}
