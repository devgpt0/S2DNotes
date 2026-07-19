# 03 - Variables, Constants, Types, Conversions, and Zero Values

## Declaration Forms

```go
var title string = "Go"
var lessons = 12
published := true
fmt.Println(title, lessons, published)
// Output: Go 12 true
```

Use `:=` inside functions when the inferred type is clear. Use `var` for zero-value declarations or when the explicit type improves the contract.

## Zero Values

Every variable has a value:

```go
var count int
var enabled bool
var name string
var pointer *int
fmt.Printf("%d %t %q %v\n", count, enabled, name, pointer)
// Output: 0 false "" <nil>
```

Design structs so the zero value is useful when practical. A zero `sync.Mutex` is ready to use; a nil map is readable but cannot accept assignments.

## Constants

```go
const maxRetries = 3
const serviceName = "course-api"
fmt.Println(serviceName, maxRetries)
// Output: course-api 3
```

Constants are compile-time values. Untyped constants can take a compatible type when used.

## `iota`

```go
type Level uint8

const (
	LevelBeginner Level = iota
	LevelIntermediate
	LevelAdvanced
)

fmt.Println(LevelBeginner, LevelIntermediate, LevelAdvanced)
// Output: 0 1 2
```

Use `iota` only when numeric identity is deliberate. For external protocols, assign stable explicit values and validate unknown input.

## Numeric Types

Go has signed/unsigned integers, architecture-sized `int`/`uint`, floating-point types, and complex types.

Prefer `int` for ordinary counts/indexes. Use fixed-width types for binary formats or protocol contracts.

```go
var count int64 = 9_000_000_000
var ratio float64 = 0.25
fmt.Println(count, ratio)
// Output: 9000000000 0.25
```

Check overflow and range at external conversions. Floating-point is not exact decimal money.

## Explicit Conversion

```go
count := 3
ratio := float64(count) / 2
fmt.Println(ratio)
// Output: 1.5
```

Go conversions do not always preserve value. Narrowing integers can truncate bits; string/integer conversions have specific semantics.

Parse text with `strconv`:

```go
value, err := strconv.Atoi("42")
if err != nil {
	log.Fatal(err)
}
fmt.Println(value)
// Output: 42
```

## Defined Types and Aliases

```go
type CourseID string
type Text = string

var id CourseID = "go-1"
fmt.Println(id)
// Output: go-1
```

- defined type: new distinct type with its own method set
- alias: another spelling for the same type

Use defined types for real domain distinctions, not every primitive.

## Booleans

Go does not treat integers, strings, or pointers as booleans:

```go
if len("Go") > 0 {
	fmt.Println("non-empty")
}
// Output: non-empty
```

## Strings, Bytes, and Runes

A string is an immutable byte sequence, commonly UTF-8 text. A rune is an alias for `int32` representing a Unicode code point.

```go
text := "Go語"
fmt.Println(len(text), utf8.RuneCountInString(text))
// Output: 5 3
```

`len` counts bytes, not user-perceived characters.

## Scope and Shadowing

```go
value := 10
if true {
	value := 20
	fmt.Println(value)
}
fmt.Println(value)
// Output:
// 20
// 10
```

The inner `:=` creates a new variable. Accidental shadowing is a common error, especially with `err`.

## Blank Identifier

`_` explicitly discards a value:

```go
value, _ := strconv.Atoi("42")
fmt.Println(value)
// Output: 42
```

Do not discard errors in production. Use `_` only when the ignored value is intentionally irrelevant and safe.

## Expert Rules

- choose domain types for semantic distinctions
- make conversion and parsing explicit
- understand byte vs rune vs grapheme behavior
- avoid unsigned integers merely to reject negatives
- check external ranges
- design useful zero values where possible
- watch `:=` shadowing during refactors
