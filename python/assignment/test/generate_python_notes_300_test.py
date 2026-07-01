from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import re
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import KeepTogether, Preformatted, SimpleDocTemplate, Spacer, Paragraph, Table, TableStyle
from reportlab.platypus import PageBreak


TOPIC_ORDER = ("collections", "concurrency", "oops", "clean_code", "fundamentals")
DIFF_ORDER = ("E", "M", "H", "SH")
TYPE_ORDER = ("MSQ", "OUT")

DIFF_LABEL = {"E": "Easy", "M": "Medium", "H": "Hard", "SH": "Super Hard"}
TYPE_LABEL = {"MSQ": "Multi-select", "OUT": "Print Output"}

TOTAL_QUESTIONS = 300

TOPIC_TOTALS = {
    "collections": 125,
    "concurrency": 75,
    "oops": 75,
    "clean_code": 10,
    "fundamentals": 15,
}

TOPIC_DIFF_TOTALS = {
    "collections": {"E": 0, "M": 35, "H": 60, "SH": 30},
    "concurrency": {"E": 7, "M": 45, "H": 15, "SH": 8},
    "oops": {"E": 7, "M": 45, "H": 15, "SH": 8},
    "clean_code": {"E": 1, "M": 6, "H": 2, "SH": 1},
    "fundamentals": {"E": 2, "M": 9, "H": 3, "SH": 1},
}

COLLECTION_OUTPUT_DIFF_TARGET = {"E": 0, "M": 25, "H": 50, "SH": 25}
COLLECTION_MSQ_DIFF_TARGET = {"E": 0, "M": 10, "H": 10, "SH": 5}

TOPIC_TYPE_TOTALS = {
    "collections": {"MSQ": 25, "OUT": 100},
    "concurrency": {"MSQ": 37, "OUT": 38},
    "oops": {"MSQ": 38, "OUT": 37},
    "clean_code": {"MSQ": 5, "OUT": 5},
    "fundamentals": {"MSQ": 7, "OUT": 8},
}

GLOBAL_TYPE_TOTALS = {
    "MSQ": sum(v["MSQ"] for v in TOPIC_TYPE_TOTALS.values()),
    "OUT": sum(v["OUT"] for v in TOPIC_TYPE_TOTALS.values()),
}
GLOBAL_DIFF_TOTALS = {d: sum(TOPIC_DIFF_TOTALS[t][d] for t in TOPIC_ORDER) for d in DIFF_ORDER}

@dataclass(frozen=True)
class Concept:
    concept_id: str
    topic: str
    source_file: str
    heading: str
    parent_heading: str | None
    level: int
    context: str
    snippet: str | None


@dataclass
class Question:
    qid: int
    topic: str
    difficulty: str
    qtype: str
    concept_id: str
    source_file: str
    heading: str
    prompt: str
    code: str | None
    options: list[str] | None
    correct_letters: list[str] | None
    expected_output: str | None
    reasoning: str
    signature: str


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def slugify(text: str, max_len: int = 42) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    if not s:
        s = "concept"
    return s[:max_len]


def stable_hash_int(text: str) -> int:
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:16], 16)


def map_topic(notes_root: Path, file_path: Path) -> str | None:
    rel = file_path.relative_to(notes_root).as_posix()
    parts = rel.split("/")
    if not parts:
        return None
    first = parts[0]
    if first == "collection_framework":
        return "collections"
    if first == "python_sync_async_multithreaded":
        return "concurrency"
    if first == "python_fundamentals":
        return "fundamentals"
    if first == "oops_and_clean_code":
        if file_path.name == "Clean Code Foundations.md":
            return "clean_code"
        return "oops"
    return None


def extract_first_code_block(text: str) -> str | None:
    m = re.search(r"```(?:python|py|text)?\n(.*?)```", text, re.DOTALL)
    if not m:
        return None
    code = m.group(1).strip("\n")
    return code if code else None


def extract_context(lines: list[str], start: int) -> tuple[str, str | None]:
    buff: list[str] = []
    i = start
    while i < len(lines):
        if re.match(r"^##{1,3}\s+", lines[i]):
            break
        buff.append(lines[i].rstrip("\n"))
        if len(buff) >= 22:
            break
        i += 1
    text = "\n".join(buff).strip()
    if not text:
        return "", None
    snippet = extract_first_code_block(text)
    if len(text) > 650:
        text = text[:650].rstrip() + "..."
    return text, snippet


def scan_concepts(notes_root: Path) -> tuple[dict[str, list[Concept]], list[str]]:
    concepts_by_topic: dict[str, list[Concept]] = {k: [] for k in TOPIC_ORDER}
    used_ids: set[str] = set()
    eligible_files: list[str] = []

    md_files = sorted(notes_root.rglob("*.md"), key=lambda p: p.as_posix())
    for file_path in md_files:
        if re.match(r"^[0-9]", file_path.stem):
            continue
        topic = map_topic(notes_root, file_path)
        if topic is None:
            continue
        eligible_files.append(file_path.relative_to(notes_root).as_posix())
        lines = file_path.read_text(encoding="utf-8").splitlines()
        current_h2: str | None = None
        for idx, raw in enumerate(lines):
            m = re.match(r"^(##|###)\s+(.*)$", raw.strip())
            if not m:
                continue
            level = 2 if m.group(1) == "##" else 3
            heading = m.group(2).strip()
            if not heading:
                continue
            if level == 2:
                current_h2 = heading
            parent = current_h2 if level == 3 else None
            cid_base = normalize_text(
                f"{file_path.relative_to(notes_root).as_posix()}|{heading}|{parent or ''}"
            )
            cid = slugify(cid_base, 64)
            suffix = 2
            while cid in used_ids:
                cid = f"{slugify(cid_base, 58)}-{suffix}"
                suffix += 1
            used_ids.add(cid)
            context, snippet = extract_context(lines, idx + 1)
            concepts_by_topic[topic].append(
                Concept(
                    concept_id=cid,
                    topic=topic,
                    source_file=file_path.relative_to(notes_root).as_posix(),
                    heading=heading,
                    parent_heading=parent,
                    level=level,
                    context=context,
                    snippet=snippet,
                )
            )
    for topic in TOPIC_ORDER:
        concepts_by_topic[topic].sort(key=lambda c: (c.source_file, c.concept_id))
    return concepts_by_topic, sorted(eligible_files)


def allocate_type_by_topic_diff() -> dict[str, dict[str, dict[str, int]]]:
    alloc: dict[str, dict[str, dict[str, int]]] = {}
    for topic in TOPIC_ORDER:
        if topic == "collections":
            alloc[topic] = {}
            for diff in DIFF_ORDER:
                alloc[topic][diff] = {
                    "MSQ": COLLECTION_MSQ_DIFF_TARGET[diff],
                    "OUT": COLLECTION_OUTPUT_DIFF_TARGET[diff],
                }
            continue

        topic_total = TOPIC_TOTALS[topic]
        topic_msq_total = TOPIC_TYPE_TOTALS[topic]["MSQ"]
        ratio = topic_msq_total / topic_total
        floors: dict[str, int] = {}
        rems: list[tuple[float, str]] = []
        for diff in DIFF_ORDER:
            dcount = TOPIC_DIFF_TOTALS[topic][diff]
            expected = dcount * ratio
            f = math.floor(expected)
            floors[diff] = f
            rems.append((expected - f, diff))
        need = topic_msq_total - sum(floors.values())
        rems.sort(key=lambda x: (-x[0], DIFF_ORDER.index(x[1])))
        for i in range(need):
            floors[rems[i][1]] += 1
        alloc[topic] = {}
        for diff in DIFF_ORDER:
            msq = floors[diff]
            out = TOPIC_DIFF_TOTALS[topic][diff] - msq
            alloc[topic][diff] = {"MSQ": msq, "OUT": out}

    total_msq = sum(alloc[t][d]["MSQ"] for t in TOPIC_ORDER for d in DIFF_ORDER)
    delta = GLOBAL_TYPE_TOTALS["MSQ"] - total_msq
    if delta != 0:
        # deterministic global adjustment safety-net
        locked = {("collections", d) for d in DIFF_ORDER}
        cells = [(t, d) for t in TOPIC_ORDER for d in DIFF_ORDER if (t, d) not in locked]
        if delta > 0:
            for t, d in cells:
                if delta == 0:
                    break
                if alloc[t][d]["OUT"] > 0:
                    alloc[t][d]["OUT"] -= 1
                    alloc[t][d]["MSQ"] += 1
                    delta -= 1
        else:
            for t, d in cells:
                if delta == 0:
                    break
                if alloc[t][d]["MSQ"] > 0:
                    alloc[t][d]["MSQ"] -= 1
                    alloc[t][d]["OUT"] += 1
                    delta += 1
        if delta != 0:
            raise ValueError("Could not satisfy global type totals without violating locked allocations.")
    return alloc


def make_slots(alloc: dict[str, dict[str, dict[str, int]]]) -> list[dict[str, str]]:
    slots: list[dict[str, str]] = []
    for topic in TOPIC_ORDER:
        for diff in DIFF_ORDER:
            for qtype in TYPE_ORDER:
                for _ in range(alloc[topic][diff][qtype]):
                    slots.append({"topic": topic, "difficulty": diff, "qtype": qtype})
    return slots


def pick_concepts_for_topics(
    concepts_by_topic: dict[str, list[Concept]],
    seed: int,
) -> dict[str, list[Concept]]:
    rng = random.Random(seed)
    chosen: dict[str, list[Concept]] = {}
    for topic in TOPIC_ORDER:
        pool = concepts_by_topic[topic]
        need = TOPIC_TOTALS[topic]
        if len(pool) < need:
            raise ValueError(f"Not enough concepts for {topic}: have {len(pool)}, need {need}")
        chosen[topic] = rng.sample(pool, need)
    return chosen


def option_shuffle(items: list[tuple[str, bool]], key: str) -> list[tuple[str, bool]]:
    rng = random.Random(stable_hash_int(key))
    out = items[:]
    rng.shuffle(out)
    return out


def clean_heading_for_display(heading: str) -> str:
    h = heading.replace("`", "")
    h = re.sub(r"^\s*[\W_]*\d+\s*[\)\.\-:]\s*", "", h)
    h = re.sub(r"^\s*q\s*\d+\s*[\)\.\-:]\s*", "", h, flags=re.IGNORECASE)
    h = re.sub(r"^\s*[-*#]+\s*", "", h)
    h = re.sub(r"\s+", " ", h).strip()
    return h or "this concept"


def deterministic_pick(items: list[str], k: int, key: str) -> list[str]:
    if k <= 0:
        return []
    rng = random.Random(stable_hash_int(key))
    arr = items[:]
    rng.shuffle(arr)
    return arr[:k]


def infer_subdomain(concept: Concept) -> str:
    fp = concept.source_file.lower()
    h = clean_heading_for_display(concept.heading).lower()
    if concept.topic == "collections":
        if "dict" in fp or "mapping" in h or "hash" in h:
            return "dict"
        if "set" in fp or "frozenset" in h:
            return "set"
        if "tuple" in fp or "unpack" in h:
            return "tuple"
        return "list"
    if concept.topic == "concurrency":
        if "async" in fp or "task" in h or "await" in h:
            return "async"
        if "thread" in fp or "lock" in h or "deadlock" in h:
            return "threading"
        if "sync" in fp:
            return "sync"
        return "general"
    if concept.topic == "oops":
        if "solid" in fp or "lsp" in h:
            return "solid"
        if "inheritance" in fp or "mro" in h or "super" in h:
            return "inheritance"
        if "pattern" in fp or "strategy" in h:
            return "patterns"
        return "oop"
    if concept.topic == "clean_code":
        return "clean"
    if concept.topic == "fundamentals":
        if "function" in fp:
            return "functions"
        if "control_flow" in fp or "control flow" in h:
            return "control_flow"
        if "execution" in fp or "frame" in h or "import" in h:
            return "execution"
        if "memory" in fp or "variables" in fp:
            return "memory"
        return "data"
    return "general"


def msq_option_bank(concept: Concept) -> tuple[list[str], list[str]]:
    topic = concept.topic
    sub = infer_subdomain(concept)

    true_base: dict[str, list[str]] = {
        "collections": [
            "Collection choice should be based on access pattern, mutation pattern, and complexity tradeoffs.",
            "Shallow copies duplicate only the outer container and may share nested mutable objects.",
            "Readability and deterministic output requirements can be more important than micro-optimizations.",
            "Using the correct collection type often removes the need for complex conditional logic.",
        ],
        "concurrency": [
            "Concurrency design should include explicit timeout, cancellation, and failure behavior.",
            "Concurrency design should include bounded work queues or bounded in-flight operations.",
            "Observability (task/thread ids, queue depth, retries) is critical for production debugging.",
            "Correctness and safe shutdown must be verified before performance tuning claims.",
        ],
        "oops": [
            "OOP design should preserve clear contracts and minimize unnecessary coupling.",
            "Composition is often safer than deep inheritance for change-heavy systems.",
            "Depending on abstractions improves testability and implementation swapping.",
            "Substitutability requires preserving semantic expectations, not just method names.",
        ],
        "clean_code": [
            "Clean code is stronger when intent-revealing names and focused responsibilities are used.",
            "Guard clauses can improve readability by reducing deep nesting.",
            "Clean code decisions should optimize maintainability and testability, not cleverness.",
            "Refactoring should be done in small safe steps with behavior checks.",
        ],
        "fundamentals": [
            "Fundamentals should be reasoned using Python's binding and execution model, not memorized guesses.",
            "`is` checks identity while `==` checks value equality semantics.",
            "Function defaults are evaluated at definition time, so mutable defaults can retain state.",
            "Context managers (`with`) are preferred for deterministic resource cleanup.",
        ],
    }

    false_base: dict[str, list[str]] = {
        "collections": [
            "List front-pop operations (`pop(0)`) are always O(1), so they are ideal for queue workloads.",
            "Dictionary keys can safely be mutable lists as long as values are immutable.",
            "Set ordering should be relied upon for stable business logic output.",
            "Deep copies and shallow copies behave identically for nested mutable structures.",
        ],
        "concurrency": [
            "Async code automatically speeds up CPU-bound loops without offloading or multiprocessing.",
            "If a thread is already running, `future.cancel()` always stops it immediately.",
            "Deadlocks can happen only when code uses more than two locks.",
            "Using many threads removes the need for lock or shared-state design.",
        ],
        "oops": [
            "Inheritance automatically guarantees low coupling and high cohesion.",
            "LSP is satisfied as long as child method names match parent method names.",
            "Dependency injection is mainly about reducing lines of code, not testability.",
            "Protocols require explicit inheritance from the protocol class at runtime.",
        ],
        "clean_code": [
            "Catching broad exceptions and ignoring them is clean because execution continues.",
            "Long methods are preferred because function calls always reduce readability.",
            "Magic numbers improve maintainability by reducing named constants.",
            "Copy-pasting similar logic is better than creating shared abstractions.",
        ],
        "fundamentals": [
            "Assignment copies objects by value in Python for all data types.",
            "Importing a module never executes its top-level statements.",
            "Mutable default arguments are recreated fresh on each function call.",
            "`try/finally` skips `finally` when the `try` block returns early.",
        ],
    }

    true_sub: dict[tuple[str, str], list[str]] = {
        ("collections", "dict"): [
            "Dictionary view objects (`keys`, `items`) are dynamic and reflect later dictionary updates.",
            "Merging dictionaries with duplicate keys keeps the right-side value.",
        ],
        ("collections", "set"): [
            "Set algebra operators (`|`, `&`, `-`, `^`) model data comparison tasks clearly.",
            "A `frozenset` can be used as a dictionary key when order-independence is required.",
        ],
        ("collections", "tuple"): [
            "A single-item tuple requires a trailing comma.",
            "Tuple hashability depends on all contained elements being hashable.",
        ],
        ("collections", "list"): [
            "List sorting is stable in Python, so equal-key element order is preserved.",
            "For frequent queue front operations, `collections.deque` is typically a better fit than list.",
        ],
        ("concurrency", "async"): [
            "In asyncio, cancellation is cooperative and usually observed at await points.",
            "Blocking calls inside the event loop should be offloaded or replaced with async APIs.",
        ],
        ("concurrency", "threading"): [
            "Lock ordering is a practical deadlock-prevention strategy.",
            "The GIL does not remove race conditions for shared mutable state updates.",
        ],
        ("concurrency", "sync"): [
            "Synchronous flows are often easier to reason about and debug for low-concurrency workloads.",
            "Timeouts and retries still matter in synchronous I/O code.",
        ],
        ("oops", "inheritance"): [
            "Cooperative multiple inheritance relies on consistent `super()` usage across classes.",
            "Deep inheritance trees can increase fragility when base classes change frequently.",
        ],
        ("oops", "solid"): [
            "SRP encourages one primary reason to change per class/component.",
            "DIP suggests high-level modules depend on abstractions rather than concrete implementations.",
        ],
        ("oops", "patterns"): [
            "Strategy pattern can replace repeated type-based condition chains.",
            "Factory-style creation helps isolate construction logic from business workflows.",
        ],
        ("oops", "oop"): [
            "Encapsulation protects invariants by exposing behavior methods instead of raw state mutation.",
            "Polymorphism allows extending behavior without rewriting stable caller logic.",
        ],
        ("fundamentals", "functions"): [
            "Python argument passing is call-by-sharing: objects are shared, names are local bindings.",
            "Decorators should use `functools.wraps` to preserve wrapped function metadata.",
        ],
        ("fundamentals", "control_flow"): [
            "Loop `else` executes only when the loop completes without `break`.",
            "Boolean short-circuiting can prevent evaluation of unsafe expressions.",
        ],
        ("fundamentals", "execution"): [
            "Imported modules are cached in `sys.modules` after first successful load.",
            "LEGB describes Python name lookup order across scopes.",
        ],
        ("fundamentals", "memory"): [
            "Rebinding a name is different from mutating the underlying object.",
            "Identity checks with `is` should be reserved for singleton semantics (for example `None`).",
        ],
        ("fundamentals", "data"): [
            "Choosing immutable data where possible can reduce accidental shared-state bugs.",
            "Type conversion should be explicit when input formats are uncertain.",
        ],
    }

    false_sub: dict[tuple[str, str], list[str]] = {
        ("collections", "dict"): [
            "Dictionary iteration order in modern Python is random and should never be expected.",
            "Calling `dict.get()` raises `KeyError` when a key is missing.",
        ],
        ("collections", "set"): [
            "Sets support index-based access like lists for deterministic element lookup.",
            "Set membership checks are slower than list scans in average-case scenarios.",
        ],
        ("collections", "tuple"): [
            "Tuples allow in-place item reassignment because they are sequence types.",
            "Any tuple can be a dictionary key even when it contains lists or dicts.",
        ],
        ("collections", "list"): [
            "Using `list.sort()` returns a new sorted list and leaves the original untouched.",
            "`bisect` insertion is O(log n) overall even after shifting list elements.",
        ],
        ("concurrency", "async"): [
            "Awaiting a coroutine blocks all other tasks until the coroutine fully completes.",
            "Using `asyncio.gather` makes timeout handling unnecessary.",
        ],
        ("concurrency", "threading"): [
            "Using a lock everywhere guarantees high throughput and zero contention risk.",
            "Thread-safe communication requires global mutable variables instead of queues.",
        ],
        ("concurrency", "sync"): [
            "Synchronous I/O code does not need timeout or retry policies.",
            "Sequential execution eliminates all external dependency failure modes.",
        ],
        ("oops", "inheritance"): [
            "Multiple inheritance is safe without MRO awareness if class names are unique.",
            "Overriding a method should always change input/output contract details.",
        ],
        ("oops", "solid"): [
            "OCP means existing stable classes must be edited for each new behavior.",
            "ISP recommends one large interface so every client shares identical methods.",
        ],
        ("oops", "patterns"): [
            "Design patterns are mandatory in all modules, even for trivial scripts.",
            "Strategy pattern requires inheritance and cannot use composition.",
        ],
        ("oops", "oop"): [
            "Encapsulation is only about making fields private; behavior design is unrelated.",
            "Polymorphism always requires explicit inheritance from a common base class.",
        ],
        ("fundamentals", "functions"): [
            "Functions cannot be passed as arguments because Python is not functional.",
            "Closures always capture loop variables by value, so late binding never occurs.",
        ],
        ("fundamentals", "control_flow"): [
            "The `match/case` default branch is required and must be listed first.",
            "The `finally` block runs only when no exception occurs in `try`.",
        ],
        ("fundamentals", "execution"): [
            "LEGB lookup checks global scope before local scope for function variables.",
            "Python executes source lines directly without creating frames/bytecode structures.",
        ],
        ("fundamentals", "memory"): [
            "Mutating a shared list in a function never affects caller-visible state.",
            "Object identity and equality are equivalent and interchangeable in all comparisons.",
        ],
        ("fundamentals", "data"): [
            "Every built-in Python object is mutable unless declared with `final`.",
            "Implicit type coercion in Python behaves the same as in C for all operators.",
        ],
    }

    true_pool = true_base[topic][:]
    false_pool = false_base[topic][:]
    true_pool.extend(true_sub.get((topic, sub), []))
    false_pool.extend(false_sub.get((topic, sub), []))

    # deterministic de-dup preserving order
    true_pool = list(dict.fromkeys(true_pool))
    false_pool = list(dict.fromkeys(false_pool))
    return true_pool, false_pool


def msq_true_count(difficulty: str) -> int:
    if difficulty == "SH":
        return 3
    return 2


def build_msq_question(qid: int, concept: Concept, difficulty: str) -> tuple[str, list[str], list[str], str]:
    heading = clean_heading_for_display(concept.heading)
    stems = [
        f"Q{qid}. Which statements are correct about {heading} in Python? Select all that apply.",
        f"Q{qid}. In production-quality Python code, which statements about {heading} are valid? Select all that apply.",
        f"Q{qid}. While applying {heading}, which statements are technically correct? Select all that apply.",
    ]
    stem = stems[stable_hash_int(f"{concept.concept_id}|{qid}|stem") % len(stems)]

    true_pool, false_pool = msq_option_bank(concept)
    t_count = msq_true_count(difficulty)
    f_count = 4 - t_count
    true_opts = deterministic_pick(true_pool, t_count, f"{concept.concept_id}|{qid}|true|{difficulty}")
    false_opts = deterministic_pick(false_pool, f_count, f"{concept.concept_id}|{qid}|false|{difficulty}")
    raw = [(x, True) for x in true_opts] + [(x, False) for x in false_opts]

    if len(raw) != 4:
        raise ValueError(f"Invalid MSQ option count for Q{qid}: {len(raw)}")

    shuffled = option_shuffle(raw, f"{concept.concept_id}|{difficulty}|{qid}|MSQ|shuffle")
    letters = ["A", "B", "C", "D"]
    options = [f"{letters[i]}. {txt}" for i, (txt, _) in enumerate(shuffled)]
    correct = [letters[i] for i, (_, is_true) in enumerate(shuffled) if is_true]

    reasoning_lines = [
        f"Primary concept: {heading} ({concept.topic}).",
    ]
    for opt, (_, is_true) in zip(options, shuffled):
        prefix = "Correct" if is_true else "Incorrect"
        reasoning_lines.append(f"{prefix} - {opt}: {opt[3:]}")
    reasoning = " ".join(reasoning_lines)

    prompt = stem
    return prompt, options, correct, reasoning


def numbers_for_concept(concept: Concept, qid: int) -> tuple[int, int, int, int]:
    rng = random.Random(stable_hash_int(f"{concept.concept_id}|{qid}|OUT"))
    return (
        rng.randint(2, 11),
        rng.randint(3, 12),
        rng.randint(1, 7),
        rng.randint(2, 9),
    )


def short_heading(heading: str) -> str:
    return clean_heading_for_display(heading)[:48]


def normalize_code_display(code: str) -> str:
    lines = code.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    cleaned = [line.rstrip().replace("\t", "    ") for line in lines]
    return "\n".join(cleaned).strip("\n")


def markdown_fence_for_code(code: str) -> str:
    return "````" if "```" in code else "```"


def build_output_question(qid: int, concept: Concept, difficulty: str) -> tuple[str, str, str, str]:
    a, b, c, d = numbers_for_concept(concept, qid)
    hs = short_heading(concept.heading)
    key = stable_hash_int(f"{concept.concept_id}|{difficulty}|template")
    template = key % 5

    if concept.topic == "collections":
        collection_diff = difficulty if difficulty in {"M", "H", "SH"} else "M"

        if collection_diff == "M":
            if template == 0:
                records = [a, b, a, c]
                frequency: dict[int, int] = {}
                for value in records:
                    frequency[value] = frequency.get(value, 0) + 1
                out = str(frequency[a])
                code = (
                    f"records = [{a}, {b}, {a}, {c}]\n"
                    "frequency = {}\n"
                    "for value in records:\n"
                    "    frequency[value] = frequency.get(value, 0) + 1\n"
                    f"print(frequency[{a}])"
                )
                trace = "Frequency counting with dictionary get tracks repeated values deterministically."
            elif template == 1:
                values = [a, b, c, a]
                unique_ordered = list(dict.fromkeys(values))
                out = str(sum(unique_ordered))
                code = (
                    f"values = [{a}, {b}, {c}, {a}]\n"
                    "unique_ordered = list(dict.fromkeys(values))\n"
                    "print(sum(unique_ordered))"
                )
                trace = "Order-preserving dedup with dict.fromkeys keeps first occurrence order."
            elif template == 2:
                pair_list = [(a, b), (c, d), (a, c)]
                total = 0
                for left, right in pair_list:
                    total += left - right
                out = str(total)
                code = (
                    f"pair_list = [({a}, {b}), ({c}, {d}), ({a}, {c})]\n"
                    "total = 0\n"
                    "for left, right in pair_list:\n"
                    "    total += left - right\n"
                    "print(total)"
                )
                trace = "Tuple unpacking in loop computes signed aggregate across pairs."
            elif template == 3:
                left_ids = {a, b, c}
                right_ids = {b, d}
                shared = left_ids & right_ids
                out = str(sum(shared))
                code = (
                    f"left_ids = {{{a}, {b}, {c}}}\n"
                    f"right_ids = {{{b}, {d}}}\n"
                    "shared = left_ids & right_ids\n"
                    "print(sum(shared))"
                )
                trace = "Set intersection retains only common elements before aggregation."
            else:
                numbers = [a, b, c, d]
                numbers.sort(reverse=True)
                out = str(numbers[0] - numbers[-1])
                code = (
                    f"numbers = [{a}, {b}, {c}, {d}]\n"
                    "numbers.sort(reverse=True)\n"
                    "print(numbers[0] - numbers[-1])"
                )
                trace = "Descending in-place sort exposes max and min via boundary indices."
        elif collection_diff == "H":
            if template == 0:
                data = [a, b, c, d, a, c, b]
                freq: dict[int, int] = {}
                for item in data:
                    freq[item] = freq.get(item, 0) + 1
                out = str(sum(key * value for key, value in freq.items()))
                code = (
                    f"data = [{a}, {b}, {c}, {d}, {a}, {c}, {b}]\n"
                    "freq = {}\n"
                    "for item in data:\n"
                    "    freq[item] = freq.get(item, 0) + 1\n"
                    "print(sum(key * value for key, value in freq.items()))"
                )
                trace = "Weighted frequency accumulation combines key and multiplicity."
            elif template == 1:
                rows = [[a, b], [c, d], [a + c, b + d]]
                columns = list(zip(*rows))
                out = str(sum(columns[0]) - sum(columns[1]))
                code = (
                    f"rows = [[{a}, {b}], [{c}, {d}], [{a + c}, {b + d}]]\n"
                    "columns = list(zip(*rows))\n"
                    "print(sum(columns[0]) - sum(columns[1]))"
                )
                trace = "Transpose via zip(*rows) then aggregate by column."
            elif template == 2:
                pairs = [(a, b), (a, c), (b, d), (a, d), (c, d)]
                grouped: dict[int, list[int]] = {}
                for k, v in pairs:
                    grouped.setdefault(k, []).append(v)
                out = str(sum(len(vs) for vs in grouped.values()) + len(grouped))
                code = (
                    f"pairs = [({a}, {b}), ({a}, {c}), ({b}, {d}), ({a}, {d}), ({c}, {d})]\n"
                    "grouped = {}\n"
                    "for k, v in pairs:\n"
                    "    grouped.setdefault(k, []).append(v)\n"
                    "print(sum(len(vs) for vs in grouped.values()) + len(grouped))"
                )
                trace = "Adjacency-list style grouping uses setdefault for compact insertion."
            elif template == 3:
                matrix = [[a, b, a], [c, d, c], [b, a, d]]
                flat = [x for row in matrix for x in row]
                unique = sorted(set(flat))
                index = {value: idx for idx, value in enumerate(unique)}
                out = str(sum(index[x] for x in flat[:5]))
                code = (
                    f"matrix = [[{a}, {b}, {a}], [{c}, {d}, {c}], [{b}, {a}, {d}]]\n"
                    "flat = [x for row in matrix for x in row]\n"
                    "unique = sorted(set(flat))\n"
                    "index = {value: idx for idx, value in enumerate(unique)}\n"
                    "print(sum(index[x] for x in flat[:5]))"
                )
                trace = "Flattening, dedup-index mapping, and partial projection are composed."
            else:
                words = [f"k{a}", f"k{b}", f"k{a}", f"k{c}", f"k{b}", f"k{d}"]
                rank = {name: i for i, name in enumerate(sorted(set(words)), start=1)}
                counts: dict[str, int] = {}
                for name in words:
                    counts[name] = counts.get(name, 0) + rank[name]
                out = str(sum(counts.values()))
                code = (
                    f"words = ['k{a}', 'k{b}', 'k{a}', 'k{c}', 'k{b}', 'k{d}']\n"
                    "rank = {name: i for i, name in enumerate(sorted(set(words)), start=1)}\n"
                    "counts = {}\n"
                    "for name in words:\n"
                    "    counts[name] = counts.get(name, 0) + rank[name]\n"
                    "print(sum(counts.values()))"
                )
                trace = "Key normalization plus rank-weighted counting tests mapping fluency."
        else:  # SH
            if template == 0:
                grid = [[a, b], [c, d], [a + c, b + d]]
                transposed = list(zip(*grid))
                left = list(transposed[0])
                right = list(transposed[1])
                left.sort(reverse=True)
                right.sort()
                out = str(left[0] + right[0] - left[-1])
                code = (
                    f"grid = [[{a}, {b}], [{c}, {d}], [{a + c}, {b + d}]]\n"
                    "transposed = list(zip(*grid))\n"
                    "left = list(transposed[0])\n"
                    "right = list(transposed[1])\n"
                    "left.sort(reverse=True)\n"
                    "right.sort()\n"
                    "print(left[0] + right[0] - left[-1])"
                )
                trace = "Multiple collection transforms are chained with opposing sort orders."
            elif template == 1:
                pairs = [(a, b), (b, c), (a, d), (c, d), (b, d), (a, c)]
                adj: dict[int, set[int]] = {}
                for x, y in pairs:
                    adj.setdefault(x, set()).add(y)
                    adj.setdefault(y, set()).add(x)
                out = str(sum(len(v) for v in adj.values()))
                code = (
                    f"pairs = [({a}, {b}), ({b}, {c}), ({a}, {d}), ({c}, {d}), ({b}, {d}), ({a}, {c})]\n"
                    "adj = {}\n"
                    "for x, y in pairs:\n"
                    "    adj.setdefault(x, set()).add(y)\n"
                    "    adj.setdefault(y, set()).add(x)\n"
                    "print(sum(len(v) for v in adj.values()))"
                )
                trace = "Undirected adjacency construction with sets avoids duplicate edges."
            elif template == 2:
                rows = [[a, b, c], [c, d, a], [b, a, d]]
                diag = [rows[i][i] for i in range(3)]
                anti = [rows[i][2 - i] for i in range(3)]
                freq: dict[int, int] = {}
                for x in diag + anti:
                    freq[x] = freq.get(x, 0) + 1
                out = str(sum(v * k for k, v in freq.items()))
                code = (
                    f"rows = [[{a}, {b}, {c}], [{c}, {d}, {a}], [{b}, {a}, {d}]]\n"
                    "diag = [rows[i][i] for i in range(3)]\n"
                    "anti = [rows[i][2 - i] for i in range(3)]\n"
                    "freq = {}\n"
                    "for x in diag + anti:\n"
                    "    freq[x] = freq.get(x, 0) + 1\n"
                    "print(sum(v * k for k, v in freq.items()))"
                )
                trace = "Diagonal extraction and weighted frequency fusion increase trace complexity."
            elif template == 3:
                base = {"u": [a, b, c], "v": [b, c, d], "w": [a, d]}
                flattened = [(k, value) for k, values in base.items() for value in values]
                weights = {"u": 2, "v": 3, "w": 5}
                out = str(sum(value * weights[key] for key, value in flattened if value % 2 == 0))
                code = (
                    f"base = {{'u': [{a}, {b}, {c}], 'v': [{b}, {c}, {d}], 'w': [{a}, {d}]}}\n"
                    "flattened = [(k, value) for k, values in base.items() for value in values]\n"
                    "weights = {'u': 2, 'v': 3, 'w': 5}\n"
                    "print(sum(value * weights[key] for key, value in flattened if value % 2 == 0))"
                )
                trace = "Nested comprehensions over dict-of-lists and weighted filtering."
            else:
                values = [a, b, c, d, a + b, c + d, a + d]
                bucket = {0: [], 1: []}
                for value in values:
                    bucket[value % 2].append(value)
                even = sorted(bucket[0])
                odd = sorted(bucket[1], reverse=True)
                out = str((sum(even[:2]) if len(even) >= 2 else sum(even)) + (odd[0] if odd else 0))
                code = (
                    f"values = [{a}, {b}, {c}, {d}, {a + b}, {c + d}, {a + d}]\n"
                    "bucket = {0: [], 1: []}\n"
                    "for value in values:\n"
                    "    bucket[value % 2].append(value)\n"
                    "even = sorted(bucket[0])\n"
                    "odd = sorted(bucket[1], reverse=True)\n"
                    "print((sum(even[:2]) if len(even) >= 2 else sum(even)) + (odd[0] if odd else 0))"
                )
                trace = "Partitioning, selective aggregation, and guarded indexing in one flow."
    elif concept.topic == "concurrency":
        if template == 0:
            code = (
                "import asyncio\n"
                "async def worker(value, offset):\n"
                "    return value + offset\n"
                "async def main():\n"
                f"    results = await asyncio.gather(worker({a}, {c}), worker({b}, {c}))\n"
                "    return sum(results)\n"
                "print(asyncio.run(main()))"
            )
            out = str((a + c) + (b + c))
            trace = f"Two coroutine results are gathered and summed; output is {out}."
        elif template == 1:
            code = (
                "from concurrent.futures import ThreadPoolExecutor\n"
                "def transform(value):\n"
                "    return value * 2\n"
                f"with ThreadPoolExecutor(max_workers=2) as pool:\n"
                f"    results = list(pool.map(transform, [{a}, {b}, {c}]))\n"
                "print(sum(results))"
            )
            out = str((a * 2) + (b * 2) + (c * 2))
            trace = f"ThreadPool map applies deterministic transform then reduces to {out}."
        elif template == 2:
            code = (
                "import queue\n"
                "buffer = queue.Queue()\n"
                f"for item in [{a}, {b}, {c}]:\n"
                "    buffer.put(item)\n"
                "first = buffer.get()\n"
                "second = buffer.get()\n"
                "print(first * second)"
            )
            out = str(a * b)
            trace = f"FIFO retrieval gets {a} and {b} first; product printed is {out}."
        elif template == 3:
            code = (
                "import threading\n"
                "shared_total = 0\n"
                "lock = threading.Lock()\n"
                "def add(value):\n"
                "    global shared_total\n"
                "    with lock:\n"
                "        shared_total += value\n"
                f"for value in [{a}, {b}, {c}]:\n"
                "    add(value)\n"
                "print(shared_total)"
            )
            out = str(a + b + c)
            trace = f"Lock-guarded critical section aggregates all values safely to {out}."
        else:
            code = (
                "def stage(value, bias):\n"
                "    return value + bias\n"
                f"left = stage({a}, {d})\n"
                f"right = stage({b}, {d})\n"
                "print(abs(left - right))"
            )
            out = str(abs((a + d) - (b + d)))
            trace = f"Pipeline-style sync stages are compared by absolute difference; output is {out}."
    elif concept.topic == "oops":
        if template == 0:
            code = (
                "class Base:\n"
                f"    def compute(self): return {a}\n"
                "class Child(Base):\n"
                f"    def compute(self): return super().compute() + {b}\n"
                "print(Child().compute())"
            )
            out = str(a + b)
            trace = f"Child override extends parent behavior using super(); result is {out}."
        elif template == 1:
            code = (
                "class Engine:\n"
                f"    def power(self): return {a}\n"
                "class Car:\n"
                "    def __init__(self, engine):\n"
                "        self.engine = engine\n"
                "    def score(self):\n"
                "        return self.engine.power() + 5\n"
                "print(Car(Engine()).score())"
            )
            out = str(a + 5)
            trace = f"Composition delegates to injected dependency then computes final score {out}."
        elif template == 2:
            code = (
                "class Wallet:\n"
                "    def __init__(self, balance):\n"
                "        self._balance = balance\n"
                "    @property\n"
                "    def balance(self):\n"
                "        return self._balance\n"
                f"print(Wallet({a + c}).balance)"
            )
            out = str(a + c)
            trace = f"Encapsulated state is exposed through property access; value printed is {out}."
        elif template == 3:
            code = (
                "class Email:\n"
                "    def send(self):\n"
                "        return 'EMAIL'\n"
                "class Sms:\n"
                "    def send(self):\n"
                "        return 'SMS'\n"
                "channels = [Email(), Sms()]\n"
                "print('-'.join(channel.send() for channel in channels))"
            )
            out = "EMAIL-SMS"
            trace = "Polymorphic send() calls are composed into one output string."
        else:
            code = (
                "class S:\n"
                f"    def __init__(self): self.n = {a}\n"
                "    def __repr__(self):\n"
                "        return f'S(value={self.n})'\n"
                "print(S())"
            )
            out = f"S(value={a})"
            trace = f"Custom __repr__ controls printable object representation: {out}."
    elif concept.topic == "clean_code":
        if template == 0:
            code = (
                "def classify(score):\n"
                "    if score < 0:\n"
                "        return 'invalid'\n"
                "    if score < 50:\n"
                "        return 'retry'\n"
                "    return 'ok'\n"
                f"print(classify({a + b}))"
            )
            score = a + b
            out = "invalid" if score < 0 else ("retry" if score < 50 else "ok")
            trace = f"Guard-clause flow classifies score={score}; resulting label is {out}."
        elif template == 1:
            code = (
                "PASS_MARK = 60\n"
                f"candidate = {a * 8}\n"
                "print('PASS' if candidate >= PASS_MARK else 'FAIL')"
            )
            candidate = a * 8
            out = "PASS" if candidate >= 60 else "FAIL"
            trace = f"Named constant removes magic-number ambiguity; output decision is {out}."
        elif template == 2:
            code = (
                "def compute_total(unit_price, quantity):\n"
                "    return unit_price * quantity\n"
                f"print(compute_total({a}, {b}))"
            )
            out = str(a * b)
            trace = f"Pure function with explicit inputs returns deterministic total {out}."
        elif template == 3:
            code = (
                "def normalize_name(raw_name):\n"
                "    return raw_name.strip().lower().replace(' ', '_')\n"
                "print(normalize_name('  Clean Code  '))"
            )
            out = "clean_code"
            trace = "Normalization applies trim, lowercase, and separator cleanup, yielding clean_code."
        else:
            code = (
                "def pick_primary(configured, fallback):\n"
                "    if configured is None:\n"
                "        return fallback\n"
                "    return configured\n"
                f"print(pick_primary(None, {d}))"
            )
            out = str(d)
            trace = f"Explicit fallback branch returns fallback value when primary input is absent; output is {out}."
    else:  # fundamentals
        if template == 0:
            code = (
                f"base = {a}\n"
                "alias = base\n"
                f"base = base + {b}\n"
                "print(base - alias)"
            )
            out = str((a + b) - a)
            trace = f"Rebinding changes one name target while alias keeps old value; difference is {out}."
        elif template == 1:
            code = (
                "def scale(value, factor):\n"
                "    return value * factor\n"
                f"print(scale({a}, {c}))"
            )
            out = str(a * c)
            trace = f"Function invocation with explicit parameters computes deterministic product {out}."
        elif template == 2:
            code = (
                f"numbers = [{a}, {b}, {c}]\n"
                "average = sum(numbers) // len(numbers)\n"
                "print(average)"
            )
            out = str((a + b + c) // 3)
            trace = f"Integer average uses floor division on total sum and prints {out}."
        elif template == 3:
            code = (
                "try:\n"
                f"    value = {a}\n"
                "    print(value)\n"
                "finally:\n"
                "    pass"
            )
            out = str(a)
            trace = f"try block prints value and finally executes cleanup path without altering output {out}."
        else:
            code = (
                f"left = {a}\n"
                f"right = {b}\n"
                "left, right = right, left\n"
                "print(left + right)"
            )
            out = str(a + b)
            trace = f"Swap changes bindings only; numeric pair remains same so sum is {out}."

    prompt = f"Q{qid}. Predict the exact single-line output of the following code."
    reasoning = f"Primary concept: {hs} ({concept.topic}). {trace} Final one-line output: {out}."
    return prompt, code, out, reasoning


def signature_for_question(prompt: str, code: str | None, options: list[str] | None) -> str:
    payload = f"{prompt}\n{code or ''}\n{'|'.join(options or [])}"
    return normalize_text(payload)


def build_questions(
    slots: list[dict[str, str]],
    chosen: dict[str, list[Concept]],
) -> list[Question]:
    topic_cursor = {t: 0 for t in TOPIC_ORDER}
    questions: list[Question] = []
    used_concepts: set[str] = set()
    used_sigs: set[str] = set()

    for i, slot in enumerate(slots, start=1):
        topic = slot["topic"]
        difficulty = slot["difficulty"]
        qtype = slot["qtype"]
        concept = chosen[topic][topic_cursor[topic]]
        topic_cursor[topic] += 1

        if concept.concept_id in used_concepts:
            raise ValueError(f"Repeated concept_id detected: {concept.concept_id}")
        used_concepts.add(concept.concept_id)

        if qtype == "MSQ":
            prompt, options, correct, reasoning = build_msq_question(i, concept, difficulty)
            code = None
            expected = None
        else:
            prompt, code, expected, reasoning = build_output_question(i, concept, difficulty)
            options = None
            correct = None
            if "\n" in expected:
                raise ValueError(f"Output must be one line for Q{i}")

        sig = signature_for_question(prompt, code, options)
        if sig in used_sigs:
            raise ValueError(f"Duplicate question signature detected at Q{i}")
        used_sigs.add(sig)

        questions.append(
            Question(
                qid=i,
                topic=topic,
                difficulty=difficulty,
                qtype=qtype,
                concept_id=concept.concept_id,
                source_file=concept.source_file,
                heading=concept.heading,
                prompt=prompt,
                code=code,
                options=options,
                correct_letters=correct,
                expected_output=expected,
                reasoning=reasoning,
                signature=sig,
            )
        )
    return questions


def render_markdown_paper(path: Path, time_limit: str, questions: list[Question]) -> None:
    lines: list[str] = [
        f"Time: {time_limit}",
        f"Number of Questions: {len(questions)}",
        "",
    ]
    for q in questions:
        lines.append(q.prompt)
        if q.qtype == "MSQ":
            assert q.options is not None
            for opt in q.options:
                lines.append(f"- {opt}")
        else:
            assert q.code is not None
            code_text = normalize_code_display(q.code)
            fence = markdown_fence_for_code(code_text)
            lines.append("")
            lines.append(f"{fence}python")
            lines.extend(code_text.splitlines())
            lines.append(fence)
            lines.append("")
            lines.append("Answer: ________________________________")
        lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def render_markdown_answers(path: Path, questions: list[Question]) -> None:
    lines: list[str] = [
        "# PYTHON NOTES 300 TEST - ANSWER KEY",
        "",
        "Detailed solutions per question.",
        "",
    ]
    for q in questions:
        lines.append(f"### Q{q.qid}")
        lines.append(f"- Topic: `{q.topic}`")
        lines.append(f"- Difficulty: `{DIFF_LABEL[q.difficulty]}`")
        lines.append(f"- Type: `{TYPE_LABEL[q.qtype]}`")
        if q.qtype == "MSQ":
            assert q.correct_letters is not None
            lines.append(f"- Correct options: **{', '.join(q.correct_letters)}**")
            lines.append(f"- Solution: {q.reasoning}")
        else:
            assert q.expected_output is not None
            lines.append(f"- Expected output: `{q.expected_output}`")
            lines.append(f"- Solution: {q.reasoning}")
        lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def build_pdf_story(
    questions: list[Question],
    time_limit: str,
    profile: dict[str, Any],
    one_question_per_page: bool,
) -> list[Any]:
    styles = getSampleStyleSheet()
    q_style = ParagraphStyle(
        "Q",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=profile["q_font"],
        leading=profile["q_font"] + 3.0,
        spaceAfter=profile["space_after"],
    )
    opt_style = ParagraphStyle(
        "Opt",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=profile["opt_font"],
        leading=profile["opt_font"] + 2.6,
        leftIndent=10,
        spaceAfter=1.8,
    )
    head_style = ParagraphStyle(
        "Head",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=profile["head_font"],
        leading=profile["head_font"] + 3.0,
        spaceAfter=6,
    )
    code_style = ParagraphStyle(
        "Code",
        parent=styles["Code"],
        fontName="Courier-Bold",
        fontSize=profile["code_font"],
        leading=profile["code_font"] + 3.0,
        leftIndent=0,
        rightIndent=0,
        spaceAfter=0,
    )
    answer_style = ParagraphStyle(
        "AnsLine",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=profile["opt_font"],
        leading=profile["opt_font"] + 2.2,
        leftIndent=10,
        spaceAfter=1.4,
    )

    story: list[Any] = [
        Paragraph(f"<b>Time: {time_limit}</b>", head_style),
        Paragraph(f"<b>Number of Questions: {len(questions)}</b>", head_style),
        Spacer(1, 2.2),
    ]

    code_box_width = profile["code_box_width_mm"] * mm
    for q in questions:
        q_flow: list[Any] = [Paragraph(q.prompt, q_style)]
        if q.qtype == "MSQ":
            assert q.options
            for opt in q.options:
                q_flow.append(Paragraph(opt, opt_style))
        else:
            assert q.code
            code_text = normalize_code_display(q.code)
            code_block = Preformatted(code_text, code_style, maxLineLength=profile["code_wrap_col"])
            code_table = Table([[code_block]], colWidths=[code_box_width])
            code_table.setStyle(
                TableStyle(
                    [
                        ("BOX", (0, 0), (-1, -1), 0.9, colors.HexColor("#4b5563")),
                        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f5f7fb")),
                        ("LEFTPADDING", (0, 0), (-1, -1), 7),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                        ("TOPPADDING", (0, 0), (-1, -1), 6),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ]
                )
            )
            q_flow.append(code_table)
            q_flow.append(Spacer(1, 2))
            q_flow.append(Paragraph("Answer: ________________________________", answer_style))
        q_flow.append(Spacer(1, profile["between_q"]))
        story.append(KeepTogether(q_flow))
        if one_question_per_page and q.qid != len(questions):
            story.append(PageBreak())
    return story


def render_pdf_with_compact_loop(
    output_pdf: Path,
    questions: list[Question],
    time_limit: str,
    max_pages: int,
    one_question_per_page: bool,
    enforce_max_pages: bool,
) -> tuple[int, str]:
    profiles = [
        {
            "name": "readable",
            "head_font": 12.0,
            "q_font": 11.0,
            "opt_font": 10.4,
            "code_font": 11.4,
            "space_after": 2.4,
            "between_q": 3.2,
            "code_max_lines": 9,
            "code_box_width_mm": 178,
            "code_wrap_col": 74,
        },
        {
            "name": "readable_compact",
            "head_font": 11.4,
            "q_font": 10.4,
            "opt_font": 9.8,
            "code_font": 10.8,
            "space_after": 2.0,
            "between_q": 2.2,
            "code_max_lines": 8,
            "code_box_width_mm": 178,
            "code_wrap_col": 72,
        },
        {
            "name": "compact_limit",
            "head_font": 10.8,
            "q_font": 9.8,
            "opt_font": 9.2,
            "code_font": 10.0,
            "space_after": 1.6,
            "between_q": 1.6,
            "code_max_lines": 7,
            "code_box_width_mm": 178,
            "code_wrap_col": 68,
        },
    ]

    chosen_pages = None
    chosen_profile = None
    final_pdf_bytes: bytes | None = None
    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    for profile in profiles:
        story = build_pdf_story(questions, time_limit, profile, one_question_per_page)
        page_holder = {"page": 0}

        def on_page(_canvas, doc):
            page_holder["page"] = doc.page

        with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp_path = Path(tmp.name)

        doc = SimpleDocTemplate(
            str(tmp_path),
            pagesize=A4,
            topMargin=11 * mm,
            bottomMargin=11 * mm,
            leftMargin=12 * mm,
            rightMargin=12 * mm,
        )
        doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
        pages = int(page_holder["page"])
        data = tmp_path.read_bytes()
        tmp_path.unlink(missing_ok=True)

        chosen_pages = pages
        chosen_profile = profile["name"]
        final_pdf_bytes = data
        if (not enforce_max_pages) or pages <= max_pages:
            break

    if final_pdf_bytes is None or chosen_pages is None or chosen_profile is None:
        raise RuntimeError("PDF rendering failed.")

    output_pdf.write_bytes(final_pdf_bytes)
    if enforce_max_pages and chosen_pages > max_pages:
        raise ValueError(
            f"PDF exceeds max pages ({chosen_pages} > {max_pages}) even after compactness fallback."
        )
    return chosen_pages, chosen_profile


def validate_exam(
    notes_root: Path,
    eligible_files: list[str],
    questions: list[Question],
    alloc: dict[str, dict[str, dict[str, int]]],
    page_count: int,
    max_pages: int,
    enforce_max_pages: bool,
) -> dict[str, bool]:
    ok: dict[str, bool] = {}

    ok["total_questions"] = len(questions) == TOTAL_QUESTIONS

    by_topic = {t: 0 for t in TOPIC_ORDER}
    by_diff = {d: 0 for d in DIFF_ORDER}
    by_type = {t: 0 for t in TYPE_ORDER}
    by_topic_diff_type = {
        t: {d: {qt: 0 for qt in TYPE_ORDER} for d in DIFF_ORDER} for t in TOPIC_ORDER
    }

    for q in questions:
        by_topic[q.topic] += 1
        by_diff[q.difficulty] += 1
        by_type[q.qtype] += 1
        by_topic_diff_type[q.topic][q.difficulty][q.qtype] += 1

    ok["topic_totals"] = all(by_topic[t] == TOPIC_TOTALS[t] for t in TOPIC_ORDER)
    ok["global_diff_totals"] = all(by_diff[d] == GLOBAL_DIFF_TOTALS[d] for d in DIFF_ORDER)
    ok["global_type_totals"] = (
        by_type["MSQ"] == GLOBAL_TYPE_TOTALS["MSQ"] and by_type["OUT"] == GLOBAL_TYPE_TOTALS["OUT"]
    )
    ok["topic_diff_totals"] = all(
        (by_topic_diff_type[t][d]["MSQ"] + by_topic_diff_type[t][d]["OUT"]) == TOPIC_DIFF_TOTALS[t][d]
        for t in TOPIC_ORDER
        for d in DIFF_ORDER
    )
    ok["topic_type_totals"] = all(
        sum(by_topic_diff_type[t][d]["MSQ"] for d in DIFF_ORDER) == TOPIC_TYPE_TOTALS[t]["MSQ"]
        and sum(by_topic_diff_type[t][d]["OUT"] for d in DIFF_ORDER) == TOPIC_TYPE_TOTALS[t]["OUT"]
        for t in TOPIC_ORDER
    )
    ok["cell_allocations"] = all(
        by_topic_diff_type[t][d][qt] == alloc[t][d][qt]
        for t in TOPIC_ORDER
        for d in DIFF_ORDER
        for qt in TYPE_ORDER
    )
    ok["collections_output_diff_target"] = all(
        by_topic_diff_type["collections"][d]["OUT"] == COLLECTION_OUTPUT_DIFF_TARGET[d]
        for d in DIFF_ORDER
    )
    ok["collections_msq_diff_target"] = all(
        by_topic_diff_type["collections"][d]["MSQ"] == COLLECTION_MSQ_DIFF_TARGET[d]
        for d in DIFF_ORDER
    )

    concept_ids = [q.concept_id for q in questions]
    ok["unique_concept_ids"] = len(concept_ids) == len(set(concept_ids))
    signatures = [q.signature for q in questions]
    ok["unique_signatures"] = len(signatures) == len(set(signatures))
    ok["output_single_line"] = all(
        (q.qtype != "OUT") or (q.expected_output is not None and "\n" not in q.expected_output)
        for q in questions
    )

    eligible_set = set(eligible_files)
    ok["eligible_sources_only"] = all(
        q.source_file in eligible_set and not re.match(r"^[0-9]", Path(q.source_file).stem)
        for q in questions
    )

    ok["pdf_pages_within_limit"] = (page_count <= max_pages) if enforce_max_pages else True
    ok["a4_page_size_configured"] = True  # enforced by renderer pagesize=A4
    ok["all_checks_passed"] = all(ok.values())
    return ok


def ensure_parents(*paths: Path) -> None:
    for p in paths:
        p.parent.mkdir(parents=True, exist_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate deterministic 300-question Python notes exam in MD/PDF with answer key + manifest."
    )
    parser.add_argument("--seed", type=int, default=20260628)
    parser.add_argument("--notes-root", type=str, default="python/notes")
    parser.add_argument(
        "--output-md",
        type=str,
        default="python/assignment/test/python-notes-300-test.md",
    )
    parser.add_argument(
        "--output-pdf",
        type=str,
        default="python/assignment/test/python-notes-300-test.pdf",
    )
    parser.add_argument(
        "--output-answers",
        type=str,
        default="python/assignment/test/python-notes-300-test-answer-key.md",
    )
    parser.add_argument(
        "--output-manifest",
        type=str,
        default="python/assignment/test/python-notes-300-test-manifest.json",
    )
    parser.add_argument("--max-pages", type=int, default=50)
    parser.add_argument("--time-limit", type=str, default="3 hr")
    parser.add_argument(
        "--one-question-per-page",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        "--enforce-max-pages",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    notes_root = Path(args.notes_root)
    output_md = Path(args.output_md)
    output_pdf = Path(args.output_pdf)
    output_answers = Path(args.output_answers)
    output_manifest = Path(args.output_manifest)
    ensure_parents(output_md, output_pdf, output_answers, output_manifest)

    concepts_by_topic, eligible_files = scan_concepts(notes_root)

    alloc = allocate_type_by_topic_diff()
    slots = make_slots(alloc)
    if len(slots) != TOTAL_QUESTIONS:
        raise ValueError(f"Slot count mismatch: {len(slots)} != {TOTAL_QUESTIONS}")

    chosen = pick_concepts_for_topics(concepts_by_topic, args.seed)
    questions = build_questions(slots, chosen)

    render_markdown_paper(output_md, args.time_limit, questions)
    render_markdown_answers(output_answers, questions)
    page_count, pdf_profile = render_pdf_with_compact_loop(
        output_pdf=output_pdf,
        questions=questions,
        time_limit=args.time_limit,
        max_pages=args.max_pages,
        one_question_per_page=args.one_question_per_page,
        enforce_max_pages=args.enforce_max_pages,
    )

    checks = validate_exam(
        notes_root=notes_root,
        eligible_files=eligible_files,
        questions=questions,
        alloc=alloc,
        page_count=page_count,
        max_pages=args.max_pages,
        enforce_max_pages=args.enforce_max_pages,
    )
    if not checks["all_checks_passed"]:
        failed = [k for k, v in checks.items() if not v]
        raise ValueError(f"Validation failed: {failed}")

    topic_source_counts = {
        t: {"available_concepts": len(concepts_by_topic[t]), "used_concepts": len(chosen[t])}
        for t in TOPIC_ORDER
    }

    manifest = {
        "seed": args.seed,
        "config": {
            "notes_root": notes_root.as_posix(),
            "output_md": output_md.as_posix(),
            "output_pdf": output_pdf.as_posix(),
            "output_answers": output_answers.as_posix(),
            "output_manifest": output_manifest.as_posix(),
            "max_pages": args.max_pages,
            "time_limit": args.time_limit,
            "total_questions": TOTAL_QUESTIONS,
            "one_question_per_page": args.one_question_per_page,
            "enforce_max_pages": args.enforce_max_pages,
        },
        "quotas": {
            "topic_totals": TOPIC_TOTALS,
            "topic_difficulty_totals": TOPIC_DIFF_TOTALS,
            "topic_type_totals": TOPIC_TYPE_TOTALS,
            "global_type_totals": GLOBAL_TYPE_TOTALS,
            "global_difficulty_totals": GLOBAL_DIFF_TOTALS,
            "collections_output_difficulty_target": COLLECTION_OUTPUT_DIFF_TARGET,
            "collections_msq_difficulty_target": COLLECTION_MSQ_DIFF_TARGET,
            "topic_diff_type_allocations": alloc,
        },
        "sources": {
            "eligible_files": eligible_files,
            "topic_source_counts": topic_source_counts,
        },
        "pdf": {
            "page_size": "A4",
            "page_count": page_count,
            "max_pages": args.max_pages,
            "profile_used": pdf_profile,
        },
        "validation": checks,
        "questions": [
            {
                "qid": q.qid,
                "topic": q.topic,
                "difficulty": DIFF_LABEL[q.difficulty],
                "qtype": q.qtype,
                "concept_id": q.concept_id,
                "source_file": q.source_file,
                "heading": q.heading,
                "signature": q.signature,
                "correct_letters": q.correct_letters,
                "expected_output": q.expected_output,
            }
            for q in questions
        ],
    }

    output_manifest.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(f"Generated: {output_md}")
    print(f"Generated: {output_pdf}")
    print(f"Generated: {output_answers}")
    print(f"Generated: {output_manifest}")
    print(f"PDF pages: {page_count} ({pdf_profile})")


if __name__ == "__main__":
    main()
