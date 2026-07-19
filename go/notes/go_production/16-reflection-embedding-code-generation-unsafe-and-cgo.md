# 16 - Reflection, Embedding, Code Generation, Unsafe, and CGO

Most Go programs should use ordinary functions, interfaces, and generics. This chapter explains the advanced tools you will encounter and the narrow cases where they are justified.

## Decision Order

```text
normal typed code -> small interface -> generics -> code generation -> reflection -> unsafe/CGO
```

Moving right increases build complexity, runtime uncertainty, or memory-safety responsibility. Use the leftmost tool that solves the real requirement clearly.

## Reflection in Simple Words

Reflection lets a program inspect a value's type and structure at runtime.

```go
package main

import (
	"fmt"
	"reflect"
)

func describe(value any) {
	if value == nil {
		fmt.Println("type=<nil>")
		return
	}
	typeInfo := reflect.TypeOf(value)
	valueInfo := reflect.ValueOf(value)
	fmt.Printf("type=%s kind=%s value=%v\n", typeInfo, typeInfo.Kind(), valueInfo.Interface())
}

func main() {
	describe(42)
	describe("Go")
	describe(nil)
}
```

Output:

```text
type=int kind=int value=42
type=string kind=string value=Go
type=<nil>
```

- `Type` describes a Go type.
- `Value` provides runtime access to one value.
- `Kind` is the underlying category, such as struct, slice, string, or pointer.
- `Interface` converts a valid, accessible reflected value back to `any`.

Always handle a nil interface before calling methods on its invalid reflected `Value`.

## Inspect Struct Fields and Tags

Libraries use reflection for formats such as JSON and for dependency or validation frameworks.

```go
package main

import (
	"fmt"
	"reflect"
)

type Course struct {
	ID    string `json:"id" required:"true"`
	Title string `json:"title" required:"true"`
}

func main() {
	typeInfo := reflect.TypeOf(Course{})
	for index := 0; index < typeInfo.NumField(); index++ {
		field := typeInfo.Field(index)
		fmt.Printf("%s -> json=%q required=%q\n",
			field.Name,
			field.Tag.Get("json"),
			field.Tag.Get("required"),
		)
	}
}
```

Output:

```text
ID -> json="id" required="true"
Title -> json="title" required="true"
```

Tags are string metadata. The compiler does not validate their spelling or meaning. The consuming library defines the contract.

## Change a Value Through Reflection

A reflected value is settable only when it refers to writable storage.

```go
package main

import (
	"fmt"
	"reflect"
)

func main() {
	name := "Go"
	value := reflect.ValueOf(&name).Elem()
	fmt.Println("settable:", value.CanSet())
	value.SetString("Rust")
	fmt.Println(name)
}
```

Output:

```text
settable: true
Rust
```

`ValueOf(name)` reflects a copy and is not settable. `ValueOf(&name).Elem()` reaches the original variable through its pointer.

Before calling a reflection operation, verify the required kind, validity, accessibility, and settable state. Incorrect reflective operations panic.

## Prefer Type Switches for a Closed Set

```go
func display(value any) string {
	switch typed := value.(type) {
	case string:
		return typed
	case int:
		return strconv.Itoa(typed)
	default:
		return "unsupported"
	}
}
```

A type switch is clearer and compiler-checked when the accepted types are known. Reflection is appropriate when the program truly works with arbitrary user-defined types, such as a serializer.

## Reflection Costs and Risks

- many mistakes become runtime panics instead of compile errors;
- field lookup and conversion add runtime work;
- refactoring tools understand reflected names poorly;
- unexported fields have access restrictions;
- nil pointers and invalid values require explicit handling;
- a generic reflective framework can hide simple control flow.

Measure reflection only if it appears in a real profile. Clarity is usually the first concern.

## Embed Files into a Binary

The `embed` package places selected files into the compiled program.

```text
web/
|-- assets.go
`-- templates/
    `-- index.html
```

```go
package web

import "embed"

//go:embed templates/index.html
var assets embed.FS

func IndexHTML() ([]byte, error) {
	return assets.ReadFile("templates/index.html")
}
```

The build fails if the pattern matches no file. Embedded content is read-only and increases binary size. Do not embed runtime secrets; anyone with the binary can potentially recover them.

Use `fs.Sub` when a consumer should see a subdirectory as its root.

## Build Constraints

Build constraints select files for a target or feature known at compile time.

```go
//go:build windows

package platform

const lineEnding = "\r\n"
```

The constraint must appear near the top of the file, followed by a blank line. A matching non-Windows file could use `//go:build !windows`.

Prefer filename suffixes such as `_windows.go` when they express the condition clearly. Test every supported build combination; code excluded on your machine can still be broken.

## Code Generation

Generation produces ordinary Go or data files before compilation. Go does not run generators automatically during `go build`.

```go
package status

//go:generate go run ./internal/cmd/genstatus -output status_string_gen.go

type Status uint8

const (
	StatusDraft Status = iota
	StatusPublished
)
```

Run:

```powershell
go generate ./...
gofmt -w .
go test ./...
git diff --exit-code
```

The generator command is resolved relative to the package directory. Pin external generator versions through the repository's tool-management policy, validate all generator input, write deterministic output, and add a generated-file header.

Generated code should normally be committed when consumers or builds should not need the generator toolchain. CI can regenerate and fail if the working tree changes.

Use generation for demonstrated mechanical repetition or external schemas. Do not generate code that a short readable function could replace.

## What `unsafe` Means

Package `unsafe` exposes operations outside Go's normal type and memory guarantees. The compiler and garbage collector rely on rules that unsafe code must preserve.

Common operations include:

- `unsafe.Sizeof`: size of a value's representation;
- `unsafe.Alignof`: required alignment;
- `unsafe.Offsetof`: field offset;
- `unsafe.Pointer`: pointer conversion boundary;
- `unsafe.Add`: checked-by-you pointer arithmetic;
- `unsafe.Slice`: construct a slice view from pointer and length.

## Inspect Layout

```go
package main

import (
	"fmt"
	"unsafe"
)

type Record struct {
	Active bool
	Count  int64
}

func main() {
	value := Record{}
	fmt.Println("size:", unsafe.Sizeof(value))
	fmt.Println("alignment:", unsafe.Alignof(value))
	fmt.Println("count offset:", unsafe.Offsetof(value.Count))
}
```

Example output on a common 64-bit target:

```text
size: 16
alignment: 8
count offset: 8
```

Layout is architecture- and compiler-dependent unless an external ABI explicitly defines it. Do not use this output as a portable serialization format.

## Unsafe Pointer Rule

Never store a Go pointer in `uintptr` across operations and expect the garbage collector to keep it valid. `uintptr` is an integer, not a tracked pointer.

Keep conversions in one expression where the documented pattern requires it, keep the original object alive for the complete access, preserve alignment and bounds, and use `runtime.KeepAlive` only when its precise lifetime semantics are understood.

Useful checks include:

```powershell
go test ./...
go test -race ./...
go test -gcflags=all=-d=checkptr=2 ./...
```

The race detector and pointer checker do not prove unsafe code correct. Keep the unsafe portion tiny, document its invariants, and expose a safe typed API only if the API can enforce those invariants.

## CGO

CGO lets Go call C code when `CGO_ENABLED=1` and a compatible C toolchain is installed.

```go
package main

/*
#include <stdlib.h>

static int add_scores(int left, int right) {
    return left + right;
}
*/
import "C"

import "fmt"

func main() {
	result := C.add_scores(C.int(40), C.int(2))
	fmt.Println(int(result))
}
```

Output:

```text
42
```

The comment immediately before `import "C"` is the C preamble. C types and Go types are distinct, so conversions are explicit.

## C Strings and Ownership

```go
package main

/*
#include <stdlib.h>
#include <string.h>
*/
import "C"

import (
	"fmt"
	"unsafe"
)

func main() {
	name := C.CString("Go")
	defer C.free(unsafe.Pointer(name))

	length := C.strlen(name)
	fmt.Println(uint64(length))
}
```

Output:

```text
2
```

`C.CString` allocates C memory. Go's garbage collector does not release it, so the matching `C.free` is required exactly once.

At every CGO boundary, document:

- who owns and frees memory;
- whether a pointer may be nil;
- how lengths and integer ranges convert;
- whether C retains a Go pointer after the call;
- which thread may call a function;
- how errors are returned;
- whether callbacks can enter Go concurrently.

Follow the current CGO pointer-passing rules. In particular, C must not keep a Go pointer after the call unless the documented pinning rules are satisfied, and C must not receive Go memory containing unpinned Go pointers.

## CGO Tradeoffs

- requires a C compiler and platform headers;
- makes cross-compilation and reproducible builds harder;
- calls cross a scheduler/runtime boundary;
- sanitizers and debuggers span two memory models;
- C crashes and memory corruption can terminate or corrupt the process;
- deployment must account for dynamic libraries and ABI compatibility.

Prefer a pure Go library when it meets the requirement. For a large or failure-prone native component, a separate process with a versioned protocol may provide a safer boundary.

## Final Rules

- use reflection only for genuinely dynamic types;
- validate kind and validity before reflective operations;
- use embedding for non-secret read-only build assets;
- test every supported build constraint;
- keep generation deterministic and reproducible;
- avoid unsafe unless measurement or interoperability requires it;
- document every unsafe memory invariant;
- define ownership and type conversion at CGO boundaries;
- test low-level code on every supported architecture and operating system;
- prefer simple typed Go whenever it can solve the problem.

