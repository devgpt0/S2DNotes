# Batch 1 — Week 3 MCQ Model Solutions

Each item includes the question, the correct (correct) option, and the reasoning.

## 1

Question: What is the most precise description of a Python variable?

correct Option: A. A name bound to an object

Solution: Python variables are names bound to objects. The name does not itself contain a fixed typed memory box; an object has a type, and a name can later be rebound to another object.

## 2

Question: Why can a tuple containing a list change its visible contents?

correct Option: A. Tuple immutability is shallow and the nested list can mutate

Solution: A tuple cannot have its element references replaced, but it does not recursively freeze the objects it references. The list inside the tuple remains mutable, so its contents can change.

## 3

Question: Why is a tuple containing a list not hashable?

correct Option: A. Its mutable member prevents a stable hash

Solution: Hashable objects must have a stable hash value during their lifetime. Since the nested list can change and lists are unhashable, the tuple cannot safely be used as a dictionary key or set member.

## 4

Question: What is the key difference between // and /?

correct Option: A. // performs floor division while / performs true division

Solution: / returns a floating-point quotient in ordinary Python division. // returns the floor of the quotient, which matters for negative values because flooring moves toward negative infinity.

## 5

Question: What does a and b return when a is falsy?

correct Option: A. The first falsy operand without evaluating later operands

Solution: and uses short-circuit evaluation and returns an operand, not necessarily a Boolean. If a is falsy, its value is returned immediately and b is not evaluated.

## 6

Question: What makes a comparison chain different from manually repeated comparisons?

correct Option: A. The shared middle expression is evaluated once

Solution: In an expression such as a < b < c, Python evaluates b once and checks both comparisons. It is logically equivalent to a < b and b < c, but avoids repeating the middle expression.

## 7

Question: When does a loop else block execute?

correct Option: A. When the loop finishes without break

Solution: The else clause belongs to the loop. It executes when iteration completes normally; a break skips it. The loop may execute zero or more times.

## 8

Question: What does a match case guard add?

correct Option: A. A boolean condition that must also succeed

Solution: A guard such as case int(n) if n > 0 first requires the pattern to match and then requires the guard expression to be truthy. Both conditions are necessary.

## 9

Question: Why is a mutable default parameter dangerous?

correct Option: A. The same default object persists across calls

Solution: Default argument expressions are evaluated once, when the function is defined. A list or dictionary default is shared by calls that omit that argument, allowing state to leak between calls.

## 10

Question: What does / in a function parameter list enforce?

correct Option: A. Parameters before it are positional-only

Solution: In def f(a, /, b), a must be supplied positionally. Parameters after / may be positional or keyword arguments unless other markers impose restrictions.

## 11

Question: What is the late-binding closure trap?

correct Option: A. Closures read a shared loop variable when called later

Solution: Closures capture the variable binding, not a snapshot of its current value. If lambdas are created in a loop and called afterward, they commonly all observe the loop variable’s final value.

## 12

Question: What is required for safe recursion?

correct Option: A. A reachable base case that stops recursive calls

Solution: Every recursive path must eventually reach a base case. Without one, calls continue until Python raises RecursionError.

## 13

Question: What do Python type hints normally do at runtime?

correct Option: A. Provide metadata without enforcing the hinted type

Solution: Standard Python does not automatically validate annotations. They are metadata for readers, IDEs, static type checkers, and optional runtime validation libraries.

## 14

Question: What is structural typing through a Protocol?

correct Option: A. Compatibility based on required behavior rather than inheritance

Solution: A structural type is satisfied when an object provides the required members, even if its class does not inherit from the protocol. This formalizes a form of duck typing for static checking.

## 15

Question: Why does except Exception not catch every possible failure?

correct Option: A. Some exceptions such as BaseException subclasses are outside Exception

Solution: Exception is not the root of the entire hierarchy; BaseException is. SystemExit, KeyboardInterrupt, and GeneratorExit derive directly from BaseException.

## 16

Question: What is a major control-flow property of finally?

correct Option: A. It runs during normal completion and most exception paths

Solution: The finally block is intended for cleanup and runs whether the try block succeeds or an exception is handled or propagated. A return or exception raised inside finally can replace an earlier result.

## 17

Question: What does raise NewError() from old_error express?

correct Option: A. Explicit exception chaining with old_error as the cause

Solution: The from clause sets the new exception’s __cause__ to the original exception. Tracebacks then show the causal relationship explicitly.

## 18

Question: What is the main risk of catching Exception broadly?

correct Option: A. It can hide unrelated programming errors

Solution: A broad handler can swallow bugs that should fail loudly or be fixed. Handlers should normally catch only exceptions that the code can meaningfully recover from or report.

## 19

Question: What happens on the first import of a module?

correct Option: A. Its top-level code executes and the module is cached

Solution: Python executes the module’s top-level statements on the first import and stores the module in sys.modules. Later imports normally reuse the cached module object.

## 20

Question: What is the purpose of if __name__ == '__main__':?

correct Option: A. To run code only when the file is executed as the entry script

Solution: When a file is run directly, its __name__ is '__main__'; when imported, it normally has its module name. The guard keeps command-line behavior from running during import.

## 21

Question: What does a leading dot in from .pricing import total mean?

correct Option: A. Import relative to the current package

Solution: A leading dot denotes a relative import. The module is resolved within the package containing the current module rather than from the top-level import path.

## 22

Question: What does LEGB describe?

correct Option: A. The order of local, enclosing, global, and built-in lookup

Solution: Python resolves an unqualified name through Local, Enclosing-function, Global, and Built-in scopes, in that order. global and nonlocal can change where assignments are made.

## 23

Question: Why is memory size not a portable Python-language guarantee?

correct Option: A. Object layout and sizes are implementation-dependent

Solution: Object representation depends on the Python implementation, version, platform, and build. Python language semantics do not promise one universal byte size for each object.

## 24

Question: What is the difference between bytes.decode and str.encode?

correct Option: A. decode turns bytes into text; encode turns text into bytes

Solution: Decoding interprets a byte sequence using an encoding such as UTF-8 and produces str. Encoding converts a string into bytes using that encoding.

## 25

Question: What does Final communicate?

correct Option: A. A static intent that a name should not be reassigned

Solution: typing.Final communicates an intended single assignment to static type checkers. It does not create a runtime lock or make the referenced object immutable.

## 26

Question:
    a = [1, 2]
    b = a
    b.append(3)
    a = [9]
    print(b, a, b is a)

correct Option: A. Output: [1, 2, 3] [9] False

Solution: a and b initially alias the same list, so append mutates it. The later assignment rebinds only a to a new list; b still refers to the original, and identity is False.

## 27

Question:
    x = [[1], [2]]
    y = x.copy()
    y[0].append(8)
    y.append([9])
    print(x, y)

correct Option: A. Output: [[1, 8], [2]] [[1, 8], [2], [9]]

Solution: copy() makes a shallow outer copy. The first inner list is shared, so appending 8 changes x[0] too; appending a new item changes only y’s outer list.

## 28

Question:
    import copy
    a = [[1], [2]]
    b = copy.deepcopy(a)
    b[0].append(7)
    print(a, b, a is b)

correct Option: A. Output: [[1], [2]] [[1, 7], [2]] False

Solution: deepcopy recursively creates independent nested objects. Mutating b[0] cannot affect a[0], and the outer lists are distinct.

## 29

Question:
    items = [1]
    alias = items
    items += [2]
    print(items is alias, alias)

correct Option: A. Output: True [1, 2]

Solution: For a list, += performs an in-place extension. Both names still refer to the same list, now containing 1 and 2.

## 30

Question:
    first, *middle, last = [10, 20, 30, 40]
    middle.append(99)
    print(first, middle, last)

correct Option: A. Output: 10 [20, 30, 99] 40

Solution: Extended unpacking assigns 10 to first, 40 to last, and a new list [20, 30] to middle. Appending 99 changes that new list only.

## 31

Question:
    def change(value):
        value.append(4)
        value = [8]
        return value
    data = [1]
    print(data, change(data))

correct Option: A. Output: [1, 4] [8]

Solution: The parameter initially aliases data, so append mutates the caller’s list. Reassigning value afterward affects only the local name, and the returned new list is [8].

## 32

Question:
    def add(value, bucket=[]):
        bucket.append(value)
        return bucket
    print(add(1))
    print(add(2))

correct Option: A. Output: [1] then [1, 2]

Solution: The default list is created once at function definition time. Both calls use the same list, so the second call sees the value appended by the first.

## 33

Question:
    functions = []
    for i in range(3):
        functions.append(lambda: i)
    print([fn() for fn in functions])

correct Option: A. Output: [2, 2, 2]

Solution: Each lambda closes over the same i binding. Calls happen after the loop, when i is 2, so every lambda returns 2.

## 34

Question:
    functions = []
    for i in range(3):
        functions.append(lambda i=i: i)
    print([fn() for fn in functions])

correct Option: A. Output: [0, 1, 2]

Solution: The default argument expression is evaluated during each loop iteration. Each lambda therefore stores its iteration’s value independently.

## 35

Question:
    def outer():
        count = 0
        def inner():
            nonlocal count
            count += 1
            return count
        return inner
    f = outer()
    print(f(), f())

correct Option: A. Output: 1 2

Solution: nonlocal count makes inner update the variable in outer’s enclosing scope. The closure retains that state between calls, producing 1 and then 2.

## 36

Question:
    def show(a, /, b, *, c):
        return a + b + c
    print(show(1, 2, c=3))

correct Option: A. Output: 6

Solution: a is positional-only, b may be positional, and c is keyword-only. The call obeys all three rules and computes 1 + 2 + 3.

## 37

Question:
    def collect(*args, **kwargs):
        return args, kwargs
    print(collect(1, 2, x=3))

correct Option: A. Output: ((1, 2), {'x': 3})

Solution: *args collects positional arguments into a tuple, while **kwargs collects keyword arguments into a dictionary. The return value contains both collections.

## 38

Question:
    def f():
        try:
            return 'try'
        finally:
            return 'finally'
    print(f())

correct Option: A. Output: finally

Solution: finally executes before the function returns. Its own return statement replaces the pending return from the try block.

## 39

Question:
    def factorial(n):
        if n == 0:
            return 1
        return n * factorial(n - 1)
    print(factorial(5))

correct Option: A. Output: 120

Solution: The calls multiply 5 × 4 × 3 × 2 × 1, then the base case returns 1. Therefore 5! is 120.

## 40

Question:
    print(7 / 2)
    print(7 // 2, -7 // 2)
    print(-10 % 3)

correct Option: A. Output: 3.5 then 3 -4 then 2

Solution: True division gives 3.5. Floor division gives 3 and -4; Python’s modulo identity makes -10 % 3 equal 2.

## 41

Question:
    print(-3**2, (-3)**2)
    print(2**3**2)

correct Option: A. Output: -9 9 then 512

Solution: Exponentiation binds more tightly than unary minus, so -3**2 is -9 while (-3)**2 is 9. Exponentiation is right-associative, making 2**(3**2) equal 512.

## 42

Question:
    result = (n := 4) * 2
    print(result, n)

correct Option: A. Output: 8 4

Solution: The assignment expression binds 4 to n and evaluates to 4. Multiplication produces result = 8, while n remains 4.

## 43

Question:
    print('' and 'later')
    print('ready' or 'later')
    print(0 or 5 and 6)

correct Option: A. Output: blank line, ready, 6

Solution: An empty string is returned by the first and, producing a blank line. or returns the first truthy operand, and and has higher precedence than or, so 0 or (5 and 6) returns 6.

## 44

Question:
    left = {1, 2, 3}
    right = {3, 4}
    print(sorted(left & right))
    print(sorted(left ^ right)) 

correct Option: A. Output: [3] then [1, 2, 4]

Solution: & is intersection, giving {3}. ^ is symmetric difference, giving elements present in exactly one set: {1, 2, 4}; sorting fixes the output order.

## 45

Question:
    value = 6
    print(value & 3, value | 3, value ^ 3)
    print(~value)

correct Option: A. Output: 2 7 5 then -7

Solution: In binary, 6 is 110 and 3 is 011: AND is 2, OR is 7, and XOR is 5. Python’s ~n equals -n - 1, so ~6 is -7.

## 46

Question:
    print(3 << 2)
    print(20 >> 2)
    print(-5 >> 1)

correct Option: A. Output: 12 then 5 then -3

Solution: Left shift by two multiplies 3 by four, giving 12. Right shift is floor-style division by powers of two: 20 >> 2 is 5 and -5 >> 1 is -3.

## 47

Question:
    raw = 'caf\u00e9'
    data = raw.encode('utf-8')
    print(type(data).__name__, data.decode('utf-8'))

correct Option: A. Output: bytes café

Solution: Encoding the Unicode string with UTF-8 creates a bytes object. Decoding those bytes with the same encoding reconstructs café.

## 48

Question:
    items = [0, '', [], [1]]
    print([bool(item) for item in items])
    print(any(items), all(items))

correct Option: A. Output: [False, False, False, True] then True False

Solution: Zero, an empty string, and an empty list are falsy; [1] is truthy. any sees the final truthy item, while all fails on the earlier falsy items.

## 49

Question:
    names = ['a', 'b', 'c']
    for index, name in enumerate(names, start=1):
        print(index, name)

correct Option: A. Output: 1 a; 2 b; 3 c

Solution: enumerate pairs each item with an index. start=1 makes the indices one-based, producing 1 a, 2 b, and 3 c.

## 50

Question:
    left = [1, 2, 3]
    right = ['a', 'b']
    print(list(zip(left, right)))

correct Option: A. Output: [(1, 'a'), (2, 'b')]

Solution: zip pairs items positionally and stops when the shortest input is exhausted. The unmatched 3 is not included.

## 51

Question:
    n = 0
    while n < 5:
        n += 1
        if n == 3:
            continue
        print(n)

correct Option: A. Output: 1 2 4 5

Solution: The counter becomes 1, 2, 3, 4, and 5. At 3, continue skips the print for that iteration; the loop then continues with 4 and 5.

## 52

Question:
    for value in [1, 2, 3]:
        if value == 4:
            break
    else:
        print('completed')

correct Option: A. Output: completed

Solution: No value equals 4, so break never runs. The loop completes normally and its else block prints completed.

## 53

Question:
    pairs = []
    for row in range(2):
        for column in range(3):
            pairs.append((row, column))
    print(pairs)

correct Option: A. Output: [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]

Solution: The outer loop fixes row at 0 while the inner loop visits columns 0, 1, and 2. It then repeats for row = 1, giving six row-major pairs.

## 54

Question:
    def classify(value):
        match value:
            case int(n) if n > 0:
                return 'positive'
            case int():
                return 'integer'
            case _:
                return 'other'
    print(classify(-2), classify(3), classify('3'))

correct Option: A. Output: integer positive other

Solution: -2 matches int(n) but fails the positive guard, then matches int() and returns integer. 3 passes the guard and is positive; the string reaches the wildcard and is other.

## 55

Question:
    values = [2, 4, 6]
    print(any(value % 2 for value in values))
    print(all(value % 2 == 0 for value in values))

correct Option: A. Output: False then True

Solution: The remainders are all 0, which is falsy, so any returns False. Every value satisfies the explicit evenness test, so all returns True.

## 56

Question:
    for value in [1, 2]:
        pass
    print('after')

correct Option: A. Output: after

Solution: pass is a no-op statement. The loop performs no output, then execution reaches the final print.

## 57

Question:
    try:
        value = int('x')
    except ValueError:
        print('bad')
    else:
        print('good')
    finally:
        print('done')

correct Option: A. Output: bad then done

Solution: Converting x raises ValueError, so except prints bad and else is skipped. finally always runs and prints done.

## 58

Question:
    try:
        {}['missing']
    except (KeyError, IndexError) as error:
        print(type(error).__name__)

correct Option: A. Output: KeyError

Solution: Looking up a missing dictionary key raises KeyError. The tuple of exception types catches either KeyError or IndexError, and the actual type name is printed.

## 59

Question:
    def convert(value):
        try:
            return int(value)
        except ValueError as error:
            raise TypeError('bad input') from error
    try:
        convert('x')
    except Exception as error:
        print(type(error).__name__, type(error.__cause__).__name__)

correct Option: A. Output: TypeError ValueError

Solution: int('x') raises ValueError. The handler raises TypeError with from error, so the new exception is TypeError and its explicit cause is ValueError.

## 60

Question:
    class ShortInputError(ValueError):
        pass
    def check(text):
        if len(text) < 3:
            raise ShortInputError('short')
        return 'ok'
    try:
        check('x')
    except ValueError as error:
        print(type(error).__name__, str(error))

correct Option: A. Output: ShortInputError short

Solution: ShortInputError is a subclass of ValueError, so the handler catches it. type(error).__name__ reports the concrete subclass, and its message is short.

## 61

Question:
    try:
        1 / 0
    except ZeroDivisionError:
        print('handled')
        raise

correct Option: A. Output: handled, then ZeroDivisionError propagates

Solution: The handler prints handled. A bare raise re-raises the currently handled ZeroDivisionError, so it continues to propagate.

## 62

Question:
    try:
        [1][4]
    except LookupError:
        print('lookup')
    except IndexError:
        print('index')

correct Option: A. Output: lookup

Solution: IndexError is a subclass of LookupError. Handlers are checked from top to bottom, so the broader first handler catches it and the second is not reached.

## 63

Question:
    def require(value):
        assert value > 0, 'non-positive'
        return value
    try:
        require(0)
    except AssertionError as error:
        print(type(error).__name__, str(error))

correct Option: A. Output: AssertionError non-positive

Solution: The assertion condition 0 > 0 is false. Python raises AssertionError with the supplied message, which the handler prints.

## 64

Question:
    namespace = {'__name__': '__main__'}
    exec("if __name__ == '__main__':\n    print('run')", namespace)

correct Option: A. Output: run

Solution: exec evaluates the source using the supplied namespace. Since that namespace sets __name__ to '__main__', the condition is true and run is printed.

## 65

Question:
    import sys, types
    module = types.ModuleType('cached_demo')
    module.count = 7
    sys.modules['cached_demo'] = module
    import cached_demo
    print(cached_demo.count)

correct Option: A. Output: 7

Solution: The manually created module is inserted into sys.modules under the requested name. The import machinery reuses that cached object, whose count attribute is 7.

## 66

Question:
    import importlib
    module = importlib.import_module('math')
    print(module.sqrt(81), module.__name__)

correct Option: A. Output: 9.0 math

Solution: import_module dynamically imports math. math.sqrt(81) returns the floating-point value 9.0, and the module’s name is math.

## 67

Question:
    import sys, types
    module = types.ModuleType('named_demo')
    module.value = 4
    sys.modules['named_demo'] = module
    print(named_demo.value)

correct Option: A. Output: NameError

Solution: Adding a module to sys.modules makes it importable, but it does not bind the name named_demo in the current namespace. Without an import statement, evaluating that name raises NameError.

## 68

Question:
    source = "value = 3\nprint(__name__)"
    namespace = {'__name__': 'demo_module'}
    exec(source, namespace)
    print(namespace['value'])

correct Option: A. Output: demo_module then 3

Solution: The executed code reads __name__ from the supplied namespace and prints demo_module. It also stores value = 3 there, which is printed afterward through the dictionary.

## 69

Question:
    from typing import get_type_hints
    def add(x: int, y: int) -> int:
        return x + y
    print(add('a', 'b'))
    print(get_type_hints(add)['return'].__name__)

correct Option: A. Output: ab then int

Solution: Annotations do not enforce argument types at runtime, so string concatenation returns ab. The return annotation remains int, which get_type_hints reports.

## 70

Question:
    from typing import TypedDict
    class User(TypedDict):
        name: str
    user = User(name='Ana')
    print(type(user).__name__, user['name'])

correct Option: A. Output: dict Ana

Solution: TypedDict describes the expected dictionary shape for static checking; it does not create a distinct runtime dictionary class. The instance is an ordinary dict containing name: Ana.

## 71

Question:
    from dataclasses import dataclass
    @dataclass(frozen=True)
    class Point:
        x: int
    p = Point(2)
    print(p)
    try:
        p.x = 3
    except Exception as error:
        print(type(error).__name__)

correct Option: A. Output: Point(x=2) then FrozenInstanceError

Solution: Dataclasses generate a readable representation, so p prints as Point(x=2). frozen=True prevents field assignment and raises FrozenInstanceError when p.x is changed.

## 72

Question:
    from typing import Protocol
    class Named(Protocol):
        name: str
    class User:
        name = 'Ana'
    def greet(value: Named):
        return value.name
    print(greet(User()))

correct Option: A. Output: Ana

Solution: User supplies the required name attribute, so it is structurally compatible with Named. The annotation does not require inheritance, and greet returns Ana.

## 73

Question:
    from typing import Final
    LIMIT: Final = 3
    LIMIT = 4
    print(LIMIT)

correct Option: A. Output: 4

Solution: Final is intended for static analysis and does not enforce immutability at runtime. The reassignment succeeds, so the printed value is 4.

## 74

Question:
    from typing import TypeVar
    T = TypeVar('T')
    def first(value: list[T]) -> T:
        return value[0]
    print(first([1, 2]), first(['a', 'b']))

correct Option: A. Output: 1 a

Solution: The function returns the first element of each list. Type variables express the relationship between the list element type and return type, but do not alter runtime behavior.

## 75

Question:
    print(type(3).__name__)
    print(isinstance(True, int))
    print(isinstance(True, bool))

correct Option: A. Output: int then True then True

Solution: The type of 3 is int. bool is a subclass of int in Python, so True is an instance of both bool and int.

## 76

Question:
    print(int('101', 2))
    print(int('ff', 16))
    print(int(3.9))

correct Option: A. Output: 5 then 255 then 3

Solution: Binary 101 is decimal 5; hexadecimal ff is 255. Converting the float to int truncates toward zero, producing 3.

## 77

Question:
    print(float(5), str(5), bool([]), bool([0]))
    print(ord('A'), chr(66))

correct Option: A. Output: 5.0 5 False True then 65 B

Solution: float(5) gives 5.0 and str(5) gives text 5. An empty list is falsy while a nonempty list is truthy, regardless of its element; ord and chr convert between characters and code points.

## 78

Question:
    print(hex(31), bin(5), oct(9))
    print(int('0b101', 0))

correct Option: A. Output: 0x1f 0b101 0o11 then 5

Solution: hex, bin, and oct use prefixes 0x, 0b, and 0o. With base 0, int detects the 0b prefix and converts binary 101 to 5.

## 79

Question:
    value = 257
    other = int('257')
    print(value == other)
    print(value is other)

correct Option: A. Output: True then False

Solution: Both values compare equal numerically. is checks object identity, not equality; independently created integer objects for 257 are not guaranteed to be the same object.

## 80

Question:
    raw = bytearray(b'abc')
    raw[0] = 65
    print(raw, bytes(raw))

correct Option: A. Output: bytearray(b'Abc') b'Abc'

Solution: A bytearray is mutable, and ASCII code 65 is A, so its first byte changes. Converting it to bytes creates an immutable byte sequence with the same contents.

## 81

Question:
    def outer():
        value = 'enclosing'
        def inner():
            return value
        return inner
    fn = outer()
    print(fn())

correct Option: A. Output: enclosing

Solution: inner closes over outer’s value. That enclosing binding remains available after outer returns, so calling fn returns enclosing.

## 82

Question:
    value = 'global'
    def show():
        print(value)
    show()

correct Option: A. Output: global

Solution: show has no local assignment to value, so name lookup proceeds to the global scope and finds global.

## 83

Question:
    value = 'global'
    def show():
        print(value)
        value = 'local'
    try:
        show()
    except Exception as error:
        print(type(error).__name__)

correct Option: A. Output: UnboundLocalError

Solution: Because show assigns to value, Python treats value as local throughout the function. The print reads that uninitialized local before its assignment, causing UnboundLocalError.

## 84

Question:
    events = []
    def mark(name):
        events.append(name)
        return name
    result = mark('left') + mark('right')
    print(events, result)

correct Option: A. Output: ['left', 'right'] leftright

Solution: Python evaluates the left operand of + before the right operand. The calls therefore append left and then right; string addition produces leftright.

## 85

Question:
    class Example:
        value = 2
        print('class body', value)
    print(Example.value)

correct Option: A. Output: class body 2 then 2

Solution: A class body executes immediately while the class is being created, so its print runs first. The assignment creates Example.value, which the second print reads.

## 86

Question:
    def decorator(fn):
        print('decorate')
        return fn
    @decorator
    def task():
        print('call')
    task()

correct Option: A. Output: decorate then call

Solution: The decorator is applied when the function definition executes, so decorate prints during definition. Calling task afterward executes its body and prints call.

## 87

Question:
    import asyncio
    async def value():
        return 7
    print(asyncio.run(value()))

correct Option: A. Output: 7

Solution: Calling an async def function creates a coroutine. asyncio.run executes it in an event loop, obtains the return value 7, and print displays it.

## 88

Question:
    import threading
    event = threading.Event()
    result = []
    def worker():
        result.append('worker')
        event.set()
    t = threading.Thread(target=worker)
    t.start()
    event.wait()
    t.join()
    print(result)

correct Option: A. Output: ['worker']

Solution: The worker appends worker and sets the event. The main thread waits for that signal, then joins the worker, so the list contains the appended value before printing.

## 89

Question:
    import subprocess, sys
    completed = subprocess.run([sys.executable, '-c', 'print(4)'], capture_output=True, text=True, check=True)
    print(completed.stdout.strip(), completed.returncode)

correct Option: A. Output: 4 0

Solution: The child Python process prints 4 and exits successfully. With text=True, stdout is a string; strip removes its newline, and a successful process has return code 0.

## 90

Question:
    import weakref
    class Item: pass
    obj = Item()
    reference = weakref.ref(obj)
    print(reference() is obj)
    del obj
    print(reference() is None)

correct Option: A. Output: True then True

Solution: Initially the weak reference resolves to the same live object. After the only strong reference obj is deleted, the object is collectible and the weak reference returns None.

## 91

Question:
    from types import MappingProxyType
    data = {'x': 1}
    view = MappingProxyType(data)
    data['x'] = 2
    print(view['x'])
    try:
        view['y'] = 3
    except TypeError:
        print('read-only')

correct Option: A. Output: 2 then read-only

Solution: A mapping proxy is a read-only view, not a snapshot. It reflects the underlying dictionary’s update to 2, but assignment through the proxy raises TypeError.

## 92

Question:
    def make():
        data = {'count': 1}
        def read():
            return data['count']
        data['count'] = 2
        return read
    print(make()())

correct Option: A. Output: 2

Solution: read closes over the mutable dictionary itself. The dictionary is changed to count 2 before the closure is returned, so the later call reads 2.

## 93

Question:
    def f(x):
        return x if x > 0 else -x
    print(f(-4))

correct Option: A. Output: 4

Solution: Since -4 > 0 is false, the conditional expression chooses -x. Negating -4 gives 4.

## 94

Question:
    values = [1, 2, 3, 4]
    result = [value * 2 for value in values if value % 2 == 0]
    print(result)

correct Option: A. Output: [4, 8]

Solution: The filter keeps only even values 2 and 4. The expression doubles them, producing [4, 8].

## 95

Question:
    text = 'A\tB'
    print(len(text))
    print(text.split('\t'))

correct Option: A. Output: 3 then ['A', 'B']

Solution: The tab is one character, so the string has three characters: A, tab, and B. Splitting on the tab gives the two strings A and B.

## 96

Question:
    values = [True, 1, 1.0, 2]
    print(len(set(values)))
    print(True == 1 == 1.0)

correct Option: A. Output: 2 then True

Solution: True, 1, and 1.0 compare equal and have compatible hashes, so they occupy one set entry; 2 is the second. Chained equality confirms all three comparisons are true.

## 97

Question:
    class Box:
        def __init__(self, value):
            self.value = value
        def __bool__(self):
            return self.value > 0
    print(bool(Box(0)), bool(Box(2)))

correct Option: A. Output: False True

Solution: Python calls Box.__bool__ when converting each object to a Boolean. 0 > 0 is false, while 2 > 0 is true.

## 98

Question:
    def apply(fn, value):
        return fn(fn(value))
    print(apply(lambda x: x + 2, 3))

correct Option: A. Output: 7

Solution: The inner call computes 3 + 2 = 5. The outer call applies the same lambda again, computing 5 + 2 = 7.

## 99

Question:
    def make():
        return lambda value: value * 2
    fn = make()
    print(fn(6), callable(fn))

correct Option: A. Output: 12 True

Solution: The returned lambda doubles its argument, so fn(6) is 12. Functions and lambda objects can be called, making callable(fn) true.

## 100

Question:
    class User:
        def __init__(self, name):
            self.name = name
        def __repr__(self):
            return f'User({self.name!r})'
    print(User('Ana'))

correct Option: A. Output: User('Ana')

Solution: print uses the object’s string representation; because no __str__ is defined, the custom __repr__ is used. The !r conversion places quotes around the string name, producing User('Ana').

