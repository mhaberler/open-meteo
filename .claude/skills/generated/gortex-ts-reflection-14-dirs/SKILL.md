---
name: gortex-ts-reflection-14-dirs
description: "Work in the ts/reflection +14 dirs area — 864 symbols across 57 files (82% cohesion)"
---

# ts/reflection +14 dirs

864 symbols | 57 files | 82% cohesion

## When to Use

Use this skill when working on files in:
- `.build/checkouts/flatbuffers/goldens/ts/flatbuffers/goldens/universe.ts`
- `.build/checkouts/flatbuffers/tests/namespace_test/NamespaceA/SecondTableInA.java`
- `.build/checkouts/flatbuffers/tests/namespace_test/NamespaceA/TableInFirstNS.java`
- `.build/checkouts/flatbuffers/tests/namespace_test/NamespaceC/TableInC.java`
- `.build/checkouts/flatbuffers/tests/ts/my-game/example/monster.js`
- `.build/checkouts/flatbuffers/tests/ts/my-game/example/monster.ts`
- `.build/checkouts/flatbuffers/tests/ts/my-game/example/type-aliases.js`
- `.build/checkouts/flatbuffers/tests/ts/my-game/example/type-aliases.ts`
- `.build/checkouts/flatbuffers/tests/ts/reflection/enum-val.js`
- `.build/checkouts/flatbuffers/tests/ts/reflection/enum-val.ts`
- `.build/checkouts/flatbuffers/tests/ts/reflection/enum.js`
- `.build/checkouts/flatbuffers/tests/ts/reflection/enum.ts`
- `.build/checkouts/flatbuffers/tests/ts/reflection/field.js`
- `.build/checkouts/flatbuffers/tests/ts/reflection/field.ts`
- `.build/checkouts/flatbuffers/tests/ts/reflection/object.js`
- `.build/checkouts/flatbuffers/tests/ts/reflection/object.ts`
- `.build/checkouts/flatbuffers/tests/ts/reflection/rpccall.js`
- `.build/checkouts/flatbuffers/tests/ts/reflection/rpccall.ts`
- `.build/checkouts/flatbuffers/tests/ts/reflection/schema-file.js`
- `.build/checkouts/flatbuffers/tests/ts/reflection/schema-file.ts`
- `.build/checkouts/flatbuffers/tests/ts/reflection/schema.js`
- `.build/checkouts/flatbuffers/tests/ts/reflection/schema.ts`
- `.build/checkouts/flatbuffers/tests/ts/reflection/service.js`
- `.build/checkouts/flatbuffers/tests/ts/reflection/service.ts`
- `.build/checkouts/flatbuffers/tests/ts/union-underlying-type/d.js`
- `.build/checkouts/flatbuffers/tests/ts/union-underlying-type/d.ts`
- `.build/checkouts/flatbuffers/tests/ts/union_vector/movie.js`
- `.build/checkouts/flatbuffers/tests/ts/union_vector/movie.ts`
- `.build/index-build/checkouts/flatbuffers/goldens/ts/flatbuffers/goldens/universe.ts`
- `.build/index-build/checkouts/flatbuffers/java/src/main/java/com/google/flatbuffers/BaseVector.java`
- `.build/index-build/checkouts/flatbuffers/java/src/main/java/com/google/flatbuffers/FlatBufferBuilder.java`
- `.build/index-build/checkouts/flatbuffers/tests/namespace_test/NamespaceA/SecondTableInA.java`
- `.build/index-build/checkouts/flatbuffers/tests/namespace_test/NamespaceC/TableInC.java`
- `.build/index-build/checkouts/flatbuffers/tests/ts/my-game/example/monster.js`
- `.build/index-build/checkouts/flatbuffers/tests/ts/my-game/example/monster.ts`
- `.build/index-build/checkouts/flatbuffers/tests/ts/my-game/example/type-aliases.js`
- `.build/index-build/checkouts/flatbuffers/tests/ts/my-game/example/type-aliases.ts`
- `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/enum-val.js`
- `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/enum-val.ts`
- `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/enum.js`
- `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/enum.ts`
- `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/field.js`
- `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/field.ts`
- `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/object.js`
- `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/object.ts`
- `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/rpccall.js`
- `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/rpccall.ts`
- `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/schema-file.js`
- `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/schema-file.ts`
- `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/schema.js`
- `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/schema.ts`
- `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/service.js`
- `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/service.ts`
- `.build/index-build/checkouts/flatbuffers/tests/ts/union-underlying-type/d.js`
- `.build/index-build/checkouts/flatbuffers/tests/ts/union-underlying-type/d.ts`
- `.build/index-build/checkouts/flatbuffers/tests/ts/union_vector/movie.js`
- `.build/index-build/checkouts/flatbuffers/tests/ts/union_vector/movie.ts`

## Key Files

| File | Symbols |
|------|---------|
| `.build/checkouts/flatbuffers/goldens/ts/flatbuffers/goldens/universe.ts` | i, startGalaxiesVector, numElems, data, builder, ... |
| `.build/checkouts/flatbuffers/tests/namespace_test/NamespaceA/SecondTableInA.java` | builder, referToCOffset, addReferToC |
| `.build/checkouts/flatbuffers/tests/namespace_test/NamespaceA/TableInFirstNS.java` | addFooUnion, builder, fooUnionOffset, addFooTable, fooTableOffset, ... |
| `.build/checkouts/flatbuffers/tests/namespace_test/NamespaceC/TableInC.java` | addReferToA2, builder, referToA2Offset |
| `.build/checkouts/flatbuffers/tests/ts/my-game/example/monster.js` | startVectorOfDoublesVector, startTestarrayofsortedstructVector, startVectorOfStrongReferrablesVector, startTest5Vector, createVectorOfCoOwningReferencesVector, ... |
| `.build/checkouts/flatbuffers/tests/ts/my-game/example/monster.ts` | builder, i, startVectorOfDoublesVector, numElems, createVectorOfEnumsVector, ... |
| `.build/checkouts/flatbuffers/tests/ts/my-game/example/type-aliases.js` | createVf64Vector, pack, createV8Vector, startV8Vector, startVf64Vector |
| `.build/checkouts/flatbuffers/tests/ts/my-game/example/type-aliases.ts` | data, builder, numElems, builder, pack, ... |
| `.build/checkouts/flatbuffers/tests/ts/reflection/enum-val.js` | createAttributesVector, startAttributesVector, startDocumentationVector |
| `.build/checkouts/flatbuffers/tests/ts/reflection/enum-val.ts` | builder, builder, startDocumentationVector, numElems, data, ... |
| `.build/checkouts/flatbuffers/tests/ts/reflection/enum.js` | createValuesVector, createDocumentationVector, startValuesVector, createAttributesVector, startAttributesVector, ... |
| `.build/checkouts/flatbuffers/tests/ts/reflection/enum.ts` | builder, i, createValuesVector, data, startDocumentationVector, ... |
| `.build/checkouts/flatbuffers/tests/ts/reflection/field.js` | createAttributesVector, startAttributesVector, createDocumentationVector, startDocumentationVector, addOffset |
| `.build/checkouts/flatbuffers/tests/ts/reflection/field.ts` | numElems, builder, createDocumentationVector, builder, startAttributesVector, ... |
| `.build/checkouts/flatbuffers/tests/ts/reflection/object.js` | startDocumentationVector, createAttributesVector, createDocumentationVector, startFieldsVector, startAttributesVector |
| `.build/checkouts/flatbuffers/tests/ts/reflection/object.ts` | numElems, builder, data, data, startFieldsVector, ... |
| `.build/checkouts/flatbuffers/tests/ts/reflection/rpccall.js` | startAttributesVector, createAttributesVector, createDocumentationVector, startDocumentationVector |
| `.build/checkouts/flatbuffers/tests/ts/reflection/rpccall.ts` | numElems, builder, numElems, builder, builder, ... |
| `.build/checkouts/flatbuffers/tests/ts/reflection/schema-file.js` | pack, startIncludedFilenamesVector, createIncludedFilenamesVector |
| `.build/checkouts/flatbuffers/tests/ts/reflection/schema-file.ts` | createIncludedFilenamesVector, builder, startIncludedFilenamesVector, i, numElems, ... |
| `.build/checkouts/flatbuffers/tests/ts/reflection/schema.js` | startServicesVector, startEnumsVector, startObjectsVector, createFbsFilesVector, startFbsFilesVector, ... |
| `.build/checkouts/flatbuffers/tests/ts/reflection/schema.ts` | i, builder, i, startServicesVector, data, ... |
| `.build/checkouts/flatbuffers/tests/ts/reflection/service.js` | startAttributesVector, createDocumentationVector, createAttributesVector, startDocumentationVector, startCallsVector |
| `.build/checkouts/flatbuffers/tests/ts/reflection/service.ts` | builder, createAttributesVector, i, numElems, data, ... |
| `.build/checkouts/flatbuffers/tests/ts/union-underlying-type/d.js` | pack, startTestVectorOfUnionTypeVector, createTestVectorOfUnionVector, startTestVectorOfUnionVector, createTestVectorOfUnionTypeVector |
| `.build/checkouts/flatbuffers/tests/ts/union-underlying-type/d.ts` | builder, createTestVectorOfUnionVector, i, builder, testVectorOfUnionType, ... |
| `.build/checkouts/flatbuffers/tests/ts/union_vector/movie.js` | pack, createCharactersVector, startCharactersTypeVector, startCharactersVector, createCharactersTypeVector |
| `.build/checkouts/flatbuffers/tests/ts/union_vector/movie.ts` | numElems, builder, builder, builder, charactersType, ... |
| `.build/index-build/checkouts/flatbuffers/goldens/ts/flatbuffers/goldens/universe.ts` | i, builder, startGalaxiesVector, builder, data, ... |
| `.build/index-build/checkouts/flatbuffers/java/src/main/java/com/google/flatbuffers/BaseVector.java` | length |
| `.build/index-build/checkouts/flatbuffers/java/src/main/java/com/google/flatbuffers/FlatBufferBuilder.java` | addOffset, createByteVector, alignment, offset, createByteVector, ... |
| `.build/index-build/checkouts/flatbuffers/tests/namespace_test/NamespaceA/SecondTableInA.java` | referToCOffset, builder, addReferToC |
| `.build/index-build/checkouts/flatbuffers/tests/namespace_test/NamespaceC/TableInC.java` | builder, referToA2Offset, referToA1Offset, addReferToA1, addReferToA2, ... |
| `.build/index-build/checkouts/flatbuffers/tests/ts/my-game/example/monster.js` | startTestarrayofstringVector, startVectorOfDoublesVector, startVectorOfStrongReferrablesVector, createTestarrayofboolsVector, startVectorOfWeakReferencesVector, ... |
| `.build/index-build/checkouts/flatbuffers/tests/ts/my-game/example/monster.ts` | data, createVectorOfEnumsVector, builder, i, startTestnestedflatbufferVector, ... |
| `.build/index-build/checkouts/flatbuffers/tests/ts/my-game/example/type-aliases.js` | startVf64Vector, pack, createV8Vector, startV8Vector, createVf64Vector |
| `.build/index-build/checkouts/flatbuffers/tests/ts/my-game/example/type-aliases.ts` | i, i, v8, builder, createVf64Vector, ... |
| `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/enum-val.js` | startDocumentationVector, createDocumentationVector, createAttributesVector, startAttributesVector |
| `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/enum-val.ts` | numElems, startDocumentationVector, builder, builder, startAttributesVector, ... |
| `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/enum.js` | createDocumentationVector, createValuesVector, startDocumentationVector, startAttributesVector, createAttributesVector, ... |
| `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/enum.ts` | i, startValuesVector, builder, i, data, ... |
| `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/field.js` | createAttributesVector, startDocumentationVector, createDocumentationVector, startAttributesVector |
| `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/field.ts` | builder, i, startDocumentationVector, builder, builder, ... |
| `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/object.js` | startDocumentationVector, startFieldsVector, createAttributesVector, createDocumentationVector, startAttributesVector, ... |
| `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/object.ts` | numElems, data, numElems, builder, startFieldsVector, ... |
| `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/rpccall.js` | startAttributesVector, createDocumentationVector, startDocumentationVector |
| `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/rpccall.ts` | createDocumentationVector, builder, builder, data, startAttributesVector, ... |
| `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/schema-file.js` | createIncludedFilenamesVector, startIncludedFilenamesVector |
| `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/schema-file.ts` | numElems, builder, builder, i, startIncludedFilenamesVector, ... |
| `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/schema.js` | startObjectsVector, createEnumsVector, createObjectsVector, startServicesVector, startFbsFilesVector, ... |
| `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/schema.ts` | builder, createFbsFilesVector, i, numElems, builder, ... |
| `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/service.js` | startAttributesVector, startCallsVector, createDocumentationVector, startDocumentationVector, createCallsVector, ... |
| `.build/index-build/checkouts/flatbuffers/tests/ts/reflection/service.ts` | i, i, createAttributesVector, startDocumentationVector, startCallsVector, ... |
| `.build/index-build/checkouts/flatbuffers/tests/ts/union-underlying-type/d.js` | startTestVectorOfUnionVector, pack, startTestVectorOfUnionTypeVector, createTestVectorOfUnionVector, createTestVectorOfUnionTypeVector |
| `.build/index-build/checkouts/flatbuffers/tests/ts/union-underlying-type/d.ts` | createTestVectorOfUnionVector, startTestVectorOfUnionTypeVector, builder, data, builder, ... |
| `.build/index-build/checkouts/flatbuffers/tests/ts/union_vector/movie.js` | createCharactersVector, startCharactersVector, pack, createCharactersTypeVector, startCharactersTypeVector |
| `.build/index-build/checkouts/flatbuffers/tests/ts/union_vector/movie.ts` | i, builder, mainCharacter, characters, data, ... |

## Connected Communities

- **ts/reflection +62 dirs** (3 cross-edges)
- **google/flatbuffers +4 dirs** (3 cross-edges)
- **my-game/example +6 dirs** (3 cross-edges)
- **ts/union-underlying-type · createD · d · d (11) #1** (2 cross-edges)
- **ts/union_vector · createMovie · movie · movie** (2 cross-edges)
- **my-game/example · createTypeAliases · type-aliases** (2 cross-edges)
- **ts/union-underlying-type · createD · d · d (11) #2** (2 cross-edges)
- **ts/union_vector · createMovie · movie (27)** (2 cross-edges)
- **namespace_test/NamespaceA +2 dirs · addByte** (1 cross-edges)
- **namespace_test/NamespaceA +2 dirs · FlatBufferBuilder** (1 cross-edges)
- **google/flatbuffers +6 dirs** (1 cross-edges)
- **ts/reflection · pack · enum-val · enum-val (57)** (1 cross-edges)
- **MyGame/Example +34 dirs · __offset** (1 cross-edges)
- **tests/ts +6 dirs** (1 cross-edges)

## How to Explore

```
get_communities with id: "community-3035"
smart_context with task: "understand ts/reflection +14 dirs", format: "gcx"
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
