import Foundation
import Logging

protocol NonRetryError: Error { }

/// Helper to track timeouts and throw errors once a headline in reached
final class TimeoutTracker {
    let startTime = Date()
    private var lastPrint = Date(timeIntervalSince1970: 0)
    let logger: Logger
    let deadline: Date

    /// Optional context (e.g. the URL being downloaded) prefixed to log messages, so retries can be attributed when multiple downloads run concurrently
    let context: String?

    /// Wait time after each download
    let retryDelaySeconds = 5

    public init(logger: Logger, deadline: Date, context: String? = nil) {
        self.logger = logger
        self.deadline = deadline
        self.context = context
    }

    /// Print statistics, throw if deadline reached, sleep backoff timer
    func check(error: Error, delay: Int? = nil) async throws {
        if let error = error as? NonRetryError {
            throw error
        }
        let delay = delay ?? retryDelaySeconds
        let timeElapsed = Date().timeIntervalSince(startTime)
        if Date().timeIntervalSince(lastPrint) > 60 {
            let prefix = context.map { "[\($0)] " } ?? ""
            logger.info("\(prefix)Download failed, retry every \(delay) seconds, (\(Int(timeElapsed / 60)) minutes elapsed, curl error '\(error) [\(type(of: error))]'")
            lastPrint = Date()
        }
        if Date() > deadline {
            let prefix = context.map { "[\($0)] " } ?? ""
            logger.error("\(prefix)Deadline reached. Last Error \(error) [\(type(of: error))]")
            throw CurlError.timeoutReached
        }
        try await Task.sleep(nanoseconds: UInt64(delay * 1_000_000_000))
    }
}
