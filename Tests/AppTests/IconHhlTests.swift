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

    @Test func levelNamesRoundTrip() {
        let column = ForecastHeightVariable(rawValue: "temperature_level65")
        #expect(column?.modelLevel == true)
        #expect(column?.rawValue == "temperature_level65")
        let fixed = ForecastHeightVariable(rawValue: "temperature_80m")
        #expect(fixed?.modelLevel == false)
        #expect(fixed?.rawValue == "temperature_80m")
        #expect(ForecastVariable(rawValue: "wind_w_level66")?.rawValue == "wind_w_level66")
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
}
