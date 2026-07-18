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
