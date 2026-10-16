import Foundation
@testable import App
import Testing

@Suite struct IconLakeElevationTests {
    /// A lake cell has FR_LAND near 0. Masking on land fraction alone stores its HSURF as sea (−999).
    /// FR_LAKE is added first, so the orography stays. Open sea, with neither fraction, is still −999.
    @Test func lakeKeepsHsurfWhileOpenSeaIsMasked() {
        let hsurf: [Float] = [531, 447, 0, 12, 80]
        let land: [Float] = [1.0, 0.05, 0.0, 0.49, 0.2]
        let lake: [Float] = [0.0, 0.86, 0.0, 0.0, 0.3]
        let masked = DownloadIconCommand.maskOpenSea(hsurf: hsurf, landFraction: land, lakeFraction: lake)

        #expect(masked[0] == 531)   // land
        #expect(masked[1] == 447)   // lake: FR_LAND 0.05 + FR_LAKE 0.86
        #expect(masked[2] == -999)  // open sea
        #expect(masked[3] == -999)  // just under 0.5 land, no lake
        #expect(masked[4] == 80)    // 0.2 + 0.3 crosses the threshold
    }

    /// The same low-land cell is sea when FR_LAKE is missing and a lake when it is present.
    @Test func omittingLakeFractionMasksTheLakeAsSea() {
        let hsurf: [Float] = [447]
        let land: [Float] = [0.05]
        let withoutLake = DownloadIconCommand.maskOpenSea(hsurf: hsurf, landFraction: land, lakeFraction: [0])
        let withLake = DownloadIconCommand.maskOpenSea(hsurf: hsurf, landFraction: land, lakeFraction: [0.86])

        #expect(withoutLake == [-999])
        #expect(withLake == [447])
    }

    /// The cut is strictly below one half. A cell at exactly 0.5 keeps HSURF.
    @Test func thresholdKeepsHalfAndMasksJustBelow() {
        let hsurf: [Float] = [100, 200]
        let masked = DownloadIconCommand.maskOpenSea(
            hsurf: hsurf,
            landFraction: [0.5, 0.499],
            lakeFraction: [0, 0]
        )
        #expect(masked == [100, -999])
    }
}
