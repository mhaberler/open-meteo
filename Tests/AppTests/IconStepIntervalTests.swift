import Foundation
@testable import App
import Testing

@Suite struct IconStepIntervalTests {
    @Test func hourThenMinuteStepsDeaccumulateInSeconds() async throws {
        let previousHour = try IconStepInterval(start: 0, end: 4, unit: 1)
        let hour5 = try IconStepInterval(start: 0, end: 5, unit: 1)
        let minute315 = try IconStepInterval(start: 0, end: 315, unit: 0)
        let minute330 = try IconStepInterval(start: 0, end: 330, unit: 0)
        let hour6 = try IconStepInterval(start: 0, end: 6, unit: 1)

        #expect(hour5.start == 0)
        #expect(hour5.end == 5 * 3600)
        #expect(minute315.end == 315 * 60)
        #expect(minute330.end == 330 * 60)
        #expect(hour6.end == 6 * 3600)
        #expect(hour6.end > minute330.end)

        let deaverager = GribDeaverager()
        // The previous file's last step is already stored, as it is across hours in a run.
        _ = await increment(deaverager, cumulative: 8, interval: previousHour)
        #expect(await increment(deaverager, cumulative: 10, interval: hour5) == [2])
        #expect(await increment(deaverager, cumulative: 10.5, interval: minute315) == [0.5])
        #expect(await increment(deaverager, cumulative: 11, interval: minute330) == [0.5])
        #expect(await increment(deaverager, cumulative: 14, interval: hour6) == [3])
    }

    @Test func unsupportedStepUnitThrows() {
        #expect(throws: IconStepIntervalError.unsupportedUnit(2)) {
            try IconStepInterval(start: 0, end: 1, unit: 2)
        }
    }

    @Test func instantStepIsUnchanged() async {
        let deaverager = GribDeaverager()
        var grid = Array2D(data: [1.5], nx: 1, ny: 1)
        let kept = await deaverager.deaccumulateIfRequired(
            variable: "snowfall_height",
            member: 0,
            stepType: "instant",
            startStep: 0,
            currentStep: 5 * 3600,
            array2d: &grid
        )
        #expect(kept)
        #expect(grid.data == [1.5])
    }

    private func increment(_ deaverager: GribDeaverager, cumulative: Float, interval: IconStepInterval) async -> [Float] {
        var grid = Array2D(data: [cumulative], nx: 1, ny: 1)
        let kept = await deaverager.deaccumulateIfRequired(
            variable: "precipitation",
            member: 0,
            stepType: "accum",
            startStep: interval.start,
            currentStep: interval.end,
            array2d: &grid
        )
        #expect(kept)
        return grid.data
    }
}
