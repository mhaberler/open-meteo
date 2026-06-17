---
name: gortex-tests-nioposixtests-xctassertnothrow-acceptbackoffhandlertest-asyncchannelbootstraptests-819-1
description: "Work in the Tests/NIOPosixTests · XCTAssertNoThrow · AcceptBackoffHandlerTest · AsyncChannelBootstrapTests (819) #1 area — 819 symbols across 42 files (99% cohesion)"
---

# Tests/NIOPosixTests · XCTAssertNoThrow · AcceptBackoffHandlerTest · AsyncChannelBootstrapTests (819) #1

819 symbols | 42 files | 99% cohesion

## When to Use

Use this skill when working on files in:
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/AcceptBackoffHandlerTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/AsyncChannelBootstrapTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/BlockingIOThreadPoolTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/BootstrapTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/ChannelNotificationTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/ChannelPipelineTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/ChannelTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/CodecTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/DatagramChannelTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/EchoServerClientTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/EventLoopFutureTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/EventLoopTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/FileRegionTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/GetAddrInfoResolverTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/HappyEyeballsTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/IPv4Header.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/IdleStateHandlerTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/MulticastTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NIOFileHandleTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NIOLoopBoundTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NIOScheduledCallbackTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NIOThreadPoolTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NonBlockingFileIOTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/PendingDatagramWritesManagerTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/PipeChannelTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/RawSocketBootstrapTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SALChannelTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SALEventLoopTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SelectorTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SerialExecutorTests.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SocketAddressTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SocketChannelTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SocketOptionProviderTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/StreamChannelsTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SyscallAbstractionLayer.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SyscallAbstractionLayerContext.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SystemTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/TestUtils.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/ThreadTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/UniversalBootstrapSupportTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/VsockAddressTest.swift`
- `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/XCTest+AsyncAwait.swift`

## Key Files

| File | Symbols |
|------|---------|
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/AcceptBackoffHandlerTest.swift` | testENFILE, testSecondErrorUpdateScheduledRead, testRemovalTriggerReadWhenPreviousReadScheduled, testECONNABORTED, testNotScheduleReadIfAlreadyScheduled, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/AsyncChannelBootstrapTests.swift` | testDatagramBootstrap_connectFails, channelRead, tearDown, IPHeaderRemoverHandler, testClientBootstrap_connectFails |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/BlockingIOThreadPoolTest.swift` | BlockingIOThreadPoolTest, testLoseLastReferenceAndShutdownWhileTaskStillRunning, testDeadLockIfCalledOutWithLockHeld, testStateCancelled, testStateActive, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/BootstrapTest.swift` | testBootstrapsCallInitializersOnCorrectEventLoop, testPipeBootstrapInEventLoop, testPipeBootstrapSetsChannelOptionsBeforeChannelInitializer, testReleaseFileHandleOnOwningFailure, MakeSureAutoReadIsOffInChannelInitializer, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/ChannelNotificationTest.swift` | testActiveBeforeChannelRead, testNotificationOrder, ChannelNotificationTest |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/ChannelPipelineTest.swift` | testRemoveHeadOrTail, testSynchronousViewAddHandler, workaroundSR9815withAUselessFunction, testFiringChannelReadsInHandlerRemovedWorks, assertWriteIndexOrder, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/ChannelTests.swift` | runTest, testWeDontCrashIfChannelReleasesBeforePipeline, testPendingWritesMoreThanWritevIOVectorLimit, veryNasty_blockUntilReadBufferIsNonEmpty, testCloseInput, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/CodecTest.swift` | testDecodeLastIsInvokedOnceEvenIfNothingEverArrivedOnChannelHalfClosure, testMemoryIsReclaimedIfMostIsConsumed, testMemoryIsReclaimedIfLotsIsAvailable, testRemoveHandlerBecauseOfChannelTearDownWhilstUserTriggeredRemovalIsInProgress, testErrorInDecodeLastWhenCloseIsReceivedReentrantlyInDecode, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/DatagramChannelTests.swift` | testReceiveEcnAndPacketInfoIPV4VectorRead, testSetGROOption, testReceiveLargeBufferWithGRO, testManyManyDatagramWrites, testReconnectingSocketFailsBufferedWrites, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/EchoServerClientTest.swift` | testEcho, testConnectUnixDomainSocket, testPendingReadProcessedAfterWriteError, testEchoUnixDomainSocket, testWriteOnAccept, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/EventLoopFutureTest.swift` | testFoldWithSuccessAndAllSuccesses, testAlwaysWithFailingPromise, testflatMapErrorThrowingWhichDoesThrow, testWhenCompleteBlockingSuccess, testFoldWithFailureAndAllUnfulfilled, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/EventLoopTest.swift` | testEventLoopGroupProvider, testShuttingDownFailsRegistration, testMultiThreadedEventLoopGroupDescription, testEdgeCasesNIODeadlinePlusTimeAmount, testEventLoopsWithoutPreSucceededFuturesDoNotCacheThem, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/FileRegionTest.swift` | testWriteFileRegion, testWriteEmptyFileRegionDoesNotHang, testOutstandingFileRegionsWork |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/GetAddrInfoResolverTest.swift` | GetaddrinfoResolverTest, testResolveNoDuplicatesV4, testResolveNoDuplicatesV6 |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/HappyEyeballsTest.swift` | testResolverOnDifferentEventLoop |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/IPv4Header.swift` | writeIPv4HeaderToBSDRawSocket, writeIPv4Header, isValidChecksum, setChecksum, computeChecksum |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/IdleStateHandlerTest.swift` | testIdleWrite, testIdleAllRead, testIdle, IdleStateHandlerTest, testIdleRead, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/MulticastTest.swift` | testCanLeaveAnIPv6MulticastGroupWithDevice, assertDatagramDoesNotReach, configureSenderMulticastIf, setUp, testCanLeaveAnIPv6MulticastGroup, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NIOFileHandleTest.swift` | testOpenCloseWorks, NIOFileHandleTest, makePipe, testCloseVsUseRace, testCloseStorm |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NIOLoopBoundTests.swift` | setUp, testLoopBoundBoxCanBeInitialisedWithNilOffLoopAndLaterSetToValue, sendableBlackhole, testLoopBoundIsSendableWithNonSendableValue, NIOLoopBoundTests, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NIOScheduledCallbackTests.swift` | assert |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NIOThreadPoolTest.swift` | testAsyncShutdownWorks, testThreadNamesAreSetUp, NIOThreadPoolTest, testThreadPoolStartsMultipleTimes, testAsyncThreadPoolNotActiveError, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NonBlockingFileIOTest.swift` | testFileRegionReadFromPipeFails, testRename, testAsyncGettingErrorWhenThreadPoolIsShutdown, testLStat, testCreateDirectory, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/PendingDatagramWritesManagerTests.swift` | withPendingDatagramWritesManager, testPendingWritesNoMoreThanWritevLimitIsWrittenInOneMassiveChunk, testPendingWritesWorkWithPartialWrites, testPendingWritesCloseDuringVectorWrite, PendingDatagramWritesManagerTests, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/PipeChannelTest.swift` | PipeChannelTest, testWeDontAcceptRegularFiles, setUp, testWriteErrorsCloseChannel, testBasicIO, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/RawSocketBootstrapTests.swift` | RawSocketBootstrapTests, testConnect, testBindWithRecevMmsg, testIpHdrincl, XCTSkipIfUserHasNotEnoughRightsForRawSocketAPI |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SALChannelTests.swift` | testWriteBeforeChannelActiveClientStreamInstantConnect_shortWriteLeadsToWritable_instantClose, testWriteBeforeChannelActiveServerStream_shortWriteLeadsToWritable_instantClose, testWritesFromWritabilityNotificationsDoNotGetLostIfWePreviouslyWroteEverything, testWriteBeforeChannelActiveClientStreamDelayedConnect, testWriteBeforeChannelActiveClientStreamInstantConnect, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SALEventLoopTests.swift` | SALEventLoopTests, testSchedulingTaskOnSleepingLoopWakesUpOnce |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SelectorTest.swift` | testWeDoNotDeliverEventsForPreviouslyClosedChannels, testDeregisterWhileProcessingEvents, SelectorTest, workaroundSR9815, assertDeregisterWhileProcessingEvents, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SerialExecutorTests.swift` | tearDown |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SocketAddressTest.swift` | testCanCreateIPv6MaskFromPrefix, testHashUnequalAddressesOnPort, testRejectsWrongIPByteBufferLength, testCanCreateIPv4AddressFromString, SocketAddressTest, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SocketChannelTest.swift` | testWriteServerSocketChannel, testSocketFlagNONBLOCKWorks, testAcceptFailsWithENFILE, testConnect, testUnprocessedOutboundUserEventFailsOnServerSocketChannel, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SocketOptionProviderTest.swift` | testSoIpMulticastIf, testIPv6MulticastLoop, testIpMulticastTtl, testTCPInfo, tearDown, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/StreamChannelsTest.swift` | testCloseInReEntrantFlushNowCall, writeOneMore, testHalfCloseOwnOutputWithPopulatedBuffer, testHalfCloseAfterEOF, testSyncChannelOptions, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SyscallAbstractionLayer.swift` | salWait, read |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SyscallAbstractionLayerContext.swift` | withSALContext |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SystemTest.swift` | testErrorsWorkCorrectly |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/TestUtils.swift` | getBoolSocketOption, withCrossConnectedPipeChannels, withPipe, forEachCrossConnectedStreamChannelPair, printSocketAddress, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/ThreadTest.swift` | ThreadTest, testThreadSpecificDoesNotLeakWhenOutOfScopeButThreadStillRunning, testThreadSpecificDoesNotLeakIfThreadExitsAfterUnset, testThreadSpecificsAreNilWhenNotPresent, testCurrentThreadWorks, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/UniversalBootstrapSupportTest.swift` | testBootstrapOverrideOfShortcutOptions, UniversalBootstrapSupportTest, testBootstrappingWorks |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/VsockAddressTest.swift` | testDescriptionWorks, testInitializeFromIntegerLiteral, testGetLocalCID, VsockAddressTest, testInitializeFromInt, ... |
| `.build/checkouts/vapor/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/XCTest+AsyncAwait.swift` | XCTAssertThrowsError, XCTAssertNoThrow |

## Connected Communities

- **Tests/NIOPosixTests · withTemporaryFile · FileRegionTest · NonBlockingFileIOTest (62) #3** (9 cross-edges)
- **Tests/NIOPosixTests · withTemporaryDirectory · NonBlockingFileIOTest · TestUtils** (5 cross-edges)
- **Sources/NIOHTTP2 +111 dirs** (2 cross-edges)

## How to Explore

```
get_communities with id: "community-11007"
smart_context with task: "understand Tests/NIOPosixTests · XCTAssertNoThrow · AcceptBackoffHandlerTest · AsyncChannelBootstrapTests (819) #1", format: "gcx"
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
