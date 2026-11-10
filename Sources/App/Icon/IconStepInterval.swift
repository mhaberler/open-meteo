import Foundation
@preconcurrency import SwiftEccodes

enum IconStepIntervalError: Error, Equatable {
    case unsupportedUnit(Int)
    case invalidInterval(start: Int, end: Int)
    case missingStep
}

/// Forecast window from a GRIB message, with both ends in seconds.
///
/// ICON-D2 quarter-hour files mix hour ranges (`0-5`) and minute ranges (`0m-315m`) in one
/// `stepRange` string. The numeric keys stay plain integers, so the 15-minute deaverager can
/// compare a later hour (`6` h = 21,600 s) with the previous minute step (`345` min = 20,700 s).
struct IconStepInterval: Equatable {
    let start: Int
    let end: Int

    init(start: Int, end: Int, unit: Int) throws {
        let seconds: Int
        switch unit {
        case 0: seconds = 60
        case 1: seconds = 3600
        default: throw IconStepIntervalError.unsupportedUnit(unit)
        }
        guard start >= 0, end >= start else {
            throw IconStepIntervalError.invalidInterval(start: start, end: end)
        }
        self.start = start * seconds
        self.end = end * seconds
    }

    init(_ message: GribMessage) throws {
        guard let start = message.getLong(attribute: "startStep"),
              let end = message.getLong(attribute: "endStep"),
              let unit = message.getLong(attribute: "stepUnits") else {
            throw IconStepIntervalError.missingStep
        }
        try self.init(start: start, end: end, unit: unit)
    }
}
