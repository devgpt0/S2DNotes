# 04 - Control Flow, Functions, Multiple Returns, and Defer

## `if`

```go
score := 75
if score >= 70 {
	fmt.Println("passed")
} else {
	fmt.Println("retry")
}
// Output: passed
```

An `if` can include a short initialization whose variable stays inside the branches:

```go
if value, err := strconv.Atoi("42"); err != nil {
	log.Fatal(err)
} else {
	fmt.Println(value)
}
// Output: 42
```

## `switch`

```go
role := "admin"
switch role {
case "admin":
	fmt.Println("manage")
case "learner":
	fmt.Println("read")
default:
	fmt.Println("unknown")
}
// Output: manage
```

Cases do not fall through by default. Type switches inspect interface dynamic types.

## `for`

```go
for index := 0; index < 3; index++ {
	fmt.Println(index)
}
// Output:
// 0
// 1
// 2
```

While-style:

```go
count := 0
for count < 2 {
	count++
}
fmt.Println(count)
// Output: 2
```

Infinite loop: `for {}`. Always define cancellation or termination for production workers.

## Range

```go
courses := []string{"Go", "Rust"}
for index, course := range courses {
	fmt.Println(index, course)
}
// Output:
// 0 Go
// 1 Rust
```

Do not rely on map iteration order. It is intentionally unspecified.

## Functions

```go
func label(id, title string) string {
	return id + ": " + title
}

fmt.Println(label("go", "Go"))
// Output: go: Go
```

Adjacent parameters of the same type can share the type.

## Multiple Returns

```go
func minMax(values []int) (int, int, error) {
	if len(values) == 0 {
		return 0, 0, errors.New("values cannot be empty")
	}
	minimum, maximum := values[0], values[0]
	for _, value := range values[1:] {
		if value < minimum {
			minimum = value
		}
		if value > maximum {
			maximum = value
		}
	}
	return minimum, maximum, nil
}

minimum, maximum, err := minMax([]int{3, 1, 5})
if err != nil {
	log.Fatal(err)
}
fmt.Println(minimum, maximum)
// Output: 1 5
```

Multiple returns make result-plus-error explicit. Avoid returning many unrelated values; use a struct when fields have domain meaning.

## Named Results

```go
func dimensions() (width int, height int) {
	width = 10
	height = 20
	return
}
```

Named results can clarify documentation and deferred error wrapping, but naked returns in long functions hide control flow. Prefer explicit returns.

## Variadic Functions

```go
func sum(values ...int) int {
	total := 0
	for _, value := range values {
		total += value
	}
	return total
}

fmt.Println(sum(10, 20, 30))
// Output: 60
```

## Functions Are Values

```go
func apply(operation func(int) int, value int) int {
	return operation(value)
}

double := func(value int) int { return value * 2 }
fmt.Println(apply(double, 5))
// Output: 10
```

## Closures

```go
func counter() func() int {
	count := 0
	return func() int {
		count++
		return count
	}
}

next := counter()
fmt.Println(next(), next())
// Output: 1 2
```

Captured variables can escape to the heap. Shared closure state needs synchronization if used by multiple goroutines.

## `defer`

Deferred calls run when the surrounding function returns, in last-in-first-out order.

```go
func demo() {
	defer fmt.Println("first deferred")
	defer fmt.Println("second deferred")
	fmt.Println("body")
}

demo()
// Output:
// body
// second deferred
// first deferred
```

Arguments are evaluated when `defer` is registered:

```go
value := 1
defer fmt.Println(value)
value = 2
// Deferred output: 1
```

Use defer immediately after acquiring a resource:

```go
file, err := os.Open(path)
if err != nil {
	return err
}
defer file.Close()
```

When close errors matter for writing, capture and combine them deliberately instead of silently discarding them.

## Production Rules

- use early returns for failures
- keep functions focused
- pass dependencies explicitly
- return structs for related named results
- use `defer` for lexical cleanup
- avoid hidden shared closure mutation
- do not launch goroutines from helpers without ownership/cancellation documentation
