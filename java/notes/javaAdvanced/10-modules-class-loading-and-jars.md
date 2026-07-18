# 10 - Modules, Class Loading, and JARs

## 1) Class Loading

Loading finds bytecode, linking verifies and prepares it, and initialization runs static initialization.

```java
final class LoadedType {
    static {
        System.out.println("initialized");
    }
}

System.out.println(LoadedType.class.getSimpleName());
new LoadedType();
// Output:
// LoadedType
// initialized
```

A class literal does not necessarily initialize the class; active use does.

## 2) Parent Delegation

Class loaders normally ask their parent first. This protects core platform classes and avoids duplicate definitions. Two classes with the same name loaded by different loaders are different runtime types.

```java
ClassLoader loader = String.class.getClassLoader();
System.out.println(loader == null);
// Output: true
// null represents the bootstrap class loader.
```

## 3) Java Platform Module System

```java
module com.example.billing {
    requires java.net.http;
    exports com.example.billing.api;
    // Result: only the api package is exported to dependent modules.
}
```

- `requires` declares a dependency.
- `exports` exposes a package for normal access.
- `opens` permits deep reflection.
- `uses` and `provides ... with` support service loading.

## 4) Service Loading

```java
ServiceLoader<Driver> drivers = ServiceLoader.load(Driver.class);
System.out.println(drivers.stream().count() >= 0);
// Output: true
// The actual provider count depends on the runtime class path/module path.
```

## 5) JAR Practices

- Keep a single version of each dependency.
- Do not package secrets in resources.
- Prefer reproducible builds and dependency locking or verification.
- Inspect transitive dependencies for vulnerabilities.
- Use the class path for simpler applications; introduce modules when strong encapsulation or modular distribution provides clear value.
