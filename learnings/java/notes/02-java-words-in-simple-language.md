# Java Words in Simple Language

Use this glossary whenever a chapter introduces an unfamiliar term.

## Basic Code Words

- **statement:** one instruction, such as `count++;`
- **expression:** code that produces a value, such as `price * 2`
- **variable:** a name holding one value
- **type:** the set of values and operations Java permits
- **method:** named behavior declared inside a type
- **parameter:** input name in a method declaration
- **argument:** actual value passed to a method
- **return value:** result sent back by a method
- **scope:** region where a name can be used
- **declaration:** introduces a name and its type, such as `int count`
- **initialization:** supplies a variable's first value
- **assignment:** replaces the value held by a variable
- **literal:** a value written directly in code, such as `42`, `true`, or `"Java"`
- **operator:** symbol that performs work, such as `+`, `==`, or `&&`
- **compile-time error:** invalid code rejected before the program runs
- **runtime exception:** failure that occurs while validly compiled code is running
- **API:** public types and operations another piece of code is allowed to use

## Words Used in Declarations

- **keyword:** reserved Java word with a fixed language meaning, such as `class` or `return`
- **modifier:** keyword that changes access or behavior, such as `public`, `static`, or `final`
- **public:** accessible from any package when the enclosing type is also accessible
- **private:** accessible only inside the declaring top-level class and its nested members
- **protected:** accessible in the same package and through subclass rules
- **static:** belongs to the class rather than to one object
- **final variable:** can be assigned only once; the referenced object may still be mutable
- **final method:** cannot be overridden
- **final class:** cannot be extended
- **void:** a method completes without returning a value
- **return:** ends a method and optionally sends a value to its caller
- **new:** creates an object or array and produces its reference
- **this:** the current object
- **super:** the superclass part of the current object or its constructor/member

## Object-Oriented Words

- **class:** definition used to create objects
- **object:** one runtime instance with state and behavior
- **field:** value stored by an object or class
- **constructor:** code that creates a valid object
- **encapsulation:** keep state protected and expose safe operations
- **invariant:** rule that must always remain true
- **inheritance:** a subtype receives/extends a parent contract
- **composition:** an object uses other objects to do its work
- **polymorphism:** different implementations can be used through one contract
- **interface:** a contract describing a capability
- **immutable:** cannot change after construction
- **override:** subtype supplies an implementation for an inherited instance-method contract
- **overload:** several methods share a name but have different parameter lists
- **abstract:** incomplete type or method intended to be completed by a subtype
- **record:** concise class for data-focused values with generated accessors and value contracts
- **sealed type:** explicitly restricts which types may extend or implement it

## Runtime Words

- **JDK:** tools used to develop and run Java
- **JVM:** runtime that executes Java bytecode
- **bytecode:** compiled JVM instructions in `.class` files
- **class loader:** component that locates and defines classes
- **stack frame:** execution state for one method call on one thread
- **heap:** memory area normally used for managed objects
- **garbage collection:** automatic recovery of unreachable object memory
- **JIT:** compiler that optimizes frequently executed code while the JVM runs
- **reference:** value that identifies an object; not an application-visible raw address
- **exception:** object describing an abnormal condition that changes normal control flow
- **checked exception:** exception the compiler requires code to catch or declare
- **unchecked exception:** `RuntimeException` family failure not forced into a method signature
- **resource:** something that must be released, such as a file, socket, or database connection

## Collection and Stream Words

- **collection:** object containing multiple elements
- **generic:** type parameter that provides compile-time type safety
- **iterator:** object that walks through elements
- **lambda:** small piece of behavior written as an expression
- **stream:** lazy pipeline for processing elements
- **intermediate operation:** builds a stream pipeline
- **terminal operation:** starts processing and produces a final result
- **reduction:** combines several values into one result

## Concurrency Words

- **thread:** one path of execution
- **concurrency:** tasks make progress during overlapping time
- **parallelism:** tasks execute at the same instant on different CPU capacity
- **race condition:** result depends on unsafe timing
- **atomic:** operation appears indivisible
- **visibility:** one thread can observe another thread's write
- **lock:** allows controlled exclusive access to shared state
- **deadlock:** tasks wait forever in a cycle
- **backpressure:** slow/reject producers when consumers cannot keep up
- **synchronized:** uses an object's monitor to provide mutual exclusion and visibility guarantees
- **volatile:** provides visibility and ordering for one field, but does not make compound actions atomic
- **happens-before:** Java Memory Model ordering that guarantees visibility of earlier actions
- **virtual thread:** lightweight JVM-managed thread suited to large numbers of blocking tasks

## Spring Words

- **bean:** object created and managed by Spring
- **dependency injection:** required collaborators are supplied from outside
- **application context:** Spring container holding bean definitions and instances
- **auto-configuration:** Boot creates useful beans when conditions match
- **proxy:** wrapper that intercepts method calls to add behavior
- **controller:** translates HTTP input/output
- **service:** owns an application use case or business operation
- **repository:** persistence boundary for loading/saving data
- **transaction:** group of data changes that commit or roll back together

## Distributed-System Words

- **idempotent:** repeating the same request has one logical effect
- **timeout:** maximum time allowed for an operation
- **retry:** repeat a safe transient failure
- **bulkhead:** isolate capacity so one failure cannot consume everything
- **circuit breaker:** temporarily stop calling a repeatedly failing dependency
- **eventual consistency:** replicas/read models may disagree temporarily but converge
- **outbox:** store business change and publish intent in one database transaction

## AI Words

- **model:** system that produces outputs from inputs
- **prompt:** messages/instructions sent to a model
- **token:** small unit used by a model for input/output accounting
- **embedding:** numeric vector representing semantic meaning
- **vector store:** database/index used to search embeddings
- **RAG:** retrieve relevant documents and include them as model context
- **tool calling:** model requests that application code execute an approved function
- **MCP:** standard protocol for exposing tools, resources, and prompts to AI clients
- **prompt injection:** untrusted text attempts to override intended instructions

## How to Decode an Unfamiliar Line

Read from the declared result outward:

```java
final List<String> names = new ArrayList<>();
System.out.println(names.isEmpty());
// Output: true
```

- `final`: `names` cannot later point to a different list.
- `List<String>`: the variable accepts a `List` whose elements are `String` values.
- `names`: variable name.
- `new ArrayList<>()`: creates the mutable list object; `<>` asks Java to infer `String`.
- `isEmpty()`: calls a method that returns whether the list has no elements.

If a chapter uses a word not listed here, first look for its definition immediately before the example. Then add the word to your own glossary in one sentence.
