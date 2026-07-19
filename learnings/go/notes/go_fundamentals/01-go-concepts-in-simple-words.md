# 01 - Go Concepts in Simple Words

## The One-Sentence Idea

A Go program groups typed values and functions into packages, compiles them into a native executable, and uses explicit errors and lightweight goroutines for reliable concurrent work.

## First Program

Save as `main.go`:

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, Go")
}
```

Run:

```powershell
go run .
# Output: Hello, Go
```

Read it line by line:

- `package main`: this file belongs to the executable package
- `import "fmt"`: use formatted input/output tools
- `func main()`: program entry point
- `fmt.Println`: print values followed by a newline

## Values and Variables

```go
package main

import "fmt"

func main() {
	course := "Go"
	lessons := 12
	fmt.Printf("%s has %d lessons\n", course, lessons)
}
// Output: Go has 12 lessons
```

`:=` declares and initializes a variable inside a function. Go infers `string` and `int` here.

## A Type Is a Rule

```go
var title string = "Go"
var published bool = true
var count int = 3
fmt.Println(title, published, count)
// Output: Go true 3
```

Go does not silently turn a string into an integer. Conversions are explicit and only allowed when the language defines them.

## Functions

```go
func double(number int) int {
	return number * 2
}

func main() {
	fmt.Println(double(5))
}
// Output: 10
```

- input: `number int`
- result type: the final `int`
- `return`: sends the result to the caller

## Conditions and Loops

```go
score := 80
if score >= 70 {
	fmt.Println("Passed")
}

for lesson := 1; lesson <= 3; lesson++ {
	fmt.Println(lesson)
}
// Output:
// Passed
// 1
// 2
// 3
```

Go has one loop keyword: `for`.

## Structs

A struct groups named fields:

```go
type Course struct {
	ID    string
	Title string
}

course := Course{ID: "go", Title: "Go Foundations"}
fmt.Println(course.Title)
// Output: Go Foundations
```

Capitalized names are exported from a package. Lowercase names stay package-private.

## Methods

```go
func (course Course) Label() string {
	return course.ID + ": " + course.Title
}

fmt.Println(course.Label())
// Output: go: Go Foundations
```

The receiver `(course Course)` connects the function to `Course` values.

## Interfaces

An interface describes behavior:

```go
type Labeler interface {
	Label() string
}

func printLabel(value Labeler) {
	fmt.Println(value.Label())
}
```

Types satisfy interfaces automatically by having the required methods. There is no `implements` keyword.

## Errors

Go commonly returns an error as a normal value:

```go
func divide(left, right int) (int, error) {
	if right == 0 {
		return 0, errors.New("right cannot be zero")
	}
	return left / right, nil
}

result, err := divide(10, 2)
if err != nil {
	log.Fatal(err)
}
fmt.Println(result)
// Output: 5
```

Handle an error where you can add context, choose a response, retry safely, or stop the operation.

## Slices and Maps

```go
courses := []string{"Go", "Rust"}
scores := map[string]int{"Asha": 90}
fmt.Println(courses[0], scores["Asha"])
// Output: Go 90
```

- slice: ordered variable-length view over an array
- map: key-to-value lookup

## Goroutines and Channels

```go
messages := make(chan string)
go func() {
	messages <- "finished"
}()
fmt.Println(<-messages)
// Output: finished
```

- `go`: start a function concurrently
- channel send: `messages <- value`
- channel receive: `<-messages`

Concurrency does not remove data races. Share state through clear ownership, channels, locks, or immutable values.

## Beginner to Expert Path

1. values, variables, control flow, functions
2. slices, maps, structs, methods, interfaces
3. errors, packages, tests, files, JSON
4. goroutines, channels, context, synchronization
5. HTTP, databases, security, profiling, operations

## Ready to Continue?

Predict the output:

```go
values := []int{1, 2, 3}
total := 0
for _, value := range values {
	total += value
}
fmt.Println(total)
// Output: 6
```
