import Foundation
import Vapor

final class HhlColumnCache: @unchecked Sendable {
    var column: [Float]?
}

/// Height math on one HHL column (ASL, index 0 = model top, last = surface).
/// The last half level is HSURF, so AGL does not depend on the sea-masked elevation.
enum IconHhlColumn {
    /// Full level `n` lies between half levels `n` and `n+1`.
    static func fullLevelASL(_ heights: [Float], fullLevel: Int) -> Float? {
        guard fullLevel >= 1, fullLevel < heights.count else { return nil }
        let lower = heights[fullLevel - 1]
        let upper = heights[fullLevel]
        guard lower.isFinite, upper.isFinite else { return .nan }
        return (lower + upper) / 2
    }

    static func halfLevelASL(_ heights: [Float], halfLevel: Int) -> Float? {
        guard halfLevel >= 1, halfLevel <= heights.count else { return nil }
        let height = heights[halfLevel - 1]
        return height.isFinite ? height : .nan
    }

    static func aboveGround(_ asl: Float?, heights: [Float]) -> Float? {
        guard let asl else { return nil }
        guard let surface = heights.last, surface.isFinite else { return .nan }
        return asl - surface
    }
}

extension IconNativeDomain {
    func makeModelLevelDerived(lat: Float, lon: Float, elevation: Float, mode: GridSelectionMode, options: GenericReaderOptions) async throws -> VariableHourlyDeriver<IconModelLevelReader>? {
        guard let raw = try await GenericReader<IconNativeDomain, IconModelLevelVariable>(domain: self, lat: lat, lon: lon, elevation: elevation, mode: mode, options: options) else {
            return nil
        }
        return VariableHourlyDeriver(reader: IconModelLevelReader(reader: raw), options: options, domainRegistry: domainRegistry)
    }
}

enum IconModelLevelError: Error, CustomStringConvertible, AbortError {
    case levelOutOfRange(level: Int, max: Int, domain: String)
    case staticFileMissing(domain: String)

    var status: HTTPResponseStatus { .badRequest }

    var reason: String { description }

    var description: String {
        switch self {
        case .levelOutOfRange(let level, let max, let domain):
            return "Model level \(level) is out of range for domain '\(domain)' (valid 1...\(max))."
        case .staticFileMissing(let domain):
            return "Static hhl.om is missing for domain '\(domain)'."
        }
    }
}

/// Reads the model-level sibling. Stored fields come from the time series. Heights come from the
/// parent's `hhl.om`. Relative humidity, dew point, and wind are derived from the stored column.
struct IconModelLevelReader: GenericReaderProtocol {
    typealias MixingVar = IconModelLevelVariable

    let reader: GenericReader<IconNativeDomain, IconModelLevelVariable>
    let hhlCache = HhlColumnCache()

    var modelLat: Float { reader.modelLat }
    var modelLon: Float { reader.modelLon }
    var modelElevation: ElevationOrSea { reader.modelElevation }
    var targetElevation: Float { reader.targetElevation }
    var modelDtSeconds: Int { reader.modelDtSeconds }

    var sourceDomain: IconDomains { reader.domain.definition.sourceDomain }
    var domainName: String { reader.domain.definition.rawValue }

    func getStatic(type: ReaderStaticVariable) async throws -> Float? {
        try await reader.getStatic(type: type)
    }

    func prefetchData(variable: IconModelLevelVariable, time: TimerangeDtAndSettings) async throws {
        switch variable.kind {
        case .surface:
            try await reader.prefetchData(variable: variable, time: time)
        case .level(let type, let level):
            try validate(type: type, level: level)
            if type.isDerived {
                switch type {
                case .relative_humidity, .dew_point:
                    try await prefetchStored(.specific_humidity, level: level, time: time)
                    try await prefetchStored(.temperature, level: level, time: time)
                    try await prefetchStored(.pressure, level: level, time: time)
                case .wind_speed, .wind_direction:
                    try await prefetchStored(.wind_u_component, level: level, time: time)
                    try await prefetchStored(.wind_v_component, level: level, time: time)
                default:
                    break
                }
                return
            }
            try await reader.prefetchData(variable: variable, time: time)
        }
    }

    func get(variable: IconModelLevelVariable, time: TimerangeDtAndSettings) async throws -> DataAndUnit {
        switch variable.kind {
        case .surface:
            return try await reader.get(variable: variable, time: time)
        case .level(let type, let level):
            try validate(type: type, level: level)
            switch type {
            case .height:
                return try await constant(try fullLevelHeightASL(fullLevel: level), count: time.time.count, unit: .metre)
            case .height_agl:
                return try await constant(try fullLevelHeightAGL(fullLevel: level), count: time.time.count, unit: .metre)
            case .height_half:
                return try await constant(try halfLevelHeightASL(halfLevel: level), count: time.time.count, unit: .metre)
            case .height_half_agl:
                return try await constant(try halfLevelHeightAGL(halfLevel: level), count: time.time.count, unit: .metre)
            case .relative_humidity:
                let qv = try await stored(.specific_humidity, level: level, time: time)
                let temperature = try await stored(.temperature, level: level, time: time)
                let pressure = try await stored(.pressure, level: level, time: time)
                return DataAndUnit(Meteorology.specificToRelativeHumidity(specificHumidity: qv.data, temperature: temperature.data, pressure: pressure.data), .percentage)
            case .dew_point:
                let humidity = try await get(variable: IconModelLevelVariable(kind: .level(.relative_humidity, level)), time: time)
                let temperature = try await stored(.temperature, level: level, time: time)
                return DataAndUnit(zip(temperature.data, humidity.data).map(Meteorology.dewpoint(temperature:relativeHumidity:)), .celsius)
            case .wind_speed:
                let u = try await stored(.wind_u_component, level: level, time: time)
                let v = try await stored(.wind_v_component, level: level, time: time)
                return DataAndUnit(zip(u.data, v.data).map(Meteorology.windspeed(u:v:)), .metrePerSecond)
            case .wind_direction:
                let u = try await stored(.wind_u_component, level: level, time: time)
                let v = try await stored(.wind_v_component, level: level, time: time)
                return DataAndUnit(Meteorology.windirectionFast(u: u.data, v: v.data), .degreeDirection)
            default:
                return try await reader.get(variable: variable, time: time)
            }
        }
    }

    private func stored(_ type: IconModelLevelVariableType, level: Int, time: TimerangeDtAndSettings) async throws -> DataAndUnit {
        try await reader.get(variable: IconModelLevelVariable(kind: .level(type, level)), time: time)
    }

    private func prefetchStored(_ type: IconModelLevelVariableType, level: Int, time: TimerangeDtAndSettings) async throws {
        try await reader.prefetchData(variable: IconModelLevelVariable(kind: .level(type, level)), time: time)
    }

    private func validate(type: IconModelLevelVariableType, level: Int) throws {
        let max = type.isHalfLevel ? sourceDomain.numberOfModelHalfLevels : sourceDomain.numberOfModelFullLevels
        guard (1...max).contains(level) else {
            throw IconModelLevelError.levelOutOfRange(level: level, max: max, domain: domainName)
        }
    }

    private func constant(_ value: Float?, count: Int, unit: SiUnit) -> DataAndUnit {
        DataAndUnit([Float](repeating: value ?? .nan, count: count), unit)
    }

    func hhlColumnASL() async throws -> [Float] {
        if let cached = hhlCache.column {
            return cached
        }
        guard let file = await reader.domain.getStaticFile(type: .hhl, httpClient: reader.httpClient, logger: reader.logger) else {
            throw IconModelLevelError.staticFileMissing(domain: domainName)
        }
        let column = try await reader.domain.grid.readColumnFromStaticFile(gridpoint: reader.position, file: file)
        hhlCache.column = column
        return column
    }

    func fullLevelHeightASL(fullLevel: Int) async throws -> Float? {
        IconHhlColumn.fullLevelASL(try await hhlColumnASL(), fullLevel: fullLevel)
    }

    func fullLevelHeightAGL(fullLevel: Int) async throws -> Float? {
        let heights = try await hhlColumnASL()
        return IconHhlColumn.aboveGround(IconHhlColumn.fullLevelASL(heights, fullLevel: fullLevel), heights: heights)
    }

    func halfLevelHeightASL(halfLevel: Int) async throws -> Float? {
        IconHhlColumn.halfLevelASL(try await hhlColumnASL(), halfLevel: halfLevel)
    }

    func halfLevelHeightAGL(halfLevel: Int) async throws -> Float? {
        let heights = try await hhlColumnASL()
        return IconHhlColumn.aboveGround(IconHhlColumn.halfLevelASL(heights, halfLevel: halfLevel), heights: heights)
    }
}
