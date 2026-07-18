# 12 - Common Java Fundamentals Code Snippets and Solved Questions

## 1) Reverse a String Safely for Unicode Code Points

Question: Reverse the visible code-point sequence without splitting supplementary Unicode characters.

```java
static String reverse(String value) {
    Objects.requireNonNull(value, "value");
    int[] codePoints = value.codePoints().toArray();
    StringBuilder result = new StringBuilder(value.length());
    for (int index = codePoints.length - 1; index >= 0; index--) {
        result.appendCodePoint(codePoints[index]);
    }
    return result.toString();
}

System.out.println(reverse("Java"));
// Output: avaJ
```

Complexity: O(n) time and O(n) space.

## 2) Check a Palindrome

```java
static boolean isPalindrome(String value) {
    Objects.requireNonNull(value, "value");
    int left = 0;
    int right = value.length() - 1;
    while (left < right) {
        if (value.charAt(left++) != value.charAt(right--)) {
            return false;
        }
    }
    return true;
}

System.out.println(isPalindrome("level"));
System.out.println(isPalindrome("java"));
// Output:
// true
// false
```

Interview note: clarify case, spaces, punctuation, and full Unicode requirements before coding.

## 3) Find the Second-Largest Distinct Number

```java
static OptionalInt secondLargest(int[] values) {
    Integer largest = null;
    Integer second = null;
    for (int value : values) {
        if (largest == null || value > largest) {
            if (largest == null || value != largest) second = largest;
            largest = value;
        } else if (value != largest && (second == null || value > second)) {
            second = value;
        }
    }
    return second == null ? OptionalInt.empty() : OptionalInt.of(second);
}

System.out.println(secondLargest(new int[] {5, 3, 5, 4}).orElseThrow());
// Output: 4
```

Complexity: O(n) time and O(1) extra space.

## 4) Prime Number Check

```java
static boolean isPrime(int value) {
    if (value < 2) return false;
    if (value % 2 == 0) return value == 2;
    for (int divisor = 3; divisor <= value / divisor; divisor += 2) {
        if (value % divisor == 0) return false;
    }
    return true;
}

System.out.println(isPrime(29));
System.out.println(isPrime(21));
// Output:
// true
// false
```

Using `divisor <= value / divisor` avoids multiplication overflow.

## 5) Factorial with Overflow Detection

```java
static long factorial(int value) {
    if (value < 0) throw new IllegalArgumentException("value must be non-negative");
    long result = 1;
    for (int number = 2; number <= value; number++) {
        result = Math.multiplyExact(result, number);
    }
    return result;
}

System.out.println(factorial(5));
// Output: 120
```

Interview note: `long` overflows beyond 20!, so use `BigInteger` when larger results are required.

## 6) Strict Integer Parsing

```java
static int parsePort(String text) {
    Objects.requireNonNull(text, "text");
    int port = Integer.parseInt(text);
    if (port < 1 || port > 65_535) {
        throw new IllegalArgumentException("port must be between 1 and 65535");
    }
    return port;
}

System.out.println(parsePort("8080"));
// Output: 8080
```

The method validates rather than trimming or silently converting malformed input.

## 7) Swap Without an Unsafe Arithmetic Trick

```java
int first = 10;
int second = 20;
int temporary = first;
first = second;
second = temporary;
System.out.println(first + ", " + second);
// Output: 20, 10
```

A temporary variable is clearer and avoids overflow-prone addition/subtraction tricks.

## Quick Interview Questions

- Why is Java pass-by-value? The parameter always receives a copied primitive or reference value.
- Why prefer `equals` for strings? `==` checks identity; `equals` checks content.
- Why use `Math.addExact/multiplyExact`? They fail explicitly on integer overflow.
- Why return `OptionalInt`? The second-largest distinct value may not exist.
- JDK vs JVM? JDK supplies development/runtime tools; JVM loads and executes bytecode.
- Primitive vs reference? Primitive variable contains a primitive value; reference identifies an object or null.
- Local vs field default? Fields receive defaults; local variables must be definitely assigned before use.
- `final` reference meaning? The variable cannot be reassigned; the referenced object may still be mutable.
- Static meaning? Member belongs to the class and is shared for that class-loader/class state.
- Overloading vs overriding? Compile-time parameter selection vs runtime subtype method dispatch.
- Widening vs boxing priority? Applicable primitive widening is normally preferred over boxing.
- Why is String immutable? Stable value/hash/security/sharing/thread-safety benefits.
- StringBuilder vs StringBuffer? Unsynchronized local mutable builder vs synchronized legacy builder.
- `&&` vs `&` for booleans? Short-circuit vs always evaluate both sides.
- `break` vs `continue`? Exit loop/switch vs skip to next loop iteration.
- `do-while` difference? Executes body once before checking.
- Integer division? `5 / 2` is 2 because both operands are integers.
- Wrapper cache trap? Identity may be shared for some boxed constants; always use equals for value comparison.
- Why avoid return in finally? It can replace a result and suppress an exception.
