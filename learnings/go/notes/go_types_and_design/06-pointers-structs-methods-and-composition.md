# 06 - Pointers, Structs, Methods, Embedding, and Composition

## Pointers

A pointer holds the address of a value. Go does not support pointer arithmetic.

```go
value := 10
pointer := &value
*pointer = 20
fmt.Println(value)
// Output: 20
```

- `&value`: address of value
- `*pointer`: value reached through pointer

## Value Copy

```go
type Point struct {
	X int
	Y int
}

first := Point{X: 1, Y: 2}
second := first
second.X = 99
fmt.Println(first.X, second.X)
// Output: 1 99
```

Struct assignment copies fields. Fields containing slices, maps, pointers, functions, or interfaces can still reference shared data.

## Struct Construction

```go
type Course struct {
	ID    string
	Title string
}

course := Course{ID: "go", Title: "Go"}
pointer := &Course{ID: "rust", Title: "Rust"}
fmt.Println(course.Title, pointer.Title)
// Output: Go Rust
```

Use keyed literals outside the defining package so adding/reordering fields does not silently change meaning.

## Constructors Are Functions

```go
func NewCourse(id, title string) (*Course, error) {
	if id == "" || title == "" {
		return nil, errors.New("id and title are required")
	}
	return &Course{ID: id, Title: title}, nil
}
```

Go has no constructor keyword. Use `NewType` only when creation validates invariants or configures dependencies. Otherwise a struct literal can be clearer.

## Value Receiver

```go
func (course Course) Label() string {
	return course.ID + ": " + course.Title
}
```

A value receiver gets a copy. It is suitable for small immutable-style values and methods that do not mutate receiver state.

## Pointer Receiver

```go
func (course *Course) Rename(title string) error {
	if title == "" {
		return errors.New("title is required")
	}
	course.Title = title
	return nil
}

course := Course{ID: "go", Title: "Old"}
if err := course.Rename("Go Foundations"); err != nil {
	log.Fatal(err)
}
fmt.Println(course.Title)
// Output: Go Foundations
```

Use pointer receivers to mutate, avoid copying large values, or keep the method set consistent. Do not mix receiver styles without a clear reason.

## Nil Pointer Receiver

Methods can receive nil pointers, but dereferencing panics. Either define meaningful nil behavior explicitly or fail before calls can occur. Do not hide invalid required dependencies behind nil-tolerant methods.

## Embedding

```go
type AuditFields struct {
	CreatedBy string
}

type Course struct {
	AuditFields
	ID    string
	Title string
}

course := Course{
	AuditFields: AuditFields{CreatedBy: "Asha"},
	ID: "go",
	Title: "Go",
}
fmt.Println(course.CreatedBy)
// Output: Asha
```

Embedding promotes fields/methods but is composition, not class inheritance. The embedded value still exists as a field.

## Composition and Dependency Injection

```go
type CourseStore interface {
	Save(context.Context, Course) error
}

type CourseService struct {
	store CourseStore
}

func NewCourseService(store CourseStore) (*CourseService, error) {
	if store == nil {
		return nil, errors.New("store is required")
	}
	return &CourseService{store: store}, nil
}
```

Dependencies enter through construction. The service owns business work; the store interface states only the capability needed.

## Struct Tags

```go
type CourseResponse struct {
	ID    string `json:"id"`
	Title string `json:"title"`
}
```

Tags are metadata read by packages such as `encoding/json`. They do not validate data by themselves.

## Comparability

Structs are comparable only when all fields are comparable. Slices, maps, and functions are not comparable except to nil.

Use explicit equality functions when domain equality differs from field-by-field comparison.

## Escape Analysis

The compiler decides whether values live on stack or heap according to escape analysis. Returning a pointer is safe; the compiler keeps the value alive.

Inspect decisions only during measured performance work:

```powershell
go build -gcflags=-m=2 ./...
```

## Expert Rules

- prefer values for small immutable-style data
- use pointers for mutation or identity
- keep constructors focused on invariants/dependencies
- use embedding deliberately
- define narrow consumer-owned interfaces
- do not optimize stack/heap placement by folklore
- avoid exposing mutable internal state
