---
name: gortex-sources-niohttp2-111-dirs
description: "Work in the Sources/NIOHTTP2 +111 dirs area — 2695 symbols across 331 files (96% cohesion)"
---

# Sources/NIOHTTP2 +111 dirs

2695 symbols | 331 files | 96% cohesion

## When to Use

Use this skill when working on files in:
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/AsyncAwait/HTTPClient+execute.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/AsyncAwait/Transaction+StateMachine.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/ChannelHandler/HTTP1ProxyConnectHandler.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/ChannelHandler/SOCKSEventsHandler.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/ChannelHandler/TLSEventsHandler.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP1/HTTP1ClientChannelHandler.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP1/HTTP1Connection.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP2/HTTP2ClientRequestHandler.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP2/HTTP2Connection.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP2/HTTP2IdleHandler.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPConnectionPool+Factory.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPConnectionPool+Manager.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPConnectionPool.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPExecutableRequest.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPRequestStateMachine+Demand.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPRequestStateMachine.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+Backoff.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP1Connections.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP1StateMachine.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP2Connections.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP2StateMachine.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+StateMachine.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/HTTPHandler.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/NIOTransportServices/NWErrorHandler.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/RequestBag+StateMachine.swift`
- `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/RequestBag.swift`
- `.build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/AsyncTestHelpers.swift`
- `.build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTP1ClientChannelHandlerTests.swift`
- `.build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTP1ConnectionTests.swift`
- `.build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTP2ConnectionTests.swift`
- `.build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTPClientTestUtils.swift`
- `.build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTPConnectionPool+RequestQueueTests.swift`
- `.build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/Mocks/MockConnectionPool.swift`
- `.build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/Mocks/MockHTTPExecutableRequest.swift`
- `.build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/RequestBagTests.swift`
- `.build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/TransactionTests.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOCore/Channel.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOCore/ChannelPipeline.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOCore/DeadChannel.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOCore/EventLoopFuture.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOEmbedded/Embedded.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOFileSystem/FileChunks.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/HTTPDecoder.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/HTTPServerUpgradeHandler.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/NIOHTTPObjectAggregator.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/NIOTypedHTTPClientUpgraderStateMachine.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/NIOTypedHTTPServerUpgraderStateMachine.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/BaseSocketChannel.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/MultiThreadedEventLoopGroup.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/PendingDatagramWritesManager.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/PendingWritesManager.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/SelectableEventLoop.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/SocketChannel.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOTLS/ProtocolNegotiationHandlerStateMachine.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOTestUtils/NIOHTTP1TestServer.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOCoreTests/CustomChannelTests.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/MulticastTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NIOScheduledCallbackTests.swift`
- `.build/checkouts/swift-async-algorithms/Sources/AsyncAlgorithms/Channels/AsyncThrowingChannel.swift`
- `.build/checkouts/swift-nio-extras/Sources/NIOExtras/HTTP1ProxyConnectHandler.swift`
- `.build/checkouts/swift-nio-extras/Sources/NIOExtras/QuiescingHelper.swift`
- `.build/checkouts/swift-nio-extras/Sources/NIOHTTPCompression/HTTPRequestCompressor.swift`
- `.build/checkouts/swift-nio-extras/Sources/NIOHTTPTypesHTTP2/HTTP2ToHTTPCodec.swift`
- `.build/checkouts/swift-nio-extras/Sources/NIONFS3/NFSFileSystemInvoker.swift`
- `.build/checkouts/swift-nio-extras/Sources/NIONFS3/NFSTypes+Containers.swift`
- `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/ConnectionStateMachine/ConnectionStateMachine.swift`
- `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/ConnectionStateMachine/ConnectionStreamsState.swift`
- `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/Frame Buffers/ConcurrentStreamBuffer.swift`
- `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/Frame Buffers/OutboundFlowControlBuffer.swift`
- `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/Frame Buffers/OutboundFrameBuffer.swift`
- `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2ChannelHandler+InboundStreamMultiplexer.swift`
- `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2ChannelHandler.swift`
- `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2CommonInboundStreamMultiplexer.swift`
- `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2FrameParser.swift`
- `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2StreamChannel.swift`
- `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2StreamDelegate.swift`
- `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2ToHTTP1Codec.swift`
- `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/NIOHTTP2ServerConnectionManagementHandler+StateMachine.swift`
- `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/NIOHTTP2ServerConnectionManagementHandler.swift`
- `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/StreamStateMachine.swift`
- `.build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/ConfiguringPipelineAsyncMultiplexerTests.swift`
- `.build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/HTTP2InlineStreamMultiplexerTests.swift`
- `.build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/OutboundFlowControlBufferTests.swift`
- `.build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/TestUtilities.swift`
- `.build/checkouts/swift-nio-ssl/Sources/NIOSSL/ByteBufferBIO.swift`
- `.build/checkouts/swift-nio-ssl/Sources/NIOSSL/CustomPrivateKey.swift`
- `.build/checkouts/swift-nio-ssl/Sources/NIOSSL/IdentityVerification.swift`
- `.build/checkouts/swift-nio-ssl/Sources/NIOSSL/NIOSSLHandler.swift`
- `.build/checkouts/swift-nio-ssl/Sources/NIOSSL/SSLCallbacks.swift`
- `.build/checkouts/swift-nio-ssl/Sources/NIOSSL/SSLConnection.swift`
- `.build/checkouts/swift-nio-ssl/Sources/NIOSSL/SSLContext.swift`
- `.build/checkouts/swift-nio-ssl/Sources/NIOSSL/SecurityFrameworkCertificateVerification.swift`
- `.build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/NIOFilterEmptyWritesHandler.swift`
- `.build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/SocketAddress+NWEndpoint.swift`
- `.build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/StateManagedChannel.swift`
- `.build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/StateManagedListenerChannel.swift`
- `.build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/StateManagedNWConnectionChannel.swift`
- `.build/checkouts/swift-nio/Sources/NIOCore/Channel.swift`
- `.build/checkouts/swift-nio/Sources/NIOCore/ChannelPipeline.swift`
- `.build/checkouts/swift-nio/Sources/NIOCore/DeadChannel.swift`
- `.build/checkouts/swift-nio/Sources/NIOCore/EventLoopFuture.swift`
- `.build/checkouts/swift-nio/Sources/NIOEmbedded/Embedded.swift`
- `.build/checkouts/swift-nio/Sources/NIOFS/FileChunks.swift`
- `.build/checkouts/swift-nio/Sources/NIOHTTP1/HTTPDecoder.swift`
- `.build/checkouts/swift-nio/Sources/NIOHTTP1/HTTPServerUpgradeHandler.swift`
- `.build/checkouts/swift-nio/Sources/NIOHTTP1/NIOHTTPObjectAggregator.swift`
- `.build/checkouts/swift-nio/Sources/NIOHTTP1/NIOTypedHTTPClientUpgraderStateMachine.swift`
- `.build/checkouts/swift-nio/Sources/NIOHTTP1/NIOTypedHTTPServerUpgraderStateMachine.swift`
- `.build/checkouts/swift-nio/Sources/NIOPosix/BaseSocketChannel.swift`
- `.build/checkouts/swift-nio/Sources/NIOPosix/MultiThreadedEventLoopGroup.swift`
- `.build/checkouts/swift-nio/Sources/NIOPosix/PendingDatagramWritesManager.swift`
- `.build/checkouts/swift-nio/Sources/NIOPosix/PendingWritesManager.swift`
- `.build/checkouts/swift-nio/Sources/NIOPosix/SelectableEventLoop.swift`
- `.build/checkouts/swift-nio/Sources/NIOPosix/SocketChannel.swift`
- `.build/checkouts/swift-nio/Sources/NIOTLS/ProtocolNegotiationHandlerStateMachine.swift`
- `.build/checkouts/swift-nio/Sources/NIOTestUtils/NIOHTTP1TestServer.swift`
- `.build/checkouts/swift-nio/Sources/_NIOFileSystem/FileChunks.swift`
- `.build/checkouts/swift-nio/Tests/NIOCoreTests/CustomChannelTests.swift`
- `.build/checkouts/swift-nio/Tests/NIOFSIntegrationTests/FileSystemTests.swift`
- `.build/checkouts/swift-nio/Tests/NIOPosixTests/MulticastTest.swift`
- `.build/checkouts/swift-nio/Tests/NIOPosixTests/NIOScheduledCallbackTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/AsyncAwait/HTTPClient+execute.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/AsyncAwait/Transaction+StateMachine.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/ChannelHandler/HTTP1ProxyConnectHandler.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/ChannelHandler/SOCKSEventsHandler.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/ChannelHandler/TLSEventsHandler.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP1/HTTP1ClientChannelHandler.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP1/HTTP1Connection.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP2/HTTP2ClientRequestHandler.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP2/HTTP2Connection.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP2/HTTP2IdleHandler.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPConnectionPool+Factory.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPConnectionPool+Manager.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPConnectionPool.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPExecutableRequest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPRequestStateMachine+Demand.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPRequestStateMachine.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+Backoff.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP1Connections.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP1StateMachine.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP2Connections.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP2StateMachine.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+StateMachine.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/HTTPHandler.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/NIOTransportServices/NWErrorHandler.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/RequestBag+StateMachine.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/RequestBag.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/AsyncTestHelpers.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTP1ClientChannelHandlerTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTP1ConnectionTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTP2ConnectionTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTPClientTestUtils.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTPConnectionPool+RequestQueueTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/Mocks/MockConnectionPool.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/Mocks/MockHTTPExecutableRequest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/RequestBagTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/TransactionTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-async-algorithms/Sources/AsyncAlgorithms/Channels/AsyncThrowingChannel.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-extras/Sources/NIOExtras/HTTP1ProxyConnectHandler.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-extras/Sources/NIOExtras/QuiescingHelper.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-extras/Sources/NIOHTTPCompression/HTTPRequestCompressor.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-extras/Sources/NIOHTTPTypesHTTP2/HTTP2ToHTTPCodec.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-extras/Sources/NIONFS3/NFSFileSystemInvoker.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-extras/Sources/NIONFS3/NFSTypes+Containers.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/ConnectionStateMachine/ConnectionStateMachine.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/ConnectionStateMachine/ConnectionStreamsState.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/Frame Buffers/ConcurrentStreamBuffer.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/Frame Buffers/OutboundFlowControlBuffer.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/Frame Buffers/OutboundFrameBuffer.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2ChannelHandler+InboundStreamMultiplexer.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2ChannelHandler.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2CommonInboundStreamMultiplexer.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2FrameParser.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2StreamChannel.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2StreamDelegate.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2ToHTTP1Codec.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/StreamStateMachine.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/ConfiguringPipelineAsyncMultiplexerTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/HTTP2InlineStreamMultiplexerTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/OutboundFlowControlBufferTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/TestUtilities.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/ByteBufferBIO.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/CustomPrivateKey.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/NIOSSLHandler.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/SSLCallbacks.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/SSLConnection.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/SSLContext.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/SecurityFrameworkCertificateVerification.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/NIOFilterEmptyWritesHandler.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/SocketAddress+NWEndpoint.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/StateManagedChannel.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/StateManagedListenerChannel.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/StateManagedNWConnectionChannel.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOCore/Channel.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOCore/ChannelPipeline.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOCore/DeadChannel.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOCore/EventLoopFuture.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOEmbedded/Embedded.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOFileSystem/FileChunks.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/HTTPDecoder.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/HTTPServerUpgradeHandler.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/NIOHTTPObjectAggregator.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/NIOTypedHTTPClientUpgraderStateMachine.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/NIOTypedHTTPServerUpgraderStateMachine.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/BaseSocketChannel.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/MultiThreadedEventLoopGroup.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/PendingDatagramWritesManager.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/PendingWritesManager.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/SelectableChannel.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/SelectableEventLoop.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/SocketChannel.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOTLS/ProtocolNegotiationHandlerStateMachine.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOTestUtils/NIOHTTP1TestServer.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOCoreTests/CustomChannelTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/MulticastTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NIOScheduledCallbackTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/websocket-kit/Sources/WebSocketKit/WebSocket.swift`
- `.build/checkouts/vapor/Sources/Vapor/Concurrency/RequestBody+Concurrency.swift`
- `.build/checkouts/vapor/Sources/Vapor/HTTP/Server/HTTPServerRequestDecoder.swift`
- `.build/checkouts/vapor/Tests/VaporTests/ServerTests.swift`
- `.build/checkouts/websocket-kit/Sources/WebSocketKit/WebSocket.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/AsyncAwait/HTTPClient+execute.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/AsyncAwait/Transaction+StateMachine.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/ChannelHandler/HTTP1ProxyConnectHandler.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/ChannelHandler/SOCKSEventsHandler.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/ChannelHandler/TLSEventsHandler.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP1/HTTP1ClientChannelHandler.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP1/HTTP1Connection.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP2/HTTP2ClientRequestHandler.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP2/HTTP2Connection.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP2/HTTP2IdleHandler.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPConnectionPool+Factory.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPConnectionPool+Manager.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPConnectionPool.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPExecutableRequest.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPRequestStateMachine+Demand.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPRequestStateMachine.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+Backoff.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP1Connections.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP1StateMachine.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP2Connections.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP2StateMachine.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+StateMachine.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/HTTPHandler.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/NIOTransportServices/NWErrorHandler.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/RequestBag+StateMachine.swift`
- `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/RequestBag.swift`
- `.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/AsyncTestHelpers.swift`
- `.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTP1ClientChannelHandlerTests.swift`
- `.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTP1ConnectionTests.swift`
- `.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTP2ConnectionTests.swift`
- `.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTPClientTestUtils.swift`
- `.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTPConnectionPool+RequestQueueTests.swift`
- `.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/Mocks/MockConnectionPool.swift`
- `.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/Mocks/MockHTTPExecutableRequest.swift`
- `.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/RequestBagTests.swift`
- `.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/TransactionTests.swift`
- `.build/index-build/checkouts/swift-async-algorithms/Sources/AsyncAlgorithms/Channels/AsyncThrowingChannel.swift`
- `.build/index-build/checkouts/swift-nio-extras/Sources/NIOExtras/HTTP1ProxyConnectHandler.swift`
- `.build/index-build/checkouts/swift-nio-extras/Sources/NIOExtras/QuiescingHelper.swift`
- `.build/index-build/checkouts/swift-nio-extras/Sources/NIOHTTPCompression/HTTPRequestCompressor.swift`
- `.build/index-build/checkouts/swift-nio-extras/Sources/NIOHTTPTypesHTTP2/HTTP2ToHTTPCodec.swift`
- `.build/index-build/checkouts/swift-nio-extras/Sources/NIONFS3/NFSFileSystemInvoker.swift`
- `.build/index-build/checkouts/swift-nio-extras/Sources/NIONFS3/NFSTypes+Containers.swift`
- `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/ConnectionStateMachine/ConnectionStateMachine.swift`
- `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/ConnectionStateMachine/ConnectionStreamsState.swift`
- `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/Frame Buffers/ConcurrentStreamBuffer.swift`
- `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/Frame Buffers/OutboundFlowControlBuffer.swift`
- `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/Frame Buffers/OutboundFrameBuffer.swift`
- `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2ChannelHandler+InboundStreamMultiplexer.swift`
- `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2ChannelHandler.swift`
- `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2CommonInboundStreamMultiplexer.swift`
- `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2FrameParser.swift`
- `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2StreamChannel.swift`
- `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2StreamDelegate.swift`
- `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2ToHTTP1Codec.swift`
- `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/NIOHTTP2ServerConnectionManagementHandler+StateMachine.swift`
- `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/NIOHTTP2ServerConnectionManagementHandler.swift`
- `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/StreamStateMachine.swift`
- `.build/index-build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/ConfiguringPipelineAsyncMultiplexerTests.swift`
- `.build/index-build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/HTTP2InlineStreamMultiplexerTests.swift`
- `.build/index-build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/OutboundFlowControlBufferTests.swift`
- `.build/index-build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/TestUtilities.swift`
- `.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/ByteBufferBIO.swift`
- `.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/CustomPrivateKey.swift`
- `.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/IdentityVerification.swift`
- `.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/NIOSSLHandler.swift`
- `.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/SSLCallbacks.swift`
- `.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/SSLConnection.swift`
- `.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/SSLContext.swift`
- `.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/SecurityFrameworkCertificateVerification.swift`
- `.build/index-build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/NIOFilterEmptyWritesHandler.swift`
- `.build/index-build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/SocketAddress+NWEndpoint.swift`
- `.build/index-build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/StateManagedChannel.swift`
- `.build/index-build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/StateManagedListenerChannel.swift`
- `.build/index-build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/StateManagedNWConnectionChannel.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOCore/Channel.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOCore/ChannelPipeline.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOCore/Codec.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOCore/DeadChannel.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOCore/EventLoopFuture.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOCore/GlobalSingletons.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOCore/Linux.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOCore/NIOScheduledCallback.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOCore/TypeAssistedChannelHandler.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOCore/Utilities.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOEmbedded/Embedded.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOFS/FileChunks.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/HTTPDecoder.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/HTTPServerUpgradeHandler.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/NIOHTTPObjectAggregator.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/NIOTypedHTTPClientUpgraderStateMachine.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/NIOTypedHTTPServerUpgraderStateMachine.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOPosix/BaseSocketChannel.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOPosix/MultiThreadedEventLoopGroup.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOPosix/NonBlockingFileIO.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOPosix/PendingDatagramWritesManager.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOPosix/PendingWritesManager.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOPosix/SelectableEventLoop.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOPosix/SocketChannel.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOTLS/ProtocolNegotiationHandlerStateMachine.swift`
- `.build/index-build/checkouts/swift-nio/Sources/NIOTestUtils/NIOHTTP1TestServer.swift`
- `.build/index-build/checkouts/swift-nio/Sources/_NIOFileSystem/FileChunks.swift`
- `.build/index-build/checkouts/swift-nio/Tests/NIOCoreTests/CustomChannelTests.swift`
- `.build/index-build/checkouts/swift-nio/Tests/NIOFSIntegrationTests/FileSystemTests.swift`
- `.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/MulticastTest.swift`
- `.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NIOScheduledCallbackTests.swift`
- `.build/index-build/checkouts/vapor/Sources/Vapor/Concurrency/RequestBody+Concurrency.swift`
- `.build/index-build/checkouts/vapor/Sources/Vapor/HTTP/Server/HTTPServerRequestDecoder.swift`
- `.build/index-build/checkouts/vapor/Tests/VaporTests/ServerTests.swift`
- `.build/index-build/checkouts/websocket-kit/Sources/WebSocketKit/WebSocket.swift`

## Key Files

| File | Symbols |
|------|---------|
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/AsyncAwait/HTTPClient+execute.swift` | TransactionCancelHandler, cancelTransaction, _registerTransaction, _cancel, cancel, ... |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/AsyncAwait/Transaction+StateMachine.swift` | httpResponseStreamTerminated, StateMachine, pauseRequestBodyStream, receiveResponseBodyParts, finishRequestBodyStream, ... |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/ChannelHandler/HTTP1ProxyConnectHandler.swift` | sendConnect, handleHTTPHeadReceived, channelInactive, write, handleHTTPEndReceived, ... |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/ChannelHandler/SOCKSEventsHandler.swift` | userInboundEventTriggered |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/ChannelHandler/TLSEventsHandler.swift` | userInboundEventTriggered |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP1/HTTP1ClientChannelHandler.swift` | writeRequestBodyPart, channelWritabilityChanged, cancelRequest, RequestExecutor, demandResponseBodyStream, ... |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP1/HTTP1Connection.swift` | HTTP1ConnectionDelegate |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP2/HTTP2ClientRequestHandler.swift` | RequestExecutor, demandResponseBodyStream, finishRequestBodyStream, writeRequestBodyPart, cancelRequest |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP2/HTTP2Connection.swift` | __forTesting_getStreamChannels, http2SettingsReceived, HTTP2ConnectionDelegate, shutdown0, HTTP2Connection, ... |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP2/HTTP2IdleHandler.swift` | closeEventReceived, StateMachine, channelActive, goAwayReceived, channelInactive, ... |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPConnectionPool+Factory.swift` | makePlainBootstrap, setupTLSInProxyConnectionIfNeeded |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPConnectionPool+Manager.swift` | executeRequest, connectionPoolDidShutdown, Manager, shutdown |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPConnectionPool.swift` | modifyStateAndRunActions, createConnection, cancelIdleTimerForConnection, cancelRequestTimeout, HTTPConnectionPool, ... |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPExecutableRequest.swift` | HTTPSchedulableRequest, HTTPRequestExecutor, HTTPRequestScheduler, HTTPExecutableRequest |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPRequestStateMachine+Demand.swift` | receivedBodyPart, read, demandMoreResponseBodyParts, end, ResponseStreamState, ... |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPRequestStateMachine.swift` | startRequest, requestStreamPartReceived, handleNIOSSLUncleanShutdownError, channelRead, idleWriteTimeoutTriggered, ... |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+Backoff.swift` | calculateBackoff |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP1Connections.swift` | release, backoffNextConnectionAttempt, shutdown, startingEventLoopConnections, migrateToHTTP2, ... |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP1StateMachine.swift` | _newHTTP1ConnectionEstablished, nextActionForToBeClosedIdleConnection, failedToCreateNewConnection, http2ConnectionClosed, waitingForConnectivity, ... |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP2Connections.swift` | leaseStreams, createNewConnectionByReplacingClosedConnection, close, addStats, fail, ... |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP2StateMachine.swift` | http2ConnectionStreamClosed, connectionCreationBackoffDone, HTTP2StateMachine, nextActionForFailedConnection, nextActionForClosingConnection, ... |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+StateMachine.swift` | http2ConnectionGoAwayReceived, newHTTP2ConnectionCreated, newHTTP2MaxConcurrentStreamsReceived, connectionIdleTimeout, http1ConnectionReleased, ... |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/HTTPHandler.swift` | didVisitURL, ResponseAccumulator, didReceiveHead, didFinishRequest, didReceiveError, ... |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/NIOTransportServices/NWErrorHandler.swift` | translateError, errorCaught, NWErrorHandler |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/RequestBag+StateMachine.swift` | willExecuteRequest, receiveResponseHead, writeNextRequestPart, finishRequestBodyStream, pauseRequestBodyStream, ... |
| `.build/checkouts/async-http-client/Sources/AsyncHTTPClient/RequestBag.swift` | deadlineExceeded0, requestHeadSent0, fail0, pauseRequestBodyStream0, failTask0, ... |
| `.build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/AsyncTestHelpers.swift` | demand, next, writeBufferOrEnd |
| `.build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTP1ClientChannelHandlerTests.swift` | next, ResponseBackpressureDelegate, didReceiveBodyPart, didFinishRequest, didReceiveHead |
| `.build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTP1ConnectionTests.swift` | MockHTTP1ConnectionDelegate, http1ConnectionClosed, http1ConnectionReleased, http1ConnectionClosed, MockConnectionDelegate, ... |
| `.build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTP2ConnectionTests.swift` | TestHTTP2ConnectionDelegate, http1ConnectionClosed, type2, EmptyHTTP2ConnectionDelegate, http2ConnectionCreated, ... |
| `.build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTPClientTestUtils.swift` | didFinishRequest, next0, didReceiveError, next, TestHTTPDelegate, ... |
| `.build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTPConnectionPool+RequestQueueTests.swift` | receiveResponseBodyParts, requestBodyStreamSent, receiveResponseEnd, pauseRequestBodyStream, fail, ... |
| `.build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/Mocks/MockConnectionPool.swift` | requestWasQueued, willExecuteRequest, requestHeadSent, resumeRequestBodyStream, receiveResponseEnd, ... |
| `.build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/Mocks/MockHTTPExecutableRequest.swift` | requestBodyStreamSent, receiveResponseHead, resumeRequestBodyStream, receiveResponseBodyParts, MockHTTPExecutableRequest, ... |
| `.build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/RequestBagTests.swift` | cancelRequest, MockTaskQueuer |
| `.build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/TransactionTests.swift` | demandResponseBodyStream, Executor, finishRequestBodyStream, Promise, fulfil, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOCore/Channel.swift` | ChannelCore |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOCore/ChannelPipeline.swift` | register, close |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOCore/DeadChannel.swift` | DeadChannelCore, write0, registerAlreadyConfigured0, flush0, register0, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOCore/EventLoopFuture.swift` | _setValue, EventLoopPromise, completeWith, _resolve, succeed, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOEmbedded/Embedded.swift` | register0, printError, triggerUserOutboundEvent0, checkCorrectThread, preconditionNotInEventLoop, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOFileSystem/FileChunks.swift` | performedProduceMore, activeThreadPool, didReadBytes, ProducerState, fileReadingState, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/HTTPDecoder.swift` | didReceiveStatusData, didReceiveHeaderFieldData, didReceiveBodyData, didReceiveHeadersCompleteNotification, didReceiveHeaderValueData, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/HTTPServerUpgradeHandler.swift` | channelRead, gotUpgrader |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/NIOHTTPObjectAggregator.swift` | idle, ignoringContent, messageHeadReceived, handlingOversizeMessage, messageEndReceived, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/NIOTypedHTTPClientUpgraderStateMachine.swift` | unbuffer |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/NIOTypedHTTPServerUpgraderStateMachine.swift` | upgradingHandlerCompleted, unbuffer, NIOTypedHTTPServerUpgraderStateMachine, channelReadData, handlerRemoved, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/BaseSocketChannel.swift` | readEOF0, badTransition |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/MultiThreadedEventLoopGroup.swift` | runTheLoop, withCurrentThreadAsEventLoop, shutdownGracefully, next, _preconditionSafeToSyncShutdown, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/PendingDatagramWritesManager.swift` | triggerVectorBufferWrite, doPendingDatagramWriteVectorOperation, triggerAppropriateWriteOperations, PendingDatagramWrite, copySocketAddress |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/PendingWritesManager.swift` | triggerAppropriateWriteOperations, doPendingWriteVectorOperation, PendingStreamWritesManager, didWrite, markFlushCheckpoint, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/SelectableEventLoop.swift` | cancelScheduledCallback, syncFinaliseClose |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/SocketChannel.swift` | leave, connectSocket, join, performGroupOperation0, GroupOperation, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOTLS/ProtocolNegotiationHandlerStateMachine.swift` | ProtocolNegotiationHandlerStateMachine, userInboundEventTriggered, unbuffer, handlerRemoved, channelRead, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Sources/NIOTestUtils/NIOHTTP1TestServer.swift` | NIOHTTP1TestServer, stop, handleChannels |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOCoreTests/CustomChannelTests.swift` | read0, triggerUserOutboundEvent0, connect0, errorCaught0, register0, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/MulticastTest.swift` | bindMulticastChannel |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NIOScheduledCallbackTests.swift` | _BaseScheduledCallbackTests, setUp |
| `.build/checkouts/swift-async-algorithms/Sources/AsyncAlgorithms/Channels/AsyncThrowingChannel.swift` | AsyncThrowingChannel, fail, send, makeAsyncIterator, finish |
| `.build/checkouts/swift-nio-extras/Sources/NIOExtras/HTTP1ProxyConnectHandler.swift` | handleHTTPEndReceived, handleHTTPBodyReceived, sendConnect, handleHTTPHeadReceived |
| `.build/checkouts/swift-nio-extras/Sources/NIOExtras/QuiescingHelper.swift` | initiateShutdown, shutdownCompleted, channelAdded, LifecycleStateMachine, channelRemoved |
| `.build/checkouts/swift-nio-extras/Sources/NIOHTTPCompression/HTTPRequestCompressor.swift` | write |
| `.build/checkouts/swift-nio-extras/Sources/NIOHTTPTypesHTTP2/HTTP2ToHTTPCodec.swift` | BaseClientCodec, processInboundData, processOutboundData, processInboundData, BaseServerCodec, ... |
| `.build/checkouts/swift-nio-extras/Sources/NIONFS3/NFSFileSystemInvoker.swift` | shutdown, NFS3FileSystemInvoker, handleNFS3Call |
| `.build/checkouts/swift-nio-extras/Sources/NIONFS3/NFSTypes+Containers.swift` | writeRPCNFS3ReplyPartially, writeRPCNFS3Call |
| `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/ConnectionStateMachine/ConnectionStateMachine.swift` | sendRstStream, receivePriority, receiveRstStream, receiveGoaway, sendWindowUpdate, ... |
| `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/ConnectionStateMachine/ConnectionStreamsState.swift` | reserveServerStreamID, forAllStreams, streamClosed, creator, dropAllStreamsWithIDHigherThan, ... |
| `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/Frame Buffers/ConcurrentStreamBuffer.swift` | streamClosed, streamCreated, nextFlushedWritableFrame, invalidateBuffer, bufferFrame, ... |
| `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/Frame Buffers/OutboundFlowControlBuffer.swift` | OutboundFlowControlBuffer, flushReceived, nextStreamToSend, streamClosed, updateWindowOfStream, ... |
| `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/Frame Buffers/OutboundFrameBuffer.swift` | processOutboundFrame |
| `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2ChannelHandler+InboundStreamMultiplexer.swift` | legacy, receivedFrame, HTTP2InboundStreamMultiplexer, inline, streamError, ... |
| `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2ChannelHandler.swift` | initialize, processOutboundFrame, uninitializedAsync, InboundStreamMultiplexerState, uninitializedLegacy, ... |
| `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2CommonInboundStreamMultiplexer.swift` | yield, requestStreamID |
| `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2FrameParser.swift` | readFrame, HTTP2FrameDecoder, append, parseHeadersFramePayload, parseOriginFramePayload, ... |
| `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2StreamChannel.swift` | StreamChannelState, activate, idle, remoteActive, localActive, ... |
| `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2StreamDelegate.swift` | NIOHTTP2StreamDelegate |
| `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2ToHTTP1Codec.swift` | BaseClientCodec, processInboundData, clearCache, processOutboundData, makeH2TrailerFramePayload, ... |
| `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/NIOHTTP2ServerConnectionManagementHandler+StateMachine.swift` | markClosed, startGracefulShutdown, receivedPingAck, streamClosed, streamOpened, ... |
| `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/NIOHTTP2ServerConnectionManagementHandler.swift` | streamCreated, HTTP2StreamDelegate, streamClosed |
| `.build/checkouts/swift-nio-http2/Sources/NIOHTTP2/StreamStateMachine.swift` | receiveHeaders, remoteInitialWindowSizeChanged, sendData, sendWindowUpdate, receiveData, ... |
| `.build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/ConfiguringPipelineAsyncMultiplexerTests.swift` | streamCreated, StreamRecorder, streamCreated, TestStreamDelegate, streamClosed, ... |
| `.build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/HTTP2InlineStreamMultiplexerTests.swift` | testInitiatedChildChannelActivates, testWritesOnCreatedChannelAreDelayed, testConnectionWindowUpdateUsesConnectionTargetWindowSize, testCreatedChildChannelCanBeClosedImmediatelyWhenBaseIsActive, testHandlersAreRemovedOnClosure, ... |
| `.build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/OutboundFlowControlBufferTests.swift` | sliceDataFrame |
| `.build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/TestUtilities.swift` | assertPushPromiseFramePayloadMatches, assertOriginFramePayloadMatches, assertSettingsFramePayloadMatches, assertPriorityFramePayloadMatches, assertPingFramePayloadMatches, ... |
| `.build/checkouts/swift-nio-ssl/Sources/NIOSSL/ByteBufferBIO.swift` | buildBoringSSLBIOMethod, boringSSLBIOReadFunc, boringSSLBIOWriteFunc, boringSSLBIOPutsFunc |
| `.build/checkouts/swift-nio-ssl/Sources/NIOSSL/CustomPrivateKey.swift` | customPrivateKeyDecrypt, customKeyDecrypt, customKeySign, customKeyComplete, customPrivateKeySign |
| `.build/checkouts/swift-nio-ssl/Sources/NIOSSL/IdentityVerification.swift` | validIdentityForService |
| `.build/checkouts/swift-nio-ssl/Sources/NIOSSL/NIOSSLHandler.swift` | write, NIOSSLHandler, doHandshakeStep, close, completeHandshake, ... |
| `.build/checkouts/swift-nio-ssl/Sources/NIOSSL/SSLCallbacks.swift` | loadContext, preparePromise |
| `.build/checkouts/swift-nio-ssl/Sources/NIOSSL/SSLConnection.swift` | extractUnconsumedData, getDataForNetwork, loadConnectionFromSSL, doShutdown, consumeDataFromNetwork, ... |
| `.build/checkouts/swift-nio-ssl/Sources/NIOSSL/SSLContext.swift` | sslContextCallback |
| `.build/checkouts/swift-nio-ssl/Sources/NIOSSL/SecurityFrameworkCertificateVerification.swift` | performSecurityFrameworkValidation |
| `.build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/NIOFilterEmptyWritesHandler.swift` | channelActive, write, errorCaught, channelInactive |
| `.build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/SocketAddress+NWEndpoint.swift` | newPort |
| `.build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/StateManagedChannel.swift` | close0 |
| `.build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/StateManagedListenerChannel.swift` | stateUpdateHandler |
| `.build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/StateManagedNWConnectionChannel.swift` | completionCallback, flush0, read0, doHalfClose0 |
| `.build/checkouts/swift-nio/Sources/NIOCore/Channel.swift` | ChannelCore |
| `.build/checkouts/swift-nio/Sources/NIOCore/ChannelPipeline.swift` | close, register |
| `.build/checkouts/swift-nio/Sources/NIOCore/DeadChannel.swift` | read0, write0, connect0, bind0, triggerUserOutboundEvent0, ... |
| `.build/checkouts/swift-nio/Sources/NIOCore/EventLoopFuture.swift` | succeed, fail, completeWith, _setValue, _resolve, ... |
| `.build/checkouts/swift-nio/Sources/NIOEmbedded/Embedded.swift` | connect0, registerAlreadyConfigured0, EmbeddedChannelCore, flush0, fail, ... |
| `.build/checkouts/swift-nio/Sources/NIOFS/FileChunks.swift` | requestedProduceMore, done, fileReadingState, didReadBytes, activeThreadPool, ... |
| `.build/checkouts/swift-nio/Sources/NIOHTTP1/HTTPDecoder.swift` | withExclusiveHTTPParser, BetterHTTPParser, didReceiveMessageBeginNotification, didReceiveURLData, didReceiveMessageCompleteNotification, ... |
| `.build/checkouts/swift-nio/Sources/NIOHTTP1/HTTPServerUpgradeHandler.swift` | channelRead, gotUpgrader |
| `.build/checkouts/swift-nio/Sources/NIOHTTP1/NIOHTTPObjectAggregator.swift` | handlingOversizeMessage, AggregatorState, ignoringContent, messageHeadReceived, receiving, ... |
| `.build/checkouts/swift-nio/Sources/NIOHTTP1/NIOTypedHTTPClientUpgraderStateMachine.swift` | unbuffer |
| `.build/checkouts/swift-nio/Sources/NIOHTTP1/NIOTypedHTTPServerUpgraderStateMachine.swift` | NIOTypedHTTPServerUpgraderStateMachine, channelReadData, inputClosed, upgradingHandlerCompleted, unbuffer, ... |
| `.build/checkouts/swift-nio/Sources/NIOPosix/BaseSocketChannel.swift` | readEOF0, badTransition |
| `.build/checkouts/swift-nio/Sources/NIOPosix/MultiThreadedEventLoopGroup.swift` | shutdownGracefully, _makePerpetualGroup, runTheLoop, next, withCurrentThreadAsEventLoop, ... |
| `.build/checkouts/swift-nio/Sources/NIOPosix/PendingDatagramWritesManager.swift` | doPendingDatagramWriteVectorOperation, triggerAppropriateWriteOperations, copySocketAddress, PendingDatagramWrite, triggerVectorBufferWrite |
| `.build/checkouts/swift-nio/Sources/NIOPosix/PendingWritesManager.swift` | closeOutbound, markFlushCheckpoint, triggerScalarBufferWrite, failAll, PendingStreamWritesManager, ... |
| `.build/checkouts/swift-nio/Sources/NIOPosix/SelectableEventLoop.swift` | cancelScheduledCallback, syncFinaliseClose |
| `.build/checkouts/swift-nio/Sources/NIOPosix/SocketChannel.swift` | join, connectSocket, leave, GroupOperation, performGroupOperation0, ... |
| `.build/checkouts/swift-nio/Sources/NIOTLS/ProtocolNegotiationHandlerStateMachine.swift` | channelRead, channelInactive, handlerRemoved, ProtocolNegotiationHandlerStateMachine, userFutureCompleted, ... |
| `.build/checkouts/swift-nio/Sources/NIOTestUtils/NIOHTTP1TestServer.swift` | handleChannels, NIOHTTP1TestServer, stop |
| `.build/checkouts/swift-nio/Sources/_NIOFileSystem/FileChunks.swift` | ProducerState, pauseProducing, performedProduceMore, requestedProduceMore, done, ... |
| `.build/checkouts/swift-nio/Tests/NIOCoreTests/CustomChannelTests.swift` | localAddress0, read0, channelRead0, bind0, write0, ... |
| `.build/checkouts/swift-nio/Tests/NIOFSIntegrationTests/FileSystemTests.swift` | testHomeDirectoryFromEnvironment |
| `.build/checkouts/swift-nio/Tests/NIOPosixTests/MulticastTest.swift` | bindMulticastChannel |
| `.build/checkouts/swift-nio/Tests/NIOPosixTests/NIOScheduledCallbackTests.swift` | setUp, _BaseScheduledCallbackTests |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/AsyncAwait/HTTPClient+execute.swift` | cancelTransaction, cancel, _cancel, TransactionCancelHandler, registerTransaction, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/AsyncAwait/Transaction+StateMachine.swift` | willExecuteRequest, StateMachine, succeedRequest, pauseRequestBodyStream, receiveResponseBodyParts, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/ChannelHandler/HTTP1ProxyConnectHandler.swift` | write, sendConnect, channelInactive, handleHTTPHeadReceived, handleHTTPEndReceived, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/ChannelHandler/SOCKSEventsHandler.swift` | userInboundEventTriggered |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/ChannelHandler/TLSEventsHandler.swift` | userInboundEventTriggered |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP1/HTTP1ClientChannelHandler.swift` | channelWritabilityChanged, writeRequestBodyPart, IdleReadStateMachine, requestEndSent, finishRequestBodyStream, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP1/HTTP1Connection.swift` | HTTP1ConnectionDelegate |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP2/HTTP2ClientRequestHandler.swift` | demandResponseBodyStream, RequestExecutor, cancelRequest, writeRequestBodyPart, finishRequestBodyStream |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP2/HTTP2Connection.swift` | http2SettingsReceived, HTTP2Connection, executeRequest0, http2GoAwayReceived, start, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP2/HTTP2IdleHandler.swift` | goAwayReceived, settingsReceived, streamClosed, closeEventReceived, streamCreated, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPConnectionPool+Factory.swift` | setupTLSInProxyConnectionIfNeeded, makePlainBootstrap |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPConnectionPool+Manager.swift` | executeRequest, connectionPoolDidShutdown, shutdown, Manager |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPConnectionPool.swift` | runUnlockedConnectionAction, cancelRequestTimeout, scheduleConnectionStartBackoffTimer, scheduleRequestTimeout, runLockedConnectionAction, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPExecutableRequest.swift` | HTTPRequestExecutor, HTTPExecutableRequest, HTTPSchedulableRequest, HTTPRequestScheduler |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPRequestStateMachine+Demand.swift` | end, ResponseStreamState, demandMoreResponseBodyParts, read, channelReadComplete, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPRequestStateMachine.swift` | channelIsWritable, demandMoreResponseBodyParts, requestStreamFinished, startRequest, requestCancelled, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+Backoff.swift` | calculateBackoff |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP1Connections.swift` | newHTTP1ConnectionEstablished, migrateToHTTP2, parkConnection, lease, createNewOverflowConnection, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP1StateMachine.swift` | migrateConnectionsAndRequestsFromHTTP2, http2ConnectionGoAwayReceived, executeRequestOnRequiredEventLoop, _newHTTP1ConnectionEstablished, http1ConnectionClosed, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP2Connections.swift` | leaseStream, HTTP2ConnectionState, closeConnectionIfIdle, hasActiveConnection, shutdown, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP2StateMachine.swift` | executeRequest, timeoutRequest, shutdown, http2ConnectionClosed, cancelRequest, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+StateMachine.swift` | http2ConnectionClosed, StateMachine, waitingForConnectivity, http2ConnectionStreamClosed, http1ConnectionReleased, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/HTTPHandler.swift` | HTTPClientTaskDelegate, ResponseAccumulator, didReceiveBodyPart, didReceiveError, didFinishRequest, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/NIOTransportServices/NWErrorHandler.swift` | translateError, errorCaught, NWErrorHandler |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/RequestBag+StateMachine.swift` | receiveResponseBodyParts, willExecuteRequest, failWithConsumptionError, fail, pauseRequestBodyStream, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/RequestBag.swift` | RequestBag, executeFailAction0, requestWasQueued0, willExecuteRequest0, fail0, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/AsyncTestHelpers.swift` | next, demand, writeBufferOrEnd |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTP1ClientChannelHandlerTests.swift` | didFinishRequest, ResponseBackpressureDelegate, didReceiveBodyPart, next, didReceiveHead |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTP1ConnectionTests.swift` | http1ConnectionClosed, http1ConnectionReleased, http1ConnectionClosed, MockHTTP1ConnectionDelegate, http1ConnectionReleased, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTP2ConnectionTests.swift` | TestHTTP2ConnectionDelegate, http2ConnectionClosed, http2ConnectionStreamClosed, http2Connection, http1ConnectionClosed, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTPClientTestUtils.swift` | didReceiveError, next, ResponseStreamDelegate, didFinishRequest, didSendRequest, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTPConnectionPool+RequestQueueTests.swift` | receiveResponseHead, receiveResponseBodyParts, fail, MockScheduledRequest, willExecuteRequest, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/Mocks/MockConnectionPool.swift` | pauseRequestBodyStream, receiveResponseBodyParts, fail, requestWasQueued, willExecuteRequest, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/Mocks/MockHTTPExecutableRequest.swift` | pauseRequestBodyStream, resumeRequestBodyStream, MockHTTPExecutableRequest, fail, calledUnimplementedMethod, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/RequestBagTests.swift` | cancelRequest, MockTaskQueuer |
| `.build/checkouts/vapor/.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/TransactionTests.swift` | fulfil, Promise, cancelRequest, demandResponseBodyStream, finishRequestBodyStream, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-async-algorithms/Sources/AsyncAlgorithms/Channels/AsyncThrowingChannel.swift` | makeAsyncIterator, AsyncThrowingChannel, finish, fail, send |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-extras/Sources/NIOExtras/HTTP1ProxyConnectHandler.swift` | handleHTTPHeadReceived, sendConnect, handleHTTPEndReceived, handleHTTPBodyReceived |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-extras/Sources/NIOExtras/QuiescingHelper.swift` | ChannelCollector, channelRemoved, channelAdded, shutdownCompleted, initiateShutdown, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-extras/Sources/NIOHTTPCompression/HTTPRequestCompressor.swift` | write |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-extras/Sources/NIOHTTPTypesHTTP2/HTTP2ToHTTPCodec.swift` | BaseClientCodec, processOutboundData, processInboundData, processInboundData, BaseServerCodec, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-extras/Sources/NIONFS3/NFSFileSystemInvoker.swift` | handleNFS3Call, NFS3FileSystemInvoker, shutdown |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-extras/Sources/NIONFS3/NFSTypes+Containers.swift` | writeRPCNFS3Call, writeRPCNFS3ReplyPartially |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/ConnectionStateMachine/ConnectionStateMachine.swift` | receiveWindowUpdate, sendPing, receiveSettingsChange, sendGoaway, sendSettings, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/ConnectionStateMachine/ConnectionStreamsState.swift` | createRemotelyPushedStream, creator, dropAllStreamsWithIDHigherThan, modifyStreamStateCreateIfNeeded, streamClosed, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/Frame Buffers/ConcurrentStreamBuffer.swift` | bufferFrame, invalidateBuffer, streamClosed, bufferFrameForNewStream, ConcurrentStreamBuffer, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/Frame Buffers/OutboundFlowControlBuffer.swift` | updateWindowOfStream, initialWindowSizeChanged, nextStreamToSend, nextFlushedWritableFrame, processOutboundFrame, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/Frame Buffers/OutboundFrameBuffer.swift` | processOutboundFrame |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2ChannelHandler+InboundStreamMultiplexer.swift` | streamCreated, legacy, streamWindowUpdated, receivedFrame, inline, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2ChannelHandler.swift` | processOutboundFrame, initialize, uninitializedAsync, InboundStreamMultiplexerState, deinitialized, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2CommonInboundStreamMultiplexer.swift` | yield, requestStreamID |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2FrameParser.swift` | nextFrame, parseSettingsFramePayload, parsePingFramePayload, parsePushPromiseFramePayload, parseRstStreamFramePayload, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2StreamChannel.swift` | StreamChannelState, completeClosing, idle, remoteActive, closed, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2StreamDelegate.swift` | NIOHTTP2StreamDelegate |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2ToHTTP1Codec.swift` | processOutboundData, BaseServerCodec, processInboundData, processOutboundData, BaseClientCodec, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/StreamStateMachine.swift` | sendWindowUpdate, receiveHeaders, localInitialWindowSizeChanged, receiveWindowUpdate, remoteInitialWindowSizeChanged, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/ConfiguringPipelineAsyncMultiplexerTests.swift` | streamCreated, streamClosed, streamClosed, StreamRecorder, TestStreamDelegate, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/HTTP2InlineStreamMultiplexerTests.swift` | testMultiplexerIgnoresFramesOnStream0, testHeadersFramesCreateNewChannels, HTTP2InlineStreamMultiplexerTests, testCreatedChildChannelCanBeClosedImmediately, testFlushingOneChannelDoesntFlushThemAll, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/OutboundFlowControlBufferTests.swift` | sliceDataFrame |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/TestUtilities.swift` | assertAlternativeServiceFramePayloadMatches, assertPriorityFramePayloadMatches, assertHeadersFramePayloadMatches, assertPushPromiseFramePayloadMatches, assertGoAwayFramePayloadMatches, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/ByteBufferBIO.swift` | boringSSLBIOWriteFunc, boringSSLBIOReadFunc, boringSSLBIOPutsFunc, buildBoringSSLBIOMethod |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/CustomPrivateKey.swift` | customPrivateKeyDecrypt, customKeySign, customKeyDecrypt, customKeyComplete, customPrivateKeySign |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/NIOSSLHandler.swift` | bufferWrite, write, channelReadComplete, scheduleTimedOutShutdown |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/SSLCallbacks.swift` | process, loadContext |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/SSLConnection.swift` | setCustomVerificationCallback, loadConnectionFromSSL, setVerificationCallback |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/SSLContext.swift` | sslContextCallback |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/SecurityFrameworkCertificateVerification.swift` | performSecurityFrameworkValidation |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/NIOFilterEmptyWritesHandler.swift` | channelActive, channelInactive, errorCaught, write |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/SocketAddress+NWEndpoint.swift` | newPort |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/StateManagedChannel.swift` | close0 |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/StateManagedListenerChannel.swift` | stateUpdateHandler |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/StateManagedNWConnectionChannel.swift` | doHalfClose0, completionCallback, stateUpdateHandler, read0, flush0 |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOCore/Channel.swift` | ChannelCore |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOCore/ChannelPipeline.swift` | connect, register, flush |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOCore/DeadChannel.swift` | errorCaught0, DeadChannelCore, triggerUserOutboundEvent0, channelRead0, read0, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOCore/EventLoopFuture.swift` | EventLoopPromise, succeed, fail, completeWith, makeUnleakablePromise, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOEmbedded/Embedded.swift` | checkCorrectThread, errorCaught0, flush0, remoteAddress0, registerAlreadyConfigured0, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOFileSystem/FileChunks.swift` | requestedProduceMore, fileReadingState, didReadBytes, done, ProducerState, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/HTTPDecoder.swift` | withExclusiveHTTPParser, didReceiveChunkHeaderNotification, didReceiveURLData, validateHeaderLength, finish, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/HTTPServerUpgradeHandler.swift` | channelRead, gotUpgrader |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/NIOHTTPObjectAggregator.swift` | ignoringContent, handlingOversizeMessage, idle, messageBodyReceived, messageEndReceived, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/NIOTypedHTTPClientUpgraderStateMachine.swift` | unbuffer |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/NIOTypedHTTPServerUpgraderStateMachine.swift` | NIOTypedHTTPServerUpgraderStateMachine, handlerRemoved, upgradingHandlerCompleted, channelReadRequestPart, channelReadData, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/BaseSocketChannel.swift` | badTransition, readEOF0 |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/MultiThreadedEventLoopGroup.swift` | setupThreadAndEventLoop, MultiThreadedEventLoopGroup, withCurrentThreadAsEventLoop, shutdownGracefully, makeIterator, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/PendingDatagramWritesManager.swift` | PendingDatagramWrite, doPendingDatagramWriteVectorOperation, triggerVectorBufferWrite, copySocketAddress |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/PendingWritesManager.swift` | triggerScalarBufferWrite |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/SelectableChannel.swift` | SelectableChannel |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/SelectableEventLoop.swift` | syncFinaliseClose, cancelScheduledCallback |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOPosix/SocketChannel.swift` | optionName, performGroupOperation0, connectSocket, leave, join, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOTLS/ProtocolNegotiationHandlerStateMachine.swift` | handlerRemoved, channelInactive, channelRead, unbuffer, userFutureCompleted, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Sources/NIOTestUtils/NIOHTTP1TestServer.swift` | handleChannels, stop, NIOHTTP1TestServer |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOCoreTests/CustomChannelTests.swift` | localAddress0, bind0, remoteAddress0, read0, channelRead0, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/MulticastTest.swift` | bindMulticastChannel |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NIOScheduledCallbackTests.swift` | setUp, _BaseScheduledCallbackTests |
| `.build/checkouts/vapor/.build/index-build/checkouts/websocket-kit/Sources/WebSocketKit/WebSocket.swift` | handle |
| `.build/checkouts/vapor/Sources/Vapor/Concurrency/RequestBody+Concurrency.swift` | produceMore0, registerBackpressurePromise, checkBodyStorage |
| `.build/checkouts/vapor/Sources/Vapor/HTTP/Server/HTTPServerRequestDecoder.swift` | didWrite, didReadBytes, didError, illegalTransition, HTTPBodyStreamState, ... |
| `.build/checkouts/vapor/Tests/VaporTests/ServerTests.swift` | testDeprecatedServerStartMethods |
| `.build/checkouts/websocket-kit/Sources/WebSocketKit/WebSocket.swift` | handle |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/AsyncAwait/HTTPClient+execute.swift` | _registerTransaction, TransactionCancelHandler, cancelTransaction, cancel, _cancel, ... |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/AsyncAwait/Transaction+StateMachine.swift` | StateMachine, willExecuteRequest, requestWasQueued, receiveResponseEnd, writeNextRequestPart, ... |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/ChannelHandler/HTTP1ProxyConnectHandler.swift` | handleHTTPBodyReceived, write, sendConnect, handleHTTPEndReceived, handleHTTPHeadReceived, ... |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/ChannelHandler/SOCKSEventsHandler.swift` | userInboundEventTriggered |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/ChannelHandler/TLSEventsHandler.swift` | userInboundEventTriggered |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP1/HTTP1ClientChannelHandler.swift` | writeRequestBodyPart, requestEndSent, demandResponseBodyStream, IdleReadStateMachine, RequestExecutor, ... |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP1/HTTP1Connection.swift` | HTTP1ConnectionDelegate |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP2/HTTP2ClientRequestHandler.swift` | writeRequestBodyPart, finishRequestBodyStream, cancelRequest, demandResponseBodyStream, RequestExecutor |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP2/HTTP2Connection.swift` | shutdown0, http2SettingsReceived, start, HTTP2ConnectionDelegate, http2GoAwayReceived, ... |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTP2/HTTP2IdleHandler.swift` | goAwayReceived, StateMachine, streamCreated, streamClosed, closeEventReceived, ... |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPConnectionPool+Factory.swift` | makePlainBootstrap, setupTLSInProxyConnectionIfNeeded |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPConnectionPool+Manager.swift` | shutdown, connectionPoolDidShutdown, Manager, executeRequest |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPConnectionPool.swift` | runUnlockedActions, cancelIdleTimerForConnection, executeRequest, scheduleConnectionStartBackoffTimer, scheduleRequestTimeout, ... |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPExecutableRequest.swift` | HTTPRequestScheduler, HTTPRequestExecutor, HTTPSchedulableRequest, HTTPExecutableRequest |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPRequestStateMachine+Demand.swift` | demandMoreResponseBodyParts, receivedBodyPart, ResponseStreamState, read, end, ... |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/HTTPRequestStateMachine.swift` | channelReadComplete, channelInactive, requestStreamPartReceived, channelRead, demandMoreResponseBodyParts, ... |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+Backoff.swift` | calculateBackoff |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP1Connections.swift` | connected, lease, HTTP1Connections, failConnection, releaseConnection, ... |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP1StateMachine.swift` | http1ConnectionReleased, nextActionForToBeClosedIdleConnection, shutdown, migrateConnectionsAndRequestsFromHTTP2, cancelRequest, ... |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP2Connections.swift` | migrateToHTTP1, backoffNextConnectionAttempt, close, failConnection, fail, ... |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+HTTP2StateMachine.swift` | newHTTP2ConnectionEstablished, timeoutRequest, HTTP2StateMachine, connectionCreationBackoffDone, connectionIdleTimeout, ... |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/ConnectionPool/State Machine/HTTPConnectionPool+StateMachine.swift` | http1ConnectionReleased, executeRequest, timeoutRequest, connectionCreationBackoffDone, newHTTP2ConnectionCreated, ... |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/HTTPHandler.swift` | didVisitURL, didReceiveError, didFinishRequest, ResponseAccumulator, didReceiveHead, ... |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/NIOTransportServices/NWErrorHandler.swift` | errorCaught, translateError, NWErrorHandler |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/RequestBag+StateMachine.swift` | willExecuteRequest, finishRequestBodyStream, resumeRequestBodyStream, receiveResponseEnd, receiveResponseBodyParts, ... |
| `.build/index-build/checkouts/async-http-client/Sources/AsyncHTTPClient/RequestBag.swift` | willExecuteRequest0, fail0, requestWasQueued0, deadlineExceeded0, receiveResponseEnd0, ... |
| `.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/AsyncTestHelpers.swift` | next, demand, writeBufferOrEnd |
| `.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTP1ClientChannelHandlerTests.swift` | next, didReceiveBodyPart, didFinishRequest, ResponseBackpressureDelegate, didReceiveHead |
| `.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTP1ConnectionTests.swift` | http1ConnectionReleased, http1ConnectionReleased, http1ConnectionClosed, MockConnectionDelegate, http1ConnectionClosed, ... |
| `.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTP2ConnectionTests.swift` | EmptyHTTP1ConnectionDelegate, EmptyHTTP2ConnectionDelegate, http2ConnectionClosed, http2ConnectionClosed, http2ConnectionCreated, ... |
| `.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTPClientTestUtils.swift` | didSendRequest, didFinishRequest, didSendRequestHead, didSendRequestPart, next, ... |
| `.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/HTTPConnectionPool+RequestQueueTests.swift` | receiveResponseEnd, pauseRequestBodyStream, requestBodyStreamSent, receiveResponseHead, willExecuteRequest, ... |
| `.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/Mocks/MockConnectionPool.swift` | pauseRequestBodyStream, receiveResponseEnd, receiveResponseBodyParts, resumeRequestBodyStream, MockHTTPScheduableRequest, ... |
| `.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/Mocks/MockHTTPExecutableRequest.swift` | calledUnimplementedMethod, receiveResponseHead, willExecuteRequest, requestHeadSent, receiveResponseBodyParts, ... |
| `.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/RequestBagTests.swift` | MockTaskQueuer, cancelRequest |
| `.build/index-build/checkouts/async-http-client/Tests/AsyncHTTPClientTests/TransactionTests.swift` | fulfil, cancelRequest, finishRequestBodyStream, Promise, Executor, ... |
| `.build/index-build/checkouts/swift-async-algorithms/Sources/AsyncAlgorithms/Channels/AsyncThrowingChannel.swift` | AsyncThrowingChannel, fail, send, finish, makeAsyncIterator |
| `.build/index-build/checkouts/swift-nio-extras/Sources/NIOExtras/HTTP1ProxyConnectHandler.swift` | handleHTTPBodyReceived, handleHTTPHeadReceived, handleHTTPEndReceived, sendConnect |
| `.build/index-build/checkouts/swift-nio-extras/Sources/NIOExtras/QuiescingHelper.swift` | LifecycleStateMachine, shutdownCompleted, channelAdded, initiateShutdown, channelRemoved |
| `.build/index-build/checkouts/swift-nio-extras/Sources/NIOHTTPCompression/HTTPRequestCompressor.swift` | write |
| `.build/index-build/checkouts/swift-nio-extras/Sources/NIOHTTPTypesHTTP2/HTTP2ToHTTPCodec.swift` | processInboundData, BaseServerCodec, processOutboundData, processInboundData, BaseClientCodec, ... |
| `.build/index-build/checkouts/swift-nio-extras/Sources/NIONFS3/NFSFileSystemInvoker.swift` | handleNFS3Call, shutdown, NFS3FileSystemInvoker |
| `.build/index-build/checkouts/swift-nio-extras/Sources/NIONFS3/NFSTypes+Containers.swift` | writeRPCNFS3Call, writeRPCNFS3ReplyPartially |
| `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/ConnectionStateMachine/ConnectionStateMachine.swift` | receiveHeaders, sendRstStream, receivePing, receivePushPromise, sendGoaway, ... |
| `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/ConnectionStateMachine/ConnectionStreamsState.swift` | ConnectionStreamState, reserveServerStreamID, createRemotelyPushedStream, dropAllStreamsWithIDHigherThan, reserveClientStreamID, ... |
| `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/Frame Buffers/ConcurrentStreamBuffer.swift` | nextFlushedWritableFrame, streamCreated, processOutboundFrame, flushReceived, bufferFrameForNewStream, ... |
| `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/Frame Buffers/OutboundFlowControlBuffer.swift` | invalidateBuffer, streamClosed, nextStreamToSend, streamCreated, initialWindowSizeChanged, ... |
| `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/Frame Buffers/OutboundFrameBuffer.swift` | processOutboundFrame |
| `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2ChannelHandler+InboundStreamMultiplexer.swift` | initialStreamWindowChanged, streamError, InboundStreamMultiplexer, streamWindowUpdated, streamCreated, ... |
| `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2ChannelHandler.swift` | initialized, uninitializedLegacy, uninitializedInline, initialize, deinitialized, ... |
| `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2CommonInboundStreamMultiplexer.swift` | requestStreamID, yield |
| `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2FrameParser.swift` | parseAltSvcFramePayload, parseSettingsFramePayload, parseGoAwayFramePayload, append, readFrame, ... |
| `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2StreamChannel.swift` | closingNeverActivated, StreamChannelState, localActive, remoteActive, activate, ... |
| `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2StreamDelegate.swift` | NIOHTTP2StreamDelegate |
| `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/HTTP2ToHTTP1Codec.swift` | processOutboundData, makeH2TrailerFramePayload, clearCache, processOutboundData, processInboundData, ... |
| `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/NIOHTTP2ServerConnectionManagementHandler+StateMachine.swift` | StateMachine, streamClosed, streamOpened, startGracefulShutdown, receivedPingAck, ... |
| `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/NIOHTTP2ServerConnectionManagementHandler.swift` | streamClosed, HTTP2StreamDelegate, streamCreated |
| `.build/index-build/checkouts/swift-nio-http2/Sources/NIOHTTP2/StreamStateMachine.swift` | remoteInitialWindowSizeChanged, localInitialWindowSizeChanged, sendData, receiveHeaders, sendWindowUpdate, ... |
| `.build/index-build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/ConfiguringPipelineAsyncMultiplexerTests.swift` | TestStreamDelegate, streamClosed, streamCreated, streamCreated, StreamRecorder, ... |
| `.build/index-build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/HTTP2InlineStreamMultiplexerTests.swift` | testStreamChannelSupportsSyncOptions, CountingStreamDelegate, testMultiplexerDoesntFireReadCompleteForEachFrame, testMultiplexerIgnoresPriorityFrames, testDelegateReceivesOutboundCreationAndCloseNotifications, ... |
| `.build/index-build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/OutboundFlowControlBufferTests.swift` | sliceDataFrame |
| `.build/index-build/checkouts/swift-nio-http2/Tests/NIOHTTP2Tests/TestUtilities.swift` | assertOriginFramePayloadMatches, assertPushPromiseFramePayloadMatches, assertPriorityFramePayloadMatches, assertAlternativeServiceFramePayloadMatches, assertHeadersFramePayloadMatches, ... |
| `.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/ByteBufferBIO.swift` | boringSSLBIOPutsFunc, buildBoringSSLBIOMethod, boringSSLBIOWriteFunc, boringSSLBIOReadFunc |
| `.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/CustomPrivateKey.swift` | customPrivateKeySign, customKeySign, customKeyDecrypt, customPrivateKeyDecrypt, customKeyComplete |
| `.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/IdentityVerification.swift` | validIdentityForService |
| `.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/NIOSSLHandler.swift` | flush, doDecodeData, channelRead, handlerRemoved, channelClose, ... |
| `.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/SSLCallbacks.swift` | loadContext, preparePromise |
| `.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/SSLConnection.swift` | validateHostname, getPeerCertificate, setConnectState, loadConnectionFromSSL, writeDataToNetwork, ... |
| `.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/SSLContext.swift` | sslContextCallback |
| `.build/index-build/checkouts/swift-nio-ssl/Sources/NIOSSL/SecurityFrameworkCertificateVerification.swift` | performSecurityFrameworkValidation |
| `.build/index-build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/NIOFilterEmptyWritesHandler.swift` | write, channelActive, errorCaught, channelInactive |
| `.build/index-build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/SocketAddress+NWEndpoint.swift` | newPort |
| `.build/index-build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/StateManagedChannel.swift` | close0 |
| `.build/index-build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/StateManagedListenerChannel.swift` | stateUpdateHandler |
| `.build/index-build/checkouts/swift-nio-transport-services/Sources/NIOTransportServices/StateManagedNWConnectionChannel.swift` | completionCallback, doHalfClose0, flush0, read0 |
| `.build/index-build/checkouts/swift-nio/Sources/NIOCore/Channel.swift` | ChannelCore |
| `.build/index-build/checkouts/swift-nio/Sources/NIOCore/ChannelPipeline.swift` | _handlerSync, bind, connect, handler, register, ... |
| `.build/index-build/checkouts/swift-nio/Sources/NIOCore/Codec.swift` | handlerAdded, channelRead |
| `.build/index-build/checkouts/swift-nio/Sources/NIOCore/DeadChannel.swift` | triggerUserOutboundEvent0, registerAlreadyConfigured0, connect0, bind0, register0, ... |
| `.build/index-build/checkouts/swift-nio/Sources/NIOCore/EventLoopFuture.swift` | _resolve, fail, _setValue, makeUnleakablePromise, preconditionFailure, ... |
| `.build/index-build/checkouts/swift-nio/Sources/NIOCore/GlobalSingletons.swift` | getTrustworthyThreadCount |
| `.build/index-build/checkouts/swift-nio/Sources/NIOCore/Linux.swift` | readLines, countCoreIds |
| `.build/index-build/checkouts/swift-nio/Sources/NIOCore/NIOScheduledCallback.swift` | cancelScheduledCallback |
| `.build/index-build/checkouts/swift-nio/Sources/NIOCore/TypeAssistedChannelHandler.swift` | unwrapOutboundIn |
| `.build/index-build/checkouts/swift-nio/Sources/NIOCore/Utilities.swift` | getenv |
| `.build/index-build/checkouts/swift-nio/Sources/NIOEmbedded/Embedded.swift` | EmbeddedScheduledTask, printError, _enqueueInboundBufferConsumer, addToBuffer, remoteAddress0, ... |
| `.build/index-build/checkouts/swift-nio/Sources/NIOFS/FileChunks.swift` | activeThreadPool, fileReadingState, pauseProducing, didReadBytes, requestedProduceMore, ... |
| `.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/HTTPDecoder.swift` | didReceiveBodyData, didReceiveMessageCompleteNotification, didReceiveChunkCompleteNotification, finish, BetterHTTPParser, ... |
| `.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/HTTPServerUpgradeHandler.swift` | gotUpgrader, channelRead |
| `.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/NIOHTTPObjectAggregator.swift` | AggregatorState, idle, messageEndReceived, messageBodyReceived, closed, ... |
| `.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/NIOTypedHTTPClientUpgraderStateMachine.swift` | unbuffer |
| `.build/index-build/checkouts/swift-nio/Sources/NIOHTTP1/NIOTypedHTTPServerUpgraderStateMachine.swift` | findingUpgraderCompleted, channelReadData, inputClosed, handlerRemoved, unbuffer, ... |
| `.build/index-build/checkouts/swift-nio/Sources/NIOPosix/BaseSocketChannel.swift` | triggerUserOutboundEvent0, connectSocket, unregisterForWritable, flushNow, deregister, ... |
| `.build/index-build/checkouts/swift-nio/Sources/NIOPosix/MultiThreadedEventLoopGroup.swift` | runTheLoop, anySEL, shutdownGracefully, clearLoopThreadLocalReference, makeIterator, ... |
| `.build/index-build/checkouts/swift-nio/Sources/NIOPosix/NonBlockingFileIO.swift` | read0 |
| `.build/index-build/checkouts/swift-nio/Sources/NIOPosix/PendingDatagramWritesManager.swift` | doPendingDatagramWriteVectorOperation, triggerVectorBufferWrite, copySocketAddress, PendingDatagramWrite, triggerAppropriateWriteOperations |
| `.build/index-build/checkouts/swift-nio/Sources/NIOPosix/PendingWritesManager.swift` | doPendingWriteVectorOperation, PendingStreamWritesManager, failAll, closeOutbound, didWrite, ... |
| `.build/index-build/checkouts/swift-nio/Sources/NIOPosix/SelectableEventLoop.swift` | syncFinaliseClose, cancelScheduledCallback |
| `.build/index-build/checkouts/swift-nio/Sources/NIOPosix/SocketChannel.swift` | connectSocket, optionName, join, GroupOperation, leave, ... |
| `.build/index-build/checkouts/swift-nio/Sources/NIOTLS/ProtocolNegotiationHandlerStateMachine.swift` | channelInactive, userInboundEventTriggered, userFutureCompleted, unbuffer, ProtocolNegotiationHandlerStateMachine, ... |
| `.build/index-build/checkouts/swift-nio/Sources/NIOTestUtils/NIOHTTP1TestServer.swift` | handleChannels, NIOHTTP1TestServer, stop |
| `.build/index-build/checkouts/swift-nio/Sources/_NIOFileSystem/FileChunks.swift` | ProducerState, didReadBytes, pauseProducing, done, performedProduceMore, ... |
| `.build/index-build/checkouts/swift-nio/Tests/NIOCoreTests/CustomChannelTests.swift` | registerAlreadyConfigured0, channelRead0, flush0, register0, read0, ... |
| `.build/index-build/checkouts/swift-nio/Tests/NIOFSIntegrationTests/FileSystemTests.swift` | testHomeDirectoryFromEnvironment |
| `.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/MulticastTest.swift` | bindMulticastChannel |
| `.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NIOScheduledCallbackTests.swift` | _BaseScheduledCallbackTests, setUp |
| `.build/index-build/checkouts/vapor/Sources/Vapor/Concurrency/RequestBody+Concurrency.swift` | checkBodyStorage, registerBackpressurePromise, produceMore0 |
| `.build/index-build/checkouts/vapor/Sources/Vapor/HTTP/Server/HTTPServerRequestDecoder.swift` | didError, didReadBytes, didWrite, didEnd, illegalTransition, ... |
| `.build/index-build/checkouts/vapor/Tests/VaporTests/ServerTests.swift` | testDeprecatedServerStartMethods |
| `.build/index-build/checkouts/websocket-kit/Sources/WebSocketKit/WebSocket.swift` | handle |

## Connected Communities

- **Sources/NIOWebSocket +12 dirs** (1 cross-edges)

## How to Explore

```
get_communities with id: "community-16712"
smart_context with task: "understand Sources/NIOHTTP2 +111 dirs", format: "gcx"
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
