from __future__ import annotations

import argparse
import json
import random
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Callable

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Flowable,
    KeepTogether,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


MODULES = ("list", "dict", "set", "tuple")
LEVELS = ("L1", "L2")
QTYPES = ("output", "mcq")

DEFAULT_DISTRIBUTION = {
    "list": {"L1": {"output": 8, "mcq": 5}, "L2": {"output": 20, "mcq": 2}},
    "dict": {"L1": {"output": 4, "mcq": 4}, "L2": {"output": 20, "mcq": 2}},
    "set": {"L1": {"output": 2, "mcq": 3}, "L2": {"output": 14, "mcq": 1}},
    "tuple": {"L1": {"output": 2, "mcq": 2}, "L2": {"output": 10, "mcq": 1}},
}


@dataclass(frozen=True)
class Question:
    module: str
    level: str
    qtype: str
    prompt: str
    concept: str
    code: str | None = None
    options: tuple[str, ...] | None = None


class AnswerLines(Flowable):
    """Draw lined answer area for hand-written responses."""

    def __init__(self, line_count: int, line_gap: float = 12.0) -> None:
        super().__init__()
        self.line_count = line_count
        self.line_gap = line_gap
        self.width = 0
        self.height = max(1, line_count) * line_gap

    def wrap(self, avail_width: float, _avail_height: float) -> tuple[float, float]:
        self.width = avail_width
        self.height = max(1, self.line_count) * self.line_gap
        return self.width, self.height

    def draw(self) -> None:
        self.canv.setStrokeColor(colors.HexColor("#9a9a9a"))
        self.canv.setLineWidth(0.5)
        y = self.height - self.line_gap + 2
        for _ in range(self.line_count):
            self.canv.line(0, y, self.width, y)
            y -= self.line_gap


def normalize_text(text: str) -> str:
    text = text.lower()
    text = text.replace("```python", "").replace("```text", "").replace("```", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


class SourceMatcher:
    """Rejects identical or highly similar questions against source worksheets."""

    def __init__(self, worksheet_paths: list[Path], threshold: float = 0.92) -> None:
        self.threshold = threshold
        units: list[str] = []
        full_text_parts: list[str] = []
        for path in worksheet_paths:
            if not path.exists():
                continue
            content = path.read_text(encoding="utf-8")
            full_text_parts.append(content)

            # Numbered questions in same line.
            units.extend(
                m.group(1).strip()
                for m in re.finditer(r"^\s*\d+\.\s+(.+?)\s*$", content, flags=re.M)
            )
            # Generic question lines.
            for line in content.splitlines():
                stripped = line.strip()
                if stripped.endswith("?") and len(stripped) > 8:
                    units.append(stripped)

        normalized_units = []
        seen = set()
        for u in units:
            n = normalize_text(u)
            if len(n) < 12:
                continue
            if n in seen:
                continue
            seen.add(n)
            normalized_units.append(n)

        self.units = normalized_units
        self.source_full = normalize_text("\n".join(full_text_parts))

    def is_too_similar(self, candidate: str) -> bool:
        n = normalize_text(candidate)
        if not n:
            return False
        if n in self.source_full:
            return True

        n_len = len(n)
        for unit in self.units:
            if abs(len(unit) - n_len) > 60:
                continue
            if SequenceMatcher(None, n, unit).ratio() >= self.threshold:
                return True
        return False


def validate_distribution(distribution: dict) -> None:
    for module in MODULES:
        if module not in distribution:
            raise ValueError(f"Missing module in distribution: {module}")
        for level in LEVELS:
            if level not in distribution[module]:
                raise ValueError(f"Missing level {level} for module {module}")
            for qtype in QTYPES:
                if qtype not in distribution[module][level]:
                    raise ValueError(f"Missing type {qtype} for {module}/{level}")
                v = distribution[module][level][qtype]
                if not isinstance(v, int) or v < 0:
                    raise ValueError(f"Invalid count for {module}/{level}/{qtype}: {v}")


def pick_words(seed: int, n: int) -> list[str]:
    words = ["red", "blue", "green", "gold", "black", "white", "cyan", "mint"]
    out = []
    for i in range(n):
        out.append(words[(seed + i * 2) % len(words)])
    return out


def rand_int_list(rng: random.Random, n: int, low: int = -5, high: int = 15) -> list[int]:
    return [rng.randint(low, high) for _ in range(n)]


# -----------------------------
# Output question patterns
# -----------------------------
def list_l1_patterns() -> list[Callable[[random.Random, int], tuple[str, str, str]]]:
    def p1(rng: random.Random, v: int) -> tuple[str, str, str]:
        nums = rand_int_list(rng, 6, 1, 30)
        a, b = rng.randint(1, 2), rng.randint(4, 6)
        return ("Predict the output of this slicing example.", f"nums = {nums}\nprint(nums[{a}:{b}])", "list_slice")

    def p2(rng: random.Random, v: int) -> tuple[str, str, str]:
        words = pick_words(v + 2, 5)
        return (
            "Predict the output (negative indexing).",
            f"items = {words}\nprint(items[-1], items[-3])",
            "list_negative_index",
        )

    def p3(rng: random.Random, v: int) -> tuple[str, str, str]:
        base = [rng.randint(1, 5), rng.randint(6, 10)]
        extra = [rng.randint(11, 15), rng.randint(16, 20)]
        return (
            "Predict the output after append and extend.",
            f"data = {base}\ndata.append({extra})\ndata.extend([{extra[0] + 10}, {extra[1] + 10}])\nprint(data)",
            "list_append_extend",
        )

    def p4(rng: random.Random, v: int) -> tuple[str, str, str]:
        vals = rand_int_list(rng, 5, 0, 9)
        idx = rng.randint(1, 3)
        val = rng.randint(50, 90)
        return (
            "Predict the output after insert and pop operations.",
            f"arr = {vals}\narr.insert({idx}, {val})\nprint(arr.pop({idx + 1}))\nprint(arr)",
            "list_insert_pop",
        )

    def p5(rng: random.Random, v: int) -> tuple[str, str, str]:
        x = rng.randint(2, 9)
        vals = [x, rng.randint(1, 9), x, rng.randint(1, 9), x]
        return (
            "Predict the output for count and index usage.",
            f"arr = {vals}\nprint(arr.count({x}), arr.index({x}, 1))",
            "list_count_index",
        )

    def p6(rng: random.Random, v: int) -> tuple[str, str, str]:
        vals = rand_int_list(rng, 4, 1, 12)
        return (
            "Predict the output for aliasing behavior.",
            f"a = {vals}\nb = a\nb[0] = b[0] + 100\nprint(a)\nprint(b)",
            "list_aliasing",
        )

    def p7(rng: random.Random, v: int) -> tuple[str, str, str]:
        vals = [[1, 2], [3, 4], [5, 6]]
        return (
            "Predict the output for shallow copy on nested list.",
            f"a = {vals}\nb = a.copy()\nb[1][0] = {90 + (v % 7)}\nprint(a)\nprint(b)",
            "list_shallow_nested",
        )

    def p8(rng: random.Random, v: int) -> tuple[str, str, str]:
        vals = rand_int_list(rng, 5, -12, 12)
        return (
            "Predict the output for sort vs sorted.",
            f"nums = {vals}\nout = sorted(nums, key=abs)\nnums.sort(reverse=True)\nprint(out)\nprint(nums)",
            "list_sort_sorted",
        )

    def p9(rng: random.Random, v: int) -> tuple[str, str, str]:
        vals = pick_words(v + 3, 4)
        return (
            "Predict the output for reversed iteration.",
            f"tokens = {vals}\nprint(list(reversed(tokens)))\ntokens.reverse()\nprint(tokens)",
            "list_reverse",
        )

    def p10(rng: random.Random, v: int) -> tuple[str, str, str]:
        vals = rand_int_list(rng, 6, 1, 9)
        rm_start = rng.randint(1, 2)
        rm_end = rm_start + 2
        return (
            "Predict the output after deleting a slice.",
            f"nums = {vals}\ndel nums[{rm_start}:{rm_end}]\nprint(nums)\nprint({rng.randint(1,9)} in nums)",
            "list_del_slice",
        )

    return [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]


def list_l2_patterns() -> list[Callable[[random.Random, int], tuple[str, str, str]]]:
    def p1(rng: random.Random, v: int) -> tuple[str, str, str]:
        vals = rand_int_list(rng, 6, 1, 12)
        return (
            "Predict the output for combined filtering and indexed transformation.",
            f"nums = {vals}\nout = [(i, x * x) for i, x in enumerate(nums) if x % 2 == 1]\nprint(out[-2:])",
            "list_comp_filter_map",
        )

    def p2(rng: random.Random, v: int) -> tuple[str, str, str]:
        mat = [[rng.randint(1, 4), rng.randint(5, 8)] for _ in range(3)]
        return (
            "Predict the output for nested flattening with conditional selection.",
            f"matrix = {mat}\nflat = [x for row in matrix for x in row if x % 2 == 0]\nprint(flat)\nprint(sum(flat))",
            "list_flatten",
        )

    def p3(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output for matrix creation pitfall.",
            "grid = [[0] * 3] * 2\ngrid[0][1] = 9\nprint(grid)",
            "list_matrix_alias_bug",
        )

    def p4(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output for deep copy in nested list.",
            "import copy\nsrc = [[1], [2]]\ncloned = copy.deepcopy(src)\ncloned[0].append(7)\nprint(src)\nprint(cloned)",
            "list_deepcopy",
        )

    def p5(rng: random.Random, v: int) -> tuple[str, str, str]:
        vals = rand_int_list(rng, 5, 1, 20)
        return (
            "Predict the output using starred unpacking.",
            f"nums = {vals}\nfirst, *mid, last = nums\nprint(first)\nprint(mid)\nprint(last)",
            "list_star_unpack",
        )

    def p6(rng: random.Random, v: int) -> tuple[str, str, str]:
        a0 = 10 + (v % 5)
        return (
            "Predict the output for zip truncation and zip_longest padding.",
            f"from itertools import zip_longest\na = [{a0}, {a0 + 10}, {a0 + 20}]\nb = ['x', 'y']\nprint(list(zip(a, b)))\nprint(list(zip_longest(a, b, fillvalue='NA')))",
            "list_zip_enum",
        )

    def p7(rng: random.Random, v: int) -> tuple[str, str, str]:
        data = [("p", rng.randint(50, 90)), ("q", rng.randint(50, 90)), ("r", rng.randint(50, 90))]
        return (
            "Predict the output for sorting by a tuple key.",
            f"items = {data}\nprint(sorted(items, key=lambda x: (x[1], x[0])))",
            "list_sort_lambda",
        )

    def p8(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output of next() with fallback after generator filtering.",
            "names = ['arya', 'neo', 'trinity', 'nora']\ng = (x.upper() for x in names if x.startswith('n'))\nprint(next(g, 'NA'))\nprint(next(g, 'NA'))\nprint(next(g, 'NA'))",
            "list_next_default",
        )

    return [p1, p2, p3, p4, p5, p6, p7, p8]


def dict_l1_patterns() -> list[Callable[[random.Random, int], tuple[str, str, str]]]:
    def p1(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output for get with default values.",
            "profile = {'name': 'Ana', 'score': 88}\nprint(profile.get('score'))\nprint(profile.get('city', 'NA'))",
            "dict_get_default",
        )

    def p2(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output when direct missing key access is handled.",
            "d = {'a': 1}\ntry:\n    print(d['b'])\nexcept KeyError:\n    print('missing')",
            "dict_missing_key_try",
        )

    def p3(rng: random.Random, v: int) -> tuple[str, str, str]:
        a, b = rng.randint(1, 7), rng.randint(8, 15)
        return (
            "Predict the output after update and merge.",
            f"d = {{'x': {a}, 'y': {b}}}\nd.update({{'y': {b + 10}, 'z': {a + b}}})\nprint(d)",
            "dict_update",
        )

    def p4(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output for dictionary merge operator.",
            "left = {'a': 1, 'k': 5}\nright = {'k': 9, 'b': 2}\nprint(left | right)",
            "dict_merge_pipe",
        )

    def p5(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output for pop and remaining dictionary.",
            "d = {'p': 10, 'q': 20, 'r': 30}\nprint(d.pop('q'))\nprint(d)",
            "dict_pop",
        )

    def p6(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output for setdefault behavior.",
            "d = {'a': 1}\nprint(d.setdefault('a', 99))\nprint(d.setdefault('b', 50))\nprint(d)",
            "dict_setdefault",
        )

    def p7(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output for fromkeys with mutable default.",
            "d = dict.fromkeys(['x', 'y'], [])\nd['x'].append(1)\nprint(d)",
            "dict_fromkeys_mutable",
        )

    def p8(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output for membership in dictionary.",
            "d = {'id': 101, 'age': 22}\nprint('id' in d)\nprint(22 in d)",
            "dict_membership",
        )

    def p9(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output for dynamic keys view.",
            "d = {'a': 1}\nkv = d.keys()\nprint(kv)\nd['b'] = 2\nprint(kv)",
            "dict_dynamic_view",
        )

    def p10(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output for shallow copy with nested list.",
            "d1 = {'scores': [10, 20]}\nd2 = d1.copy()\nd2['scores'].append(30)\nprint(d1)\nprint(d2)",
            "dict_shallow_copy",
        )

    def p11(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output for key/value/item iteration.",
            "d = {'a': 1, 'b': 2}\nfor k, v in d.items():\n    print(k, v, end=' | ')\nprint()",
            "dict_iteration",
        )

    def p12(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output for dictionary comprehension.",
            "sq = {x: x * x for x in range(5) if x % 2 == 1}\nprint(sq)",
            "dict_comp",
        )

    return [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12]


def dict_l2_patterns() -> list[Callable[[random.Random, int], tuple[str, str, str]]]:
    def p1(rng: random.Random, v: int) -> tuple[str, str, str]:
        txt = "".join(chr(97 + ((v + i) % 3)) for i in range(5))
        return (
            "Predict the output for defaultdict(int) counting.",
            f"from collections import defaultdict\nfreq = defaultdict(int)\nfor ch in '{txt}':\n    freq[ch] += 1\nprint(dict(freq))",
            "dict_defaultdict_count",
        )

    def p2(rng: random.Random, v: int) -> tuple[str, str, str]:
        base = 2 + (v % 4)
        return (
            "Predict the output using Counter.",
            f"from collections import Counter\nc = Counter([{base}, {base}, {base + 1}, {base + 1}, {base + 1}, {base + 2}])\nprint(c)\nprint(c.most_common(1))",
            "dict_counter",
        )

    def p3(rng: random.Random, v: int) -> tuple[str, str, str]:
        theme_a = "light" if v % 2 == 0 else "solarized"
        theme_b = "dark" if v % 2 == 0 else "midnight"
        return (
            "Predict the output for ChainMap lookup order.",
            f"from collections import ChainMap\ncfg = ChainMap({{'theme': '{theme_a}'}}, {{'theme': '{theme_b}', 'lang': 'en'}})\nprint(cfg['theme'], cfg['lang'])",
            "dict_chainmap",
        )

    def p4(rng: random.Random, v: int) -> tuple[str, str, str]:
        a = 1 + (v % 7)
        return (
            "Predict the output for MappingProxyType view.",
            f"from types import MappingProxyType\nbase = {{'a': {a}}}\nview = MappingProxyType(base)\nbase['a'] = {a + 8}\nprint(view['a'])",
            "dict_mappingproxy",
        )

    def p5(rng: random.Random, v: int) -> tuple[str, str, str]:
        a = 1 + (v % 6)
        return (
            "Predict the output for dict key collision of bool/int.",
            f"d = {{}}\nd[{a}] = 'int-like'\nd[{float(a)}] = 'float-like'\nprint(d)\nprint(len(d))",
            "dict_key_collision",
        )

    def p6(rng: random.Random, v: int) -> tuple[str, str, str]:
        x = 8 + (v % 7)
        y = 2 + (v % 5)
        return (
            "Predict the output for dispatch table call.",
            f"def add(a, b):\n    return a + b\n\ndef sub(a, b):\n    return a - b\nops = {{'+': add, '-': sub}}\nprint(ops['+']({x}, {y}), ops['-']({x}, {y}))",
            "dict_dispatch",
        )

    def p7(rng: random.Random, v: int) -> tuple[str, str, str]:
        x = 1 + (v % 4)
        return (
            "Predict the output for sorting dict items by value.",
            f"d = {{'x': {x + 2}, 'y': {x}, 'z': {x + 1}}}\nout = sorted(d.items(), key=lambda kv: kv[1], reverse=True)\nprint(out)",
            "dict_sort_items",
        )

    return [p1, p2, p3, p4, p5, p6, p7]


def set_l1_patterns() -> list[Callable[[random.Random, int], tuple[str, str, str]]]:
    def p1(rng: random.Random, v: int) -> tuple[str, str, str]:
        a = 1 + (v % 4)
        b = a + 1
        c = b + 1
        return (
            "Predict the output for duplicate removal in set.",
            f"s = {{{a}, {b}, {b}, {c}, {c}, {c + 1}}}\nprint(s)\nprint(len(s))",
            "set_unique",
        )

    def p2(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output for empty dict vs empty set.",
            "a = {}\nb = set()\nprint(type(a).__name__, type(b).__name__)",
            "set_empty_creation",
        )

    def p3(rng: random.Random, v: int) -> tuple[str, str, str]:
        x = 2 + (v % 5)
        return (
            "Predict the output for add and update.",
            f"s = {{{x}, {x + 1}}}\ns.add({x + 1})\ns.update([{x + 2}, {x + 3}], ({x + 3}, {x + 4}))\nprint(s)",
            "set_add_update",
        )

    def p4(rng: random.Random, v: int) -> tuple[str, str, str]:
        x = 10 + (v % 6) * 5
        return (
            "Predict the output for remove/discard handling.",
            f"s = {{{x}, {x + 10}, {x + 20}}}\ntry:\n    s.remove({x + 99})\nexcept KeyError:\n    print('keyerror')\ns.discard({x + 99})\nprint(s)",
            "set_remove_discard",
        )

    def p5(rng: random.Random, v: int) -> tuple[str, str, str]:
        z = 1 + (v % 4)
        return (
            "Predict the output for set operations.",
            f"a = {{{z}, {z + 1}, {z + 2}}}\nb = {{{z + 2}, {z + 3}, {z + 4}}}\nprint(a | b)\nprint(a & b)\nprint(a ^ b)",
            "set_ops",
        )

    def p6(rng: random.Random, v: int) -> tuple[str, str, str]:
        z = 2 + (v % 5)
        return (
            "Predict the output for subset and disjoint checks.",
            f"a = {{{z}, {z + 1}}}\nb = {{{z}, {z + 1}, {z + 2}}}\nc = {{{z + 10}, {z + 11}}}\nprint(a.issubset(b), a.isdisjoint(c))",
            "set_relations",
        )

    def p7(rng: random.Random, v: int) -> tuple[str, str, str]:
        start = v % 3
        return (
            "Predict the output for set comprehension.",
            f"s = {{x * x for x in range({start}, {start + 8}) if x % 2 == 0}}\nprint(s)",
            "set_comprehension",
        )

    def p8(rng: random.Random, v: int) -> tuple[str, str, str]:
        x = 1 + (v % 5)
        return (
            "Predict the output for truthiness with any/all.",
            f"s = {{0, {x}, {x + 1}}}\nprint(any(s), all(s))",
            "set_any_all",
        )

    def p9(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output for bool/int behavior in a set.",
            "s = {True, 1, 2, 0, False}\nprint(s)\nprint(len(s))",
            "set_bool_int",
        )

    def p10(rng: random.Random, v: int) -> tuple[str, str, str]:
        b = 1 + (v % 4)
        return (
            "Predict the output for frozenset basics.",
            f"fs = frozenset([{b}, {b + 1}, {b + 1}, {b + 2}])\nprint(fs)\nprint(type(fs).__name__)",
            "set_frozenset",
        )

    return [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]


def set_l2_patterns() -> list[Callable[[random.Random, int], tuple[str, str, str]]]:
    def p1(rng: random.Random, v: int) -> tuple[str, str, str]:
        b = 1 + (v % 4)
        return (
            "Predict the output with operator precedence in set expressions.",
            f"a = {{{b}, {b + 1}, {b + 2}}}\nb = {{{b + 1}, {b + 2}, {b + 3}}}\nc = {{{b + 2}, {b + 3}, {b + 4}}}\nprint(a | b & c)\nprint((a | b) & c)",
            "set_precedence",
        )

    def p2(rng: random.Random, v: int) -> tuple[str, str, str]:
        b = 1 + (v % 5)
        return (
            "Predict the output for in-place update return values.",
            f"s = {{{b}, {b + 1}, {b + 2}, {b + 3}}}\nprint(s.difference_update({{{b + 1}, {b + 3}}}))\nprint(s)",
            "set_update_return",
        )

    def p3(rng: random.Random, v: int) -> tuple[str, str, str]:
        b = 1 + (v % 4)
        return (
            "Predict the output for nested-loop set comprehension.",
            f"matrix = [[{b}, {b + 1}], [{b + 1}, {b + 2}], [{b + 2}, {b + 3}]]\nflat = {{x for row in matrix for x in row}}\nprint(flat)",
            "set_flatten_unique",
        )

    def p4(rng: random.Random, v: int) -> tuple[str, str, str]:
        b = 1 + (v % 4)
        return (
            "Predict the output for first-duplicate detection.",
            f"nums = [{b + 4}, {b}, {b + 2}, {b + 1}, {b + 2}, {b + 3}, {b + 1}]\nseen = set()\nfirst_dup = None\nfor x in nums:\n    if x in seen:\n        first_dup = x\n        break\n    seen.add(x)\nprint(first_dup)",
            "set_first_duplicate",
        )

    def p5(rng: random.Random, v: int) -> tuple[str, str, str]:
        b = 1 + (v % 6)
        return (
            "Predict the output for relation operators on sets.",
            f"a = {{{b}, {b + 1}}}\nb = {{{b}, {b + 1}, {b + 2}}}\nprint(a <= b, a < b)\nprint(b >= a, b > a)",
            "set_relation_operators",
        )

    return [p1, p2, p3, p4, p5]


def tuple_l1_patterns() -> list[Callable[[random.Random, int], tuple[str, str, str]]]:
    def p1(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output for single-element tuple syntax.",
            "a = (7)\nb = (7,)\nprint(type(a).__name__, type(b).__name__)",
            "tuple_single_element",
        )

    def p2(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output for tuple packing/unpacking.",
            "t = 10, 20, 30\nx, y, z = t\nprint(x + y + z)",
            "tuple_unpack",
        )

    def p3(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output for extended unpacking.",
            "t = (1, 2, 3, 4, 5)\nfirst, *mid, last = t\nprint(first)\nprint(mid)\nprint(last)",
            "tuple_extended_unpack",
        )

    def p4(rng: random.Random, v: int) -> tuple[str, str, str]:
        vals = tuple(rand_int_list(rng, 5, 1, 9))
        return (
            "Predict the output for slicing and reverse slicing.",
            f"t = {vals}\nprint(t[1:4])\nprint(t[::-1])",
            "tuple_slice",
        )

    def p5(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output for tuple operators.",
            "print((1, 2) + (3, 4))\nprint((1, 2) * 2)",
            "tuple_ops",
        )

    def p6(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output for tuple methods.",
            "t = (1, 2, 2, 3, 2)\nprint(t.count(2), t.index(3))",
            "tuple_methods",
        )

    def p7(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output showing mutable inner object in tuple.",
            "t = ([1, 2], [3, 4])\nt[0].append(9)\nprint(t)",
            "tuple_mutable_inner",
        )

    def p8(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict the output for tuple hashability as dict key.",
            "d = {(1, 2): 'pt'}\nprint(d[(1, 2)])\nprint((1, 2, 3) in d)",
            "tuple_hashable_key",
        )

    return [p1, p2, p3, p4, p5, p6, p7, p8]


def tuple_l2_patterns() -> list[Callable[[random.Random, int], tuple[str, str, str]]]:
    def p1(rng: random.Random, v: int) -> tuple[str, str, str]:
        y = 5 + (v % 7)
        return (
            "Predict the output for tuple pattern matching.",
            f"point = (0, {y})\nmatch point:\n    case (0, y):\n        print('Y', y)\n    case (x, 0):\n        print('X', x)\n    case _:\n        print('O')",
            "tuple_match_case",
        )

    def p2(rng: random.Random, v: int) -> tuple[str, str, str]:
        b = 2 + (v % 6)
        return (
            "Predict the output for copy behavior with nested tuple data.",
            f"import copy\nt1 = (1, [{b}, {b + 1}])\nt2 = copy.copy(t1)\nt3 = copy.deepcopy(t1)\nt1[1].append({b + 6})\nprint(t2)\nprint(t3)",
            "tuple_copy",
        )

    def p3(rng: random.Random, v: int) -> tuple[str, str, str]:
        a = 3 + (v % 6)
        b = 7 + (v % 5)
        return (
            "Predict the output for function return unpacking and starred target.",
            f"def get_data():\n    return {a}, {b}, {b + 3}, {a + 2}\nfirst, *mid, last = get_data()\nprint(first)\nprint(mid)\nprint(last)",
            "tuple_func_return",
        )

    def p4(rng: random.Random, v: int) -> tuple[str, str, str]:
        a = 4 + (v % 5)
        return (
            "Predict the output for reversed/sorted behavior and tuple identity slice.",
            f"t = ({a + 1}, {a - 3}, {a - 1})\nprint(tuple(reversed(t)))\nprint(sorted(t))\nprint(t[:] is t)",
            "tuple_sorted_reversed",
        )

    return [p1, p2, p3, p4]


# -----------------------------
# MCQ banks (single correct option)
# -----------------------------
MCQ_BANK: dict[str, dict[str, list[tuple[str, tuple[str, str, str, str], str]]]] = {
    "list": {
        "L1": [
            ("Which operation adds each element of another iterable to an existing list?", ("A) append", "B) extend", "C) insert", "D) remove"), "list_extend"),
            ("When `b = a` for lists, what is true?", ("A) `b` is a deep copy", "B) `b` points to same object", "C) `b` is immutable copy", "D) `b` is tuple"), "list_alias"),
            ("Which statement about `sorted(lst)` is correct?", ("A) It mutates `lst` in-place", "B) It returns a new sorted list", "C) It returns `None`", "D) It works only on int lists"), "list_sorted"),
            ("Which complexity is typical for `x in my_list`?", ("A) O(1)", "B) O(log n)", "C) O(n)", "D) O(n log n)"), "list_membership_complexity"),
            ("What does `lst.pop()` do by default?", ("A) Removes first element", "B) Removes last element and returns it", "C) Removes all duplicates", "D) Returns index of max"), "list_pop"),
            ("Which is the safer matrix initialization?", ("A) `[[0]*m]*n`", "B) `[[0 for _ in range(m)] for _ in range(n)]`", "C) `list(0)`", "D) `[0,0]*n`"), "list_matrix_safe"),
            ("What does `a[1:1]` return for a list?", ("A) IndexError", "B) The element at index 1", "C) Empty list", "D) None"), "list_empty_slice"),
        ],
        "L2": [
            ("`zip(a, b)` with different lengths stops at:", ("A) Longest iterable", "B) Shortest iterable", "C) Raises ValueError", "D) Pads with zeros automatically"), "list_zip"),
            ("Which operation keeps original list unchanged while sorting with custom key?", ("A) `lst.sort(key=...)`", "B) `sorted(lst, key=...)`", "C) `lst.reverse()`", "D) `reversed(lst)`"), "list_sorted_key"),
            ("If `a = [1,2]`, which statement usually creates a new list object?", ("A) `a += [3]`", "B) `a.append(3)`", "C) `a = a + [3]`", "D) `a.extend([3])`"), "list_new_object_plus"),
            ("What does `reversed(lst)` return?", ("A) New reversed list", "B) Iterator", "C) None", "D) Tuple"), "list_reversed"),
        ],
    },
    "dict": {
        "L1": [
            ("For optional lookup, which is safest?", ("A) `d[k]`", "B) `d.get(k, default)`", "C) `del d[k]`", "D) `d.popitem()`"), "dict_get"),
            ("In dictionaries, `in` checks membership of:", ("A) Values", "B) Key-value tuples", "C) Keys", "D) Indices"), "dict_in"),
            ("Which key type is invalid for dict keys?", ("A) tuple of ints", "B) string", "C) list", "D) int"), "dict_hashable"),
            ("What does `d.copy()` create for nested mutable values?", ("A) Deep copy", "B) Shallow copy", "C) Read-only proxy", "D) No copy"), "dict_shallow_copy"),
            ("In `d1 | d2`, duplicate keys are taken from:", ("A) d1", "B) d2", "C) both in list", "D) random side"), "dict_merge_right_wins"),
            ("`dict.fromkeys(keys, [])` can be risky because:", ("A) It is very slow", "B) It rejects list values", "C) Same list is shared across keys", "D) It sorts keys automatically"), "dict_fromkeys_pitfall"),
        ],
        "L2": [
            ("Best built-in for frequency counting is:", ("A) `itertools.groupby` only", "B) `collections.Counter`", "C) `setdefault` only", "D) `heapq`"), "dict_counter_mcq"),
            ("In `ChainMap(a, b)`, lookup order is:", ("A) b then a", "B) a then b", "C) random", "D) sorted by key"), "dict_chainmap_mcq"),
            ("`keys_view = d.keys()` then adding a key to `d` means:", ("A) `keys_view` stays unchanged", "B) `keys_view` updates dynamically", "C) error is raised", "D) `keys_view` becomes list"), "dict_keys_dynamic"),
            ("Changing dict size while iterating directly may raise:", ("A) KeyError", "B) RuntimeError", "C) TypeError", "D) ImportError"), "dict_iter_mutation"),
        ],
    },
    "set": {
        "L1": [
            ("Which method removes an element without error if missing?", ("A) remove", "B) discard", "C) pop", "D) clear"), "set_discard"),
            ("Main strength of set in DSA problems:", ("A) Indexing", "B) Stable order", "C) Fast membership checks", "D) Key-value mapping"), "set_lookup"),
            ("What creates an empty set?", ("A) `{}`", "B) `[]`", "C) `set()`", "D) `()`"), "set_empty"),
            ("Set elements must be:", ("A) Mutable", "B) Hashable", "C) Sorted", "D) Numeric"), "set_hashable"),
        ],
        "L2": [
            ("Average complexity of set intersection is near:", ("A) O(1)", "B) O(min(len(a), len(b)))", "C) O(n^2)", "D) O(log n)"), "set_intersection_complexity"),
            ("In expression `a | b & c`, which operation happens first?", ("A) Union `|`", "B) Intersection `&`", "C) Left-to-right only", "D) Symmetric difference"), "set_precedence_mcq"),
            ("`symmetric_difference` returns:", ("A) only common items", "B) only left-only items", "C) items in either set but not both", "D) sorted union"), "set_symdiff"),
        ],
    },
    "tuple": {
        "L1": [
            ("Correct one-element tuple syntax is:", ("A) `(5)`", "B) `[5,]`", "C) `(5,)`", "D) `{5}`"), "tuple_single"),
            ("Tuples are usually preferred when data is:", ("A) frequently appended", "B) fixed-shape record", "C) key-value mapping", "D) unordered unique collection"), "tuple_use_case"),
            ("`*args` inside function is collected as:", ("A) dict", "B) tuple", "C) list", "D) set"), "tuple_args"),
        ],
        "L2": [
            ("A tuple can be dict key when:", ("A) length is 2", "B) all elements are hashable", "C) it contains list", "D) it is sorted"), "tuple_hashable_rule"),
            ("For immutable-only tuple `t`, which is commonly true in CPython?", ("A) `t[:] is t` can be True", "B) `t[:]` always creates deep copy", "C) `t[:]` returns list", "D) slicing tuple is invalid"), "tuple_slice_identity"),
            ("Most accurate tuple immutability statement:", ("A) tuple and nested objects are deeply frozen", "B) tuple structure is fixed; inner mutables may change", "C) tuples are mutable in Python 3", "D) tuple cannot contain lists"), "tuple_immutability_depth"),
        ],
    },
}


def get_output_patterns(module: str, level: str) -> list[Callable[[random.Random, int], tuple[str, str, str]]]:
    mapping = {
        ("list", "L1"): list_l1_patterns(),
        ("list", "L2"): list_l2_patterns(),
        ("dict", "L1"): dict_l1_patterns(),
        ("dict", "L2"): dict_l2_patterns(),
        ("set", "L1"): set_l1_patterns(),
        ("set", "L2"): set_l2_patterns(),
        ("tuple", "L1"): tuple_l1_patterns(),
        ("tuple", "L2"): tuple_l2_patterns(),
    }
    return mapping[(module, level)]


def question_signature(q: Question) -> str:
    options = "\n".join(q.options or ())
    payload = f"{q.module}|{q.level}|{q.qtype}|{q.prompt}\n{q.code or ''}\n{options}"
    return normalize_text(payload)


def generate_output_questions(
    module: str,
    level: str,
    count: int,
    rng: random.Random,
    source_matcher: SourceMatcher,
    signatures: set[str],
) -> list[Question]:
    patterns = get_output_patterns(module, level)
    generated: list[Question] = []
    attempts = 0
    variant = 0
    max_attempts = max(300, count * 80)

    while len(generated) < count and attempts < max_attempts:
        attempts += 1
        pattern = rng.choice(patterns)
        prompt, code, concept = pattern(rng, variant)
        variant += 1
        q = Question(module=module, level=level, qtype="output", prompt=prompt, code=code, concept=concept)
        sig = question_signature(q)
        if sig in signatures:
            continue
        if source_matcher.is_too_similar(f"{prompt}\n{code}"):
            continue
        signatures.add(sig)
        generated.append(q)

    if len(generated) != count:
        raise RuntimeError(f"Could not generate enough output questions for {module}/{level}: {len(generated)}/{count}")
    return generated


def generate_mcq_questions(
    module: str,
    level: str,
    count: int,
    rng: random.Random,
    source_matcher: SourceMatcher,
    signatures: set[str],
) -> list[Question]:
    pool = MCQ_BANK[module][level][:]
    rng.shuffle(pool)
    generated: list[Question] = []

    for prompt, options, concept in pool:
        q = Question(module=module, level=level, qtype="mcq", prompt=prompt, options=options, concept=concept)
        sig = question_signature(q)
        if sig in signatures:
            continue
        if source_matcher.is_too_similar(f"{prompt}\n" + "\n".join(options)):
            continue
        signatures.add(sig)
        generated.append(q)
        if len(generated) == count:
            break

    if len(generated) != count:
        raise RuntimeError(f"Could not generate enough MCQ questions for {module}/{level}: {len(generated)}/{count}")
    return generated


def build_question_set(distribution: dict, rng: random.Random, source_matcher: SourceMatcher) -> list[Question]:
    signatures: set[str] = set()
    questions: list[Question] = []

    for module in MODULES:
        for level in LEVELS:
            out_count = distribution[module][level]["output"]
            mcq_count = distribution[module][level]["mcq"]
            questions.extend(generate_output_questions(module, level, out_count, rng, source_matcher, signatures))
            questions.extend(generate_mcq_questions(module, level, mcq_count, rng, source_matcher, signatures))

    return questions


def verify_totals(questions: list[Question], distribution: dict) -> dict[str, int]:
    module_totals = {m: 0 for m in MODULES}
    level_totals = {l: 0 for l in LEVELS}
    type_totals = {t: 0 for t in QTYPES}

    for q in questions:
        module_totals[q.module] += 1
        level_totals[q.level] += 1
        type_totals[q.qtype] += 1

    for module in MODULES:
        expected = sum(distribution[module][level][qtype] for level in LEVELS for qtype in QTYPES)
        if module_totals[module] != expected:
            raise AssertionError(f"Module count mismatch for {module}: {module_totals[module]} vs {expected}")

    expected_level_l1 = sum(distribution[m]["L1"][t] for m in MODULES for t in QTYPES)
    expected_level_l2 = sum(distribution[m]["L2"][t] for m in MODULES for t in QTYPES)
    if level_totals["L1"] != expected_level_l1 or level_totals["L2"] != expected_level_l2:
        raise AssertionError("Level total mismatch.")

    expected_output = sum(distribution[m][l]["output"] for m in MODULES for l in LEVELS)
    expected_mcq = sum(distribution[m][l]["mcq"] for m in MODULES for l in LEVELS)
    if type_totals["output"] != expected_output or type_totals["mcq"] != expected_mcq:
        raise AssertionError("Question-type total mismatch.")

    if len(questions) != expected_output + expected_mcq:
        raise AssertionError("Total question count mismatch.")

    return {
        "total": len(questions),
        "l1": level_totals["L1"],
        "l2": level_totals["L2"],
        "output": type_totals["output"],
        "mcq": type_totals["mcq"],
        "list": module_totals["list"],
        "dict": module_totals["dict"],
        "set": module_totals["set"],
        "tuple": module_totals["tuple"],
    }


def split_for_render(questions: list[Question], seed: int) -> dict[str, dict[str, list[Question]]]:
    rng = random.Random(seed + 999)
    bucket = {"L1": {"output": [], "mcq": []}, "L2": {"output": [], "mcq": []}}
    for q in questions:
        bucket[q.level][q.qtype].append(q)
    for level in LEVELS:
        rng.shuffle(bucket[level]["output"])
        rng.shuffle(bucket[level]["mcq"])
    return bucket


def line_count_for_output(level: str, code: str) -> int:
    _ = (level, code)
    return 2


def render_pdf(output_path: Path, rendered: dict[str, dict[str, list[Question]]], summary: dict[str, int]) -> None:
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        alignment=1,
        spaceAfter=6,
    )
    h1_style = ParagraphStyle(
        "H1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        spaceBefore=8,
        spaceAfter=4,
    )
    h2_style = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        spaceBefore=6,
        spaceAfter=3,
    )
    q_style = ParagraphStyle(
        "Q",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=11.2,
        leading=14.6,
        spaceAfter=2,
    )
    code_style = ParagraphStyle(
        "CodeStyle",
        fontName="Courier-Bold",
        fontSize=10.2,
        leading=12.8,
        leftIndent=0,
        rightIndent=0,
        spaceBefore=0,
        spaceAfter=0,
        textColor=colors.HexColor("#111111"),
    )
    opt_style = ParagraphStyle(
        "Opt",
        parent=q_style,
        leftIndent=12,
        spaceAfter=1.5,
    )
    meta_style = ParagraphStyle(
        "Meta",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.2,
        leading=11.8,
        textColor=colors.HexColor("#303030"),
        spaceAfter=2,
    )

    def footer(canvas_obj, doc_obj) -> None:
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.setFillColor(colors.HexColor("#5a5a5a"))
        canvas_obj.drawRightString(A4[0] - 12 * mm, 8.5 * mm, f"Page {doc_obj.page}")

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=12 * mm,
        rightMargin=12 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
        title="Python Week 3 Test",
        author="Auto Generator",
    )

    story = []
    story.append(Paragraph("PYTHON WEEK 3 TEST", title_style))
    story.append(Paragraph("Collections Framework: List, Dict, Set, Tuple", h2_style))
    story.append(
        Paragraph(
            (
                "Instructions: (1) Solve all questions. (2) For print-output questions, write exact output. "
                "(3) For MCQ, choose one correct option. "
                f"(4) Total: {summary['total']} questions | L1: {summary['l1']} | L2: {summary['l2']} | "
                f"Output: {summary['output']} | MCQ: {summary['mcq']}."
            ),
            meta_style,
        )
    )
    story.append(Spacer(1, 4))

    q_number = 1
    for level in LEVELS:
        story.append(Paragraph(f"{'Level 1' if level == 'L1' else 'Level 2'}", h1_style))

        story.append(Paragraph("Part A: Predict the Output", h2_style))
        for q in rendered[level]["output"]:
            q_block = [Paragraph(f"Q{q_number}. {q.prompt}", q_style)]
            code_header = Paragraph("<b>Code Snippet</b>", meta_style)
            code_block = Preformatted(q.code or "", code_style)
            code_table = Table([[code_block]], colWidths=["100%"])
            code_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f6f8fa")),
                        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#7a7a7a")),
                        ("LEFTPADDING", (0, 0), (-1, -1), 7),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                        ("TOPPADDING", (0, 0), (-1, -1), 6),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ]
                )
            )
            q_block.append(code_header)
            q_block.append(code_table)
            q_block.append(Spacer(1, 2))
            q_block.append(Paragraph("Answer:", meta_style))
            q_block.append(AnswerLines(line_count_for_output(level, q.code or "")))
            q_block.append(Spacer(1, 4))
            story.append(KeepTogether(q_block))
            q_number += 1

        story.append(Paragraph("Part B: MCQ (Single Correct Option)", h2_style))
        for q in rendered[level]["mcq"]:
            q_block = [Paragraph(f"Q{q_number}. {q.prompt}", q_style)]
            if q.options:
                for opt in q.options:
                    q_block.append(Paragraph(opt, opt_style))
            q_block.append(Spacer(1, 5))
            story.append(KeepTogether(q_block))
            q_number += 1

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def load_distribution(path: Path | None) -> dict:
    if path is None:
        return DEFAULT_DISTRIBUTION
    data = json.loads(path.read_text(encoding="utf-8"))
    validate_distribution(data)
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Week 3 Python collections test PDF.")
    parser.add_argument(
        "--output",
        default=str(Path("python/assignement/test/python week3 test.pdf")),
        help="Output PDF path.",
    )
    parser.add_argument("--seed", type=int, default=20260525, help="Random seed for reproducibility.")
    parser.add_argument(
        "--distribution-file",
        default=None,
        help="Optional JSON file for distribution matrix.",
    )
    args = parser.parse_args()

    distribution = load_distribution(Path(args.distribution_file)) if args.distribution_file else DEFAULT_DISTRIBUTION
    validate_distribution(distribution)

    worksheet_paths = [
        Path("python/assignement/worksheets/collection_framwork/list.md"),
        Path("python/assignement/worksheets/collection_framwork/dict.md"),
        Path("python/assignement/worksheets/collection_framwork/set.md"),
        Path("python/assignement/worksheets/collection_framwork/tuple.md"),
    ]
    source_matcher = SourceMatcher(worksheet_paths=worksheet_paths, threshold=0.97)

    rng = random.Random(args.seed)
    questions = build_question_set(distribution=distribution, rng=rng, source_matcher=source_matcher)
    summary = verify_totals(questions, distribution)
    rendered = split_for_render(questions, seed=args.seed)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    render_pdf(output_path=output_path, rendered=rendered, summary=summary)

    print("Generated:", output_path)
    print(
        "Summary:",
        f"total={summary['total']}, L1={summary['l1']}, L2={summary['l2']}, "
        f"output={summary['output']}, mcq={summary['mcq']}, "
        f"list={summary['list']}, dict={summary['dict']}, set={summary['set']}, tuple={summary['tuple']}",
    )


if __name__ == "__main__":
    main()
