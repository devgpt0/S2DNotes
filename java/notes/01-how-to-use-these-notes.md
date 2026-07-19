# How to Learn Java with These Notes

You do not need to understand the whole repository at once.

## The Learning Loop

For every concept:

1. Read the simple meaning.
2. Type the example yourself.
3. Guess the output before running it.
4. Run it and compare the result.
5. Change one value and run it again.
6. Explain the concept in your own words.
7. Solve one small problem without copying.

Reading alone creates familiarity. Typing, predicting, debugging, and explaining create skill.

## The Learning Flow Inside a Chapter

Use the same order whenever a chapter contains code:

1. **Purpose:** identify the problem the feature solves.
2. **New words:** read the keyword meanings before the code.
3. **Small example:** type the smallest runnable program.
4. **Prediction:** write down what each print statement will show.
5. **Trace:** follow values and method calls one statement at a time.
6. **Output:** run the program and compare the real output with the prediction.
7. **Failure case:** make one invalid change and read the compiler or runtime error.
8. **Production rule:** learn when to use the feature and when a simpler choice is safer.
9. **Practice:** solve the checkpoint without copying.

Not every code block is a complete program. A block labelled **fragment** belongs inside a class or method. A block labelled **runnable example** contains everything needed to compile it.

## First Java Program

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello Java");
    }
}
// Output: Hello Java
```

Save it as `Hello.java`, then run:

```powershell
javac Hello.java
java Hello
# Output: Hello Java
```

### Read the Program One Keyword at a Time

- `public`: other code is allowed to access this declaration.
- `class`: declares a type that can contain data and methods.
- `static`: the method belongs to the class, so the JVM does not need a `Hello` object to call it.
- `void`: the method returns no value.
- `main`: the JVM's conventional application entry point.
- `String[] args`: an array containing command-line arguments.
- `System.out`: the standard output stream.
- `println`: prints a value and then ends the line.

For learning programs, `System.out.println` and `System.out.printf` make state visible. In production server code, use an application logger for operational events, HTTP responses for API results, and assertions for tests. Do not replace useful production logging with print statements.

## A Complete Predict-Run-Change Example

```java
public class LearningLoop {
    public static void main(String[] args) {
        int lessonsFinished = 2;
        int lessonsRemaining = 5 - lessonsFinished;

        System.out.printf("Finished: %d%n", lessonsFinished);
        System.out.printf("Remaining: %d%n", lessonsRemaining);
    }
}
// Output:
// Finished: 2
// Remaining: 3
```

Trace it:

1. `lessonsFinished` receives `2`.
2. Java evaluates `5 - 2` and stores `3` in `lessonsRemaining`.
3. `%d` is replaced by an integer; `%n` starts a new line on every operating system.

Now change `lessonsFinished` to `4`, predict both lines, and run it again.

## What to Ignore on the First Pass

When you see an advanced word such as proxy, bytecode, covariance, backpressure, isolation, advisor, or idempotency:

- read the simple definition once
- continue with the example
- do not memorize internal details yet
- return after completing the prerequisite chapters

## Beginner Path

1. Variables and data types
2. Conditions, loops, and methods
3. Strings, arrays, classes, and objects
4. OOP and exceptions
5. Lists, sets, maps, and queues
6. Generics and lambdas
7. Streams
8. Files, dates, and testing
9. Concurrency
10. Spring Boot

## How to Read Code

Read code in this order:

1. Find where execution begins.
2. Write down initial variable values.
3. Follow one statement at a time.
4. When a method is called, enter it and return with its result.
5. Track object mutation separately from variable reassignment.
6. Write every printed line in order.

## From Beginner to Expert

An expert does more than remember syntax. An expert can answer:

- Why does this feature exist?
- What guarantee does it provide?
- What can fail?
- Is the data valid and secure?
- What happens under load or concurrency?
- How will we test and observe it?
- When is a simpler solution better?

Take the modules in order. Interview and architecture chapters are revision material after the teaching chapters, not the starting point.

## Chapter Completion Check

Do not mark a chapter complete until you can:

- define its important words without copying
- predict the main example's output
- explain why each important line exists
- recognize one common failure
- write a smaller example from memory
- state one situation where you should not use the feature
