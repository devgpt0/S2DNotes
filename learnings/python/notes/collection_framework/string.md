# `str` in Python
## 1. Core truth

A string is ordered text in Python.
It behaves like a sequence of characters, but it is immutable.

```python
text = "python"
print(text.upper())
```

Output:

```text
PYTHON
```

`upper()` returns a new string with uppercase letters.

## 2. String foundations

### Strings are immutable

```python
text = "cat"
print(text.replace("c", "b"))
print(text)
```

Output:

```text
bat
cat
```

### Slicing extracts parts

```python
text = "python"
print(text[0:3])
print(text[-3:])
```

Output:

```text
pyt
hon
```

### `split()` and `join()`

```python
text = "ana,raj,mia"
parts = text.split(",")
print(parts)
print(" | ".join(parts))
```

Output:

```text
['ana', 'raj', 'mia']
ana | raj | mia
```

## 3. String operations

- `upper()`
- `lower()`
- `strip()`
- `split()`
- `join()`
- `replace()`
- slicing

## 4. Practical text patterns

### Example 1: Clean text

```python
text = "  Ana  "
print(text.strip())
```

Output:

```text
Ana
```

### Example 2: Break text into parts

```python
text = "one,two,three"
print(text.split(","))
```

Output:

```text
['one', 'two', 'three']
```

### Example 3: Build a sentence

```python
words = ["hello", "world"]
print(" ".join(words))
```

Output:

```text
hello world
```

- cleaning user input;
- parsing simple text formats;
- formatting messages;
- creating readable output.

## 5. Text-handling mistakes

### Mistake 1: Expecting string methods to modify in place

They return new strings.

### Mistake 2: Confusing text and bytes

Text is `str`; binary data is `bytes`.

### Mistake 3: Forgetting to strip input

Whitespace often needs explicit removal before validation.

## 6. Text-type decision guide

| Need | Best choice | Why |
| --- | --- | --- |
| Text handling | `str` | immutable and expressive |
| Character list editing | list of chars | easier for complex edits |
| Binary data | `bytes` | not text |

## 7. Performance and validation

- strings are immutable, so repeated concatenation can cost more than building once;
- use explicit encoding when moving between text and bytes;
- validate external text before trusting it.

## 8. Advanced text behavior

- string formatting;
- Unicode awareness;
- normalization in text-heavy systems.

## 9. Mental model

| Method | Use |
| --- | --- |
| `upper()` | uppercase |
| `strip()` | remove outer whitespace |
| `split()` | break into pieces |
| `join()` | combine pieces |
| `replace()` | swap text |

## 10. Unicode-safe text handling

`lower()` is for display-oriented casing; `casefold()` is stronger and is the
better basis for caseless comparison.

```python
left = "Straße"
right = "STRASSE"
print(left.casefold() == right.casefold())
```

Output:

```text
True
```

Visually identical text can use different code-point sequences. Normalize only
when the business contract requires canonical equivalence.

```python
import unicodedata

composed = "é"
decomposed = "e\u0301"
print(composed == decomposed)
print(unicodedata.normalize("NFC", composed) == unicodedata.normalize("NFC", decomposed))
```

Output:

```text
False
True
```

Python indexes Unicode code points, not user-perceived grapheme clusters. Emoji
and combining sequences may occupy several indices; use a Unicode segmentation
library when cursor movement or visible-character limits matter.

## 11. Parsing and encoding boundaries

Use `partition()` when one delimiter split is required; it always returns three
parts and avoids an exception when the delimiter is missing.

```python
key, separator, value = "mode=fast".partition("=")
print(key, separator, value)
```

Output:

```text
mode = fast
```

Convert text to bytes with an explicit encoding and error policy. Default to
strict errors; replacement can silently corrupt identifiers or signatures.
