# 04 - Files, Paths, and NIO.2

## 1) `Path` Models a Path

`Path` does not guarantee that a file exists.

```java
Path path = Path.of("reports", "daily.txt");
System.out.println(path.getFileName());
System.out.println(path.getParent());
// Output:
// daily.txt
// reports
```

## 2) Read and Write Small Files

```java
Path file = Files.createTempFile("java-notes-", ".txt");
Files.writeString(file, "first\nsecond", StandardCharsets.UTF_8);
System.out.println(Files.readString(file, StandardCharsets.UTF_8));
Files.delete(file);
// Output:
// first
// second
```

Specify the character set explicitly at data boundaries.

## 3) Stream Large Files

```java
Path file = Files.createTempFile("lines-", ".txt");
Files.write(file, List.of("Java", "Spring"), StandardCharsets.UTF_8);
try (Stream<String> lines = Files.lines(file, StandardCharsets.UTF_8)) {
    System.out.println(lines.filter(line -> line.startsWith("J")).count());
}
Files.delete(file);
// Output: 1
```

The stream owns an open file, so close it with try-with-resources.

## 4) Safe Directory Traversal

```java
Path root = Files.createTempDirectory("notes-");
Files.writeString(root.resolve("a.txt"), "A");
try (Stream<Path> entries = Files.list(root)) {
    entries.map(Path::getFileName).forEach(System.out::println);
}
Files.delete(root.resolve("a.txt"));
Files.delete(root);
// Output: a.txt
```

`Files.walk` is recursive; `Files.list` is one level.

## 5) Prevent Path Traversal

```java
static Path resolveInside(Path root, String userFile) {
    Path normalizedRoot = root.toAbsolutePath().normalize();
    Path resolved = normalizedRoot.resolve(userFile).normalize();
    if (!resolved.startsWith(normalizedRoot)) {
        throw new IllegalArgumentException("path escapes allowed directory");
    }
    return resolved;
}

System.out.println(resolveInside(Path.of("uploads"), "images/a.png").getFileName());
// Output: a.png
```

For security-sensitive writes, also consider symbolic links and filesystem permissions.

## 6) Useful APIs

- `Files.copy/move/delete`
- `Files.isRegularFile/isDirectory/isReadable`
- `DirectoryStream` for filtered iteration
- `WatchService` for filesystem change notifications
- `FileChannel` and buffers for lower-level random or high-throughput I/O
