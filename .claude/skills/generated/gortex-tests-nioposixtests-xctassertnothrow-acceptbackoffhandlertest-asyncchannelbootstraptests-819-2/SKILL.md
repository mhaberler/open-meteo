---
name: gortex-tests-nioposixtests-xctassertnothrow-acceptbackoffhandlertest-asyncchannelbootstraptests-819-2
description: "Work in the Tests/NIOPosixTests · XCTAssertNoThrow · AcceptBackoffHandlerTest · AsyncChannelBootstrapTests (819) #2 area — 819 symbols across 41 files (99% cohesion)"
---

# Tests/NIOPosixTests · XCTAssertNoThrow · AcceptBackoffHandlerTest · AsyncChannelBootstrapTests (819) #2

819 symbols | 41 files | 99% cohesion

## When to Use

Use this skill when working on files in:
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/AcceptBackoffHandlerTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/AsyncChannelBootstrapTests.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/BlockingIOThreadPoolTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/BootstrapTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/ChannelNotificationTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/ChannelPipelineTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/ChannelTests.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/CodecTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/DatagramChannelTests.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/EchoServerClientTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/EventLoopFutureTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/EventLoopTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/FileRegionTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/GetAddrInfoResolverTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/HappyEyeballsTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/IPv4Header.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/IdleStateHandlerTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/MulticastTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NIOFileHandleTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NIOLoopBoundTests.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NIOThreadPoolTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NonBlockingFileIOTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/PendingDatagramWritesManagerTests.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/PipeChannelTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/RawSocketBootstrapTests.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SALChannelTests.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SALEventLoopTests.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SelectorTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SerialExecutorTests.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SocketAddressTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SocketChannelTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SocketOptionProviderTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/StreamChannelsTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SyscallAbstractionLayer.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SyscallAbstractionLayerContext.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SystemTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/TestUtils.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/ThreadTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/UniversalBootstrapSupportTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/VsockAddressTest.swift`
- `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/XCTest+AsyncAwait.swift`

## Key Files

| File | Symbols |
|------|---------|
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/AcceptBackoffHandlerTest.swift` | defaultBackoffProvider, testSecondErrorUpdateScheduledRead, testENOMEM, testChannelInactiveCancelScheduled, testENFILE, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/AsyncChannelBootstrapTests.swift` | tearDown, IPHeaderRemoverHandler, channelRead, testClientBootstrap_connectFails, testDatagramBootstrap_connectFails |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/BlockingIOThreadPoolTest.swift` | testPoolDoesGetReleasedWhenStoppedAndReferencedDropped, testStateActive, testClosureReferencesDroppedAfterTwoConsecutiveWorkItemsExecution, BlockingIOThreadPoolTest, testClosureReferenceDroppedAfterSingleWorkItemExecution, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/BootstrapTest.swift` | testClientBootstrapSetsChannelOptionsBeforeChannelInitializer, workaround, testNIOPipeBootstrapValidatesWorkingELGsCorrectly, testDatagramBootstrapSetsChannelOptionsBeforeChannelInitializer, testNoDoubleAddOnPipeBootstrapTakingOwnership_inputOutputSeparate, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/ChannelNotificationTest.swift` | testNotificationOrder, ChannelNotificationTest, testActiveBeforeChannelRead |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/ChannelPipelineTest.swift` | testTeardownDuringFormalRemovalProcess, testGetNotAddedHandler, testChannelInfrastructureIsNotLeaked, testSynchronousViewGetTypedHandler, testAddBeforeWhileClosedForSynchronousPosition, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/ChannelTests.swift` | testInputAndOutputClosedResultsInFullClosure, testCloseInUnregister, testSpecificConnectTimeout, testPendingWritesSpinCountWorksForVectorWrites, testSocketErroringSynchronouslyCorrectlyTearsTheChannelDown, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/CodecTest.swift` | testTrivialDecoderDoesSensibleStuffWhenCloseInRead, testDecodeLoopStopsOnChannelInactive, testDecoderReentranceChannelRead, testRemoveHandlerBecauseOfChannelTearDownWhilstUserTriggeredRemovalIsInProgress, testDecoder, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/DatagramChannelTests.swift` | testSetGetPktInfoOption, testWriteBufferAboveGSOSegmentCountLimitShouldError, testWritesAreAccountedCorrectly, testRecvMmsgForMultipleCycles, testEcnSendReceiveIPV4VectorRead, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/EchoServerClientTest.swift` | testChannelErrorEOFNotFiredThroughPipeline, testWriteOnAccept, testPendingReadProcessedAfterWriteError, testEchoVsock, testConnectUnixDomainSocket, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/EventLoopFutureTest.swift` | testAndAllWithEmptyFutureList, testFoldWithFailureAndAllUnfulfilled, testAndAllWithOneFailure, testAssertFailure, testFoldWithMultipleEventLoops, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/EventLoopTest.swift` | testScheduledTasksAreOrdered, testMakeCompletedFutureWithResultOf, testFailingFlatSubmit, testRepeatedTaskThatCancelsItselfNotifiesOnlyWhenFinished, assertCurrentEventLoop0, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/FileRegionTest.swift` | testOutstandingFileRegionsWork, testWriteFileRegion, testWriteEmptyFileRegionDoesNotHang |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/GetAddrInfoResolverTest.swift` | testResolveNoDuplicatesV6, testResolveNoDuplicatesV4, GetaddrinfoResolverTest |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/HappyEyeballsTest.swift` | testResolverOnDifferentEventLoop |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/IPv4Header.swift` | setChecksum, writeIPv4Header, isValidChecksum, computeChecksum, writeIPv4HeaderToBSDRawSocket |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/IdleStateHandlerTest.swift` | IdleStateHandlerTest, testIdleAllWrite, testIdleWrite, testIdleAllRead, testIdle, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/MulticastTest.swift` | testCanJoinBasicMulticastGroupIPv6WithDevice, tearDown, leaveMulticastGroup, testCanJoinBasicMulticastGroupIPv4WithDevice, configureSenderMulticastIf, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NIOFileHandleTest.swift` | testOpenCloseWorks, testCloseVsUseRace, NIOFileHandleTest, testCloseStorm, makePipe |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NIOLoopBoundTests.swift` | testLoopBoundBoxCanBeInitialisedWithTakingValueOffLoopAndLaterSetToValue, NIOLoopBoundTests, testLoopBoundBoxCanBeInitialisedWithNilOffLoopAndLaterSetToValue, tearDown, testLoopBoundIsSendableWithNonSendableValue, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NIOThreadPoolTest.swift` | testAsyncThreadPool, testThreadNamesAreSetUp, testAsyncShutdownWorks, testAsyncThreadPoolErrorPropagation, testAsyncThreadPoolNotActiveError, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/NonBlockingFileIOTest.swift` | testAsyncReadDoesNotReadShort, testReadFromNonBlockingPipeFails, testDoesNotBlockTheThreadOrEventLoop, testRemove, testLStat, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/PendingDatagramWritesManagerTests.swift` | testPendingWritesUsesVectorWriteOperationAndDoesntWriteTooMuch, testPendingWritesNoMoreThanWritevLimitIsWrittenInOneMassiveChunk, testPendingWritesSpinCountWorksForSingleWrites, testPendingWritesEmptyWritesWorkAndWeDontWriteUnflushedThings, testPendingWritesCloseDuringVectorWrite, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/PipeChannelTest.swift` | PipeChannelTest, testWeDontAcceptRegularFiles, setUp, testWriteErrorsCloseChannel, testBasicIO, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/RawSocketBootstrapTests.swift` | XCTSkipIfUserHasNotEnoughRightsForRawSocketAPI, testConnect, RawSocketBootstrapTests, testIpHdrincl, testBindWithRecevMmsg |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SALChannelTests.swift` | testWeSurviveIfIgnoringSIGPIPEFails, testAcceptingInboundConnections, testBasicRead, testWriteBeforeChannelActiveClientStreamInstantConnect, testBasicConnectWithClientBootstrap, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SALEventLoopTests.swift` | testSchedulingTaskOnSleepingLoopWakesUpOnce, SALEventLoopTests |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SelectorTest.swift` | testWeDoNotDeliverEventsForPreviouslyClosedChannels, testDeregisterAndCloseWhileProcessingEvents, testTimerFDIsLevelTriggered, testDeregisterWhileProcessingEvents, workaroundSR9815, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SerialExecutorTests.swift` | tearDown |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SocketAddressTest.swift` | testIPAddressWorks, testConvertingStorage, testDescriptionWorksWithByteBufferIPv4IP, testHashEqualSocketAddresses, testUnequalAcrossFamilies, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SocketChannelTest.swift` | assertAcceptFails, testAcceptFailsWithENOBUFS, testConnectServerSocketChannel, testWeAreInterestedInReadEOFWhenChannelIsConnectedOnTheServerSide, testSetGetOptionClosedServerSocketChannel, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SocketOptionProviderTest.swift` | testIpv6MulticastIf, setUp, SocketOptionProviderTest, testIPv6MulticastHops, testPassingInvalidSizeToSetComplexSocketOptionFails, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/StreamChannelsTest.swift` | testWritabilityStartsTrueGoesFalseAndBackToTrue, testWriteFailsAfterOutputClosed, testHalfCloseOwnOutputWithPopulatedBuffer, testEchoBasic, runTest, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SyscallAbstractionLayer.swift` | salWait, read |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SyscallAbstractionLayerContext.swift` | withSALContext |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/SystemTest.swift` | testErrorsWorkCorrectly |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/TestUtils.swift` | withCrossConnectedUnixDomainSocketChannels, forEachActiveChannelType, withCrossConnectedSockAddrChannels, withTemporaryUnixDomainSocketPathName, forEachCrossConnectedStreamChannelPair, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/ThreadTest.swift` | testSharingThreadSpecificVariableWorks, testThreadSpecificDoesNotLeakIfReplacedWithNewValue, testThreadSpecificDoesNotLeakWhenOutOfScopeButThreadStillRunning, joinThread, testThreadSpecificInitWithValueWorks, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/UniversalBootstrapSupportTest.swift` | testBootstrappingWorks, testBootstrapOverrideOfShortcutOptions, UniversalBootstrapSupportTest |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/VsockAddressTest.swift` | testDescriptionWorks, testSocketAddressEqualitySpecialValues, testSocketAddressEquality, testGetLocalCID, testInitializeFromInt, ... |
| `.build/checkouts/console-kit/.build/index-build/checkouts/swift-nio/Tests/NIOPosixTests/XCTest+AsyncAwait.swift` | XCTAssertThrowsError, XCTAssertNoThrow |

## Connected Communities

- **Tests/NIOPosixTests · withTemporaryFile · FileRegionTest · NonBlockingFileIOTest (62) #4** (9 cross-edges)
- **Tests/NIOPosixTests · withTemporaryDirectory · ChannelTests · NonBlockingFileIOTest (21) #1** (5 cross-edges)
- **Sources/NIOHTTP2 +111 dirs** (2 cross-edges)

## How to Explore

```
get_communities with id: "community-1410"
smart_context with task: "understand Tests/NIOPosixTests · XCTAssertNoThrow · AcceptBackoffHandlerTest · AsyncChannelBootstrapTests (819) #2", format: "gcx"
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
