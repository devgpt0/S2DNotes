# 17 - Java Evolution and Migration

## Major Modern Features

- Java 8: lambdas, streams, Optional, default methods, java.time
- Java 9: modules, collection factories, Flow API
- Java 10: local variable type inference
- Java 11: standardized HTTP client and useful String/files methods
- Java 14-17: switch expressions, text blocks, records, sealed classes, pattern matching for `instanceof`
- Java 21: virtual threads, record patterns, pattern matching for switch, sequenced collections
- later releases continue language, runtime, GC, and concurrency evolution

## Migration Rules

```powershell
jdeps --multi-release 21 --recursive app.jar
# Result: reports module/package dependencies and possible internal JDK API usage.
```

```powershell
java -Xlog:class+load=info -jar app.jar
# Result: logs class loading for compatibility diagnosis; output is application-specific.
```

- upgrade build plugins and test tools first
- compile with the intended `--release`
- remove internal JDK API usage
- check removed Java EE modules and `javax` to `jakarta` migrations
- run unit, integration, performance, and production-like tests
- inspect deprecation/removal warnings
- validate GC, TLS, locale, timezone, reflection, and serialization behavior
- use a supported LTS unless a non-LTS feature justifies the operational cadence

## `var` Interview Point

```java
var names = List.of("Asha", "Ravi");
System.out.println(names.getClass().getSimpleName());
// Output is an internal immutable-list class name and is not an API guarantee.
// var changes local syntax, not Java's static typing.
```
