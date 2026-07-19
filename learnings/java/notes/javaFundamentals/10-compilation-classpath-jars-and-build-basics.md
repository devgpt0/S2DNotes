# 10 - Compilation, Classpath, JARs, and Build Basics

## Source to Execution

```text
Example.java -> javac -> Example.class bytecode -> class loader -> verifier -> JVM execution/JIT
# Result: Java source is compiled to platform-independent bytecode, then executed by a JVM.
```

## Compile and Run

```powershell
javac -d out src\com\example\Main.java
java -cp out com.example.Main
# Output: whatever Main.main prints.
```

The classpath contains roots of package trees and JAR files, not individual package directories.

## JAR

```powershell
jar --create --file app.jar -C out .
java -cp app.jar com.example.Main
# Result: classes are packaged and Main executes from app.jar.
```

An executable JAR has a main class in its manifest and can run with `java -jar`.

## Maven Lifecycle

Common phases: `validate`, `compile`, `test`, `package`, `verify`, `install`, `deploy`.

```powershell
.\mvnw.cmd clean verify
# Result: sources compile, tests run, and verification checks execute.
```

Maven scopes include compile, provided, runtime, test, and import. Inspect transitive dependencies and avoid version conflicts through a BOM or dependency management.

## Gradle Basics

```powershell
.\gradlew.bat clean build
# Result: compilation, tests, checks, and packaging run through the wrapper.
```

Always commit the build wrapper, use reproducible dependency versions, verify checksums where supported, and never package credentials.

## Compile-Time vs Runtime Errors

- syntax/type/access/checked-exception errors are normally compile-time
- missing classes, linkage conflicts, invalid casts, and business failures can occur at runtime
- `ClassNotFoundException` is checked explicit loading failure
- `NoClassDefFoundError` means a class expected by already compiled code could not be defined at runtime
