# JSON

## 1. Core truth

JSON is a text format for structured data.
It is common because many languages and tools can read it.

```python
import json

data = '{"name": "Ana", "age": 30}'
obj = json.loads(data)
print(obj["name"])
```

Output:

```text
Ana
```

`loads()` converts JSON text into a Python dictionary.

## 2. JSON foundations

### `loads()` parses a string

```python
import json

text = '{"name": "Ana", "age": 30}'
obj = json.loads(text)
print(obj["age"])
```

Output:

```text
30
```

### `dumps()` serializes a Python object

```python
import json

obj = {"name": "Ana", "age": 30}
print(json.dumps(obj, sort_keys=True))
```

Output:

```text
{"age": 30, "name": "Ana"}
```

### Pretty printing helps debugging

```python
import json

obj = {"name": "Ana", "age": 30}
print(json.dumps(obj, indent=2, sort_keys=True))
```

Output:

```text
{
  "age": 30,
  "name": "Ana"
}
```

## 3. Parser and serializer APIs

- `json.loads(text)`
- `json.dumps(obj)`
- `json.load(file)`
- `json.dump(obj, file)`

```python
import json

obj = {"x": 1}
print(json.dumps(obj))
```

Output:

```text
{"x": 1}
```

## 4. Practical JSON processing

### Example 1: Parse a JSON string

```python
import json

data = '{"city": "Pune"}'
print(json.loads(data)["city"])
```

Output:

```text
Pune
```

### Example 2: Serialize a dictionary

```python
import json

data = {"city": "Pune"}
print(json.dumps(data))
```

Output:

```text
{"city": "Pune"}
```

### Example 3: Pretty print nested data

```python
import json

data = {"user": {"name": "Ana", "active": True}}
print(json.dumps(data, indent=2, sort_keys=True))
```

Output:

```text
{
  "user": {
    "active": true,
    "name": "Ana"
  }
}
```

- API request and response payloads;
- configuration files;
- logging structured events;
- exchanging nested data between systems.

## 5. JSON mistakes

### Mistake 1: Assuming every Python object is JSON serializable

`datetime`, sets, and custom objects often need conversion first.

### Mistake 2: Trusting JSON input without validation

External JSON should be checked before use.

### Mistake 3: Confusing JSON booleans and Python booleans

JSON uses lowercase `true` and `false`; Python uses `True` and `False`.

## 6. Format decision guide

| Need | Best choice | Why |
| --- | --- | --- |
| Nested structured text | JSON | portable and common |
| Human-edited config | JSON or YAML | readable, but validate carefully |
| Tabular rows | CSV | simpler for tables |

## 7. Validation and safety

- validate data after parsing;
- use stable key ordering when helpful for diffs;
- avoid serializing unsupported types without an explicit rule;
- keep JSON at system boundaries.

## 8. Advanced JSON behavior

- custom encoders;
- decoding into typed domain objects;
- file streaming for larger payloads.

## 9. Mental model

| Function | Use |
| --- | --- |
| `loads` | parse text |
| `dumps` | create text |
| `load` | read from file |
| `dump` | write to file |

## 10. Strict numeric behavior

The standard encoder accepts non-finite floats by default even though they are
outside interoperable JSON. Reject them with `allow_nan=False`.

```python
import json

try:
    json.dumps({"value": float("nan")}, allow_nan=False)
except ValueError as error:
    print(type(error).__name__)
```

Output:

```text
ValueError
```

Use `parse_float=Decimal` when decimal text must not first become a binary
floating-point value.

```python
import json
from decimal import Decimal

payload = json.loads('{"price": 0.1}', parse_float=Decimal)
print(type(payload["price"]).__name__)
print(payload["price"])
```

Output:

```text
Decimal
0.1
```

## 11. Duplicate keys and schema validation

JSON objects may contain duplicate names. The default decoder keeps the last
value. Reject duplicates when they make the request ambiguous.

```python
import json


def reject_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


try:
    json.loads('{"role": "user", "role": "admin"}', object_pairs_hook=reject_duplicates)
except ValueError as error:
    print(error)
```

Output:

```text
duplicate key: role
```

Parsing proves only that the JSON grammar is valid. Validate required keys,
types, ranges, lengths, and unknown-field policy separately without coercion.

## 12. Resource and interoperability limits

- Bound payload bytes and nesting depth before or during parsing.
- Stream newline-delimited JSON or use a streaming parser for large datasets;
  `json.load()` builds the entire value in memory.
- Use `ensure_ascii=False` for readable Unicode when the transport is UTF-8.
- Use stable separators and key ordering only when a protocol requires them;
  `sort_keys=True` alone is not a complete canonical-JSON specification.
- Never treat JSON as trusted merely because it cannot execute code directly.
