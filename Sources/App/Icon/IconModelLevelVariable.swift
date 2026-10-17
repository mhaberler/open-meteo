import Foundation
import OmFileFormat

/// Variables on ICON native model levels, named `<variable>_level<N>` (1 = model top).
enum IconModelLevelVariableType: String, CaseIterable, Sendable {
    case height
    case height_agl
    case height_half
    case height_half_agl
    case wind_w
    case wind_u_component
    case wind_v_component
    case temperature
    case specific_humidity
    case relative_humidity
    case pressure
    case wind_speed
    case wind_direction
    case dew_point
    case cloud_water
    case cloud_ice
    case cloud_cover

    var isHalfLevel: Bool {
        switch self {
        case .wind_w, .height_half, .height_half_agl: return true
        default: return false
        }
    }

    /// Computed on read. Nothing is downloaded or stored.
    var isDerived: Bool {
        switch self {
        case .height, .height_agl, .height_half, .height_half_agl, .relative_humidity, .wind_speed, .wind_direction, .dew_point:
            return true
        default:
            return false
        }
    }
}

/// A sibling-domain variable: either a legacy 80/120/180 m surface field or a native `<var>_levelN`.
struct IconModelLevelVariable: GenericVariable, IconVariableDownloadable, Hashable {
    enum Kind: Hashable, Sendable {
        case surface(IconSurfaceVariable)
        case level(IconModelLevelVariableType, Int)
    }

    let kind: Kind

    init(kind: Kind) {
        self.kind = kind
    }

    init(variable: IconModelLevelVariableType, level: Int) {
        self.kind = .level(variable, level)
    }

    init?(rawValue: String) {
        if let surface = IconSurfaceVariable(rawValue: rawValue),
           IconDownloadDomains.icon.getVarAndLevel(surface)?.cat == "model-level" {
            self.kind = .surface(surface)
            return
        }
        guard let range = rawValue.range(of: "_level", options: .backwards) else {
            return nil
        }
        let name = String(rawValue[rawValue.startIndex..<range.lowerBound])
        guard let variable = IconModelLevelVariableType(rawValue: name),
              let level = Int(rawValue[range.upperBound..<rawValue.endIndex]) else {
            return nil
        }
        self.kind = .level(variable, level)
    }

    var rawValue: String {
        switch kind {
        case .surface(let surface):
            return surface.rawValue
        case .level(let variable, let level):
            return "\(variable.rawValue)_level\(level)"
        }
    }

    var level: Int {
        switch kind {
        case .surface:
            return 0
        case .level(_, let level):
            return level
        }
    }

    var variable: IconModelLevelVariableType {
        switch kind {
        case .surface:
            preconditionFailure("80/120/180 m fields are surface variables, not a model-level column")
        case .level(let variable, _):
            return variable
        }
    }

    var omFileName: (file: String, level: Int) {
        (rawValue, 0)
    }

    var scalefactor: Float {
        switch kind {
        case .surface(let surface):
            return surface.scalefactor
        case .level(let variable, _):
            switch variable {
            case .height, .height_agl, .height_half, .height_half_agl: return 1
            case .wind_w: return 100
            case .wind_u_component, .wind_v_component: return 10
            case .temperature: return 10
            case .specific_humidity: return 10000
            case .cloud_water, .cloud_ice: return 30000
            case .relative_humidity, .cloud_cover: return 1
            case .pressure: return 10000 // log10(1 + hPa); 1050 hPa stays below int16
            case .wind_speed, .wind_direction, .dew_point: return 10
            }
        }
    }

    var omFileCompression: OmCompressionType {
        switch kind {
        case .level(let variable, _) where variable == .specific_humidity || variable == .cloud_water || variable == .cloud_ice:
            return .pfor_delta2d_int16_logarithmic
        case .level(.pressure, _):
            // Global tops are near 0.02 hPa. Linear 0.1 hPa steps store the upper levels as 0.
            return .pfor_delta2d_int16_logarithmic
        default:
            return .pfor_delta2d_int16
        }
    }

    var interpolation: ReaderInterpolation {
        switch kind {
        case .surface(let surface):
            return surface.interpolation
        case .level(let variable, _):
            switch variable {
            case .height, .height_agl, .height_half, .height_half_agl, .specific_humidity, .cloud_water, .cloud_ice:
                return .linear
            case .relative_humidity, .cloud_cover:
                return .hermite(bounds: 0...100)
            case .wind_direction:
                return .linearDegrees
            default:
                return .hermite(bounds: nil)
            }
        }
    }

    var unit: SiUnit {
        switch kind {
        case .surface(let surface):
            return surface.unit
        case .level(let variable, _):
            switch variable {
            case .height, .height_agl, .height_half, .height_half_agl: return .metre
            case .wind_w: return .metrePerSecondNotUnitConverted
            case .wind_u_component, .wind_v_component, .wind_speed: return .metrePerSecond
            case .temperature, .dew_point: return .celsius
            case .specific_humidity, .cloud_water, .cloud_ice: return .gramPerKilogram
            case .relative_humidity, .cloud_cover: return .percentage
            case .pressure: return .hectopascal
            case .wind_direction: return .degreeDirection
            }
        }
    }

    var isElevationCorrectable: Bool { false }

    var storePreviousForecast: Bool {
        switch kind {
        case .surface(let surface):
            return surface.storePreviousForecast
        case .level:
            return false
        }
    }

    func skipHour(hour: Int, domain: IconDownloadDomains, forDownload: Bool, run: Timestamp) -> Bool {
        switch kind {
        case .surface(let surface):
            return domain.skipHour(surface, hour: hour, forDownload: forDownload, run: run)
        case .level(let variable, let level):
            return variable == .cloud_cover && level < domain.cloudCoverMinimumModelLevel
        }
    }

    var multiplyAdd: (multiply: Float, add: Float)? {
        switch kind {
        case .surface(let surface):
            return surface.multiplyAdd
        case .level(let variable, _):
            switch variable {
            case .temperature:
                return (1, -273.15)
            case .specific_humidity, .cloud_water, .cloud_ice:
                return (1000, 0)
            case .pressure:
                return (0.01, 0)
            default:
                return nil
            }
        }
    }

    func getVarAndLevel(domain: IconDownloadDomains) -> (variable: String, cat: String, level: Int?)? {
        switch kind {
        case .surface(let surface):
            return domain.getVarAndLevel(surface)
        case .level(let variable, let level):
            if variable.isDerived { return nil }
            let name: String
            switch variable {
            case .wind_w: name = "w"
            case .wind_u_component: name = "u"
            case .wind_v_component: name = "v"
            case .temperature: name = "t"
            case .specific_humidity: name = "qv"
            case .cloud_water: name = "qc"
            case .cloud_ice: name = "qi"
            case .cloud_cover: name = "clc"
            case .pressure: name = "p"
            default: return nil
            }
            return (name, "model-level", level)
        }
    }
}
