# How Java Code Runs - Beginner to Expert

This chapter explains what happens between writing a `.java` file and seeing output.

## 1) The Big Picture

```text
Source code (.java) -> javac compiler -> bytecode (.class) -> JVM -> machine execution
# Result: the same bytecode can run on different operating systems with a compatible JVM.
```

- JDK: tools for developing Java, including compiler and runtime
- JVM: virtual machine that loads and executes bytecode
- bytecode: JVM instructions stored in `.class` files

## 2) Compile and Run

```powershell
javac Hello.java
java Hello
# Output: whatever Hello.main prints.
```

`javac` checks syntax and types. `java` starts a JVM and asks it to run the class.

## 3) Program Entry Point

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello Java");
    }
}
// Output: Hello Java
```

The launcher can call `main` without constructing `Hello` because it is static.

## 4) Class Loading

The JVM locates bytecode, verifies it, prepares class data, and initializes the class before active use.

```java
final class Example {
    static { System.out.println("class initialized"); }
}
new Example();
// Output: class initialized
```

A class is normally initialized once per class loader.

## 5) Method Calls and Stack Frames

Each thread has a call stack. A method call creates a frame containing method execution state such as local variables and an operand stack. Returning removes that frame.

```java
static int doubleValue(int value) {
    return value * 2;
}
static int calculate() {
    return doubleValue(21);
}
System.out.println(calculate());
// Output: 42
```

Call order: `main -> calculate -> doubleValue`, then returns in reverse order.

## 6) Objects and Heap

Objects are normally managed in heap memory. Variables hold primitive values or references that identify objects. Java references are not raw addresses available to application code.

The JVM may optimize storage using escape analysis, so “locals are always stack and objects are always heap” is a teaching shortcut, not a language guarantee.

## 7) Interpreter and JIT

The JVM can interpret bytecode and observe which code runs often. The Just-In-Time compiler turns hot code into optimized machine code.

This is why a tiny single-run timing is not a valid benchmark. Use JMH for Java microbenchmarks.

## 8) Exceptions and Stack Unwinding

When an exception is thrown, Java looks for a matching catch block while unwinding method frames.

```java
try {
    Integer.parseInt("not-a-number");
} catch (NumberFormatException exception) {
    System.out.println("invalid number");
}
// Output: invalid number
```

If nobody handles it, the thread terminates and the uncaught failure is reported.

## 9) Garbage Collection

The JVM reclaims objects that are no longer reachable. Collection timing is not controlled by setting a variable to null or calling `System.gc()`.

Files, sockets, and database connections must be closed explicitly, usually with try-with-resources.

## Interview Checklist

Explain JDK/JVM/bytecode, compilation vs runtime failure, main method, class loading, stack frames, heap, JIT, exception unwinding, and garbage collection without claiming implementation details are language guarantees.
