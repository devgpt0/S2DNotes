from __future__ import annotations

import argparse
import random
import re
from dataclasses import dataclass
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


TOPICS = ("sync", "async", "multithreaded")
LEVELS = ("L1", "L2")
QTYPES = ("output", "mcq")

DEFAULT_DISTRIBUTION = {
    "sync": {"L1": {"output": 4, "mcq": 4}, "L2": {"output": 8, "mcq": 4}},
    "async": {"L1": {"output": 8, "mcq": 6}, "L2": {"output": 16, "mcq": 10}},
    "multithreaded": {"L1": {"output": 8, "mcq": 6}, "L2": {"output": 16, "mcq": 10}},
}


@dataclass(frozen=True)
class Question:
    topic: str
    level: str
    qtype: str
    prompt: str
    concept: str
    code: str | None = None
    options: tuple[str, ...] | None = None


class AnswerLines(Flowable):
    """Draw lined answer area for hand-written responses."""

    def __init__(self, line_count: int, line_gap: float = 9.0) -> None:
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


def validate_distribution(distribution: dict) -> None:
    for topic in TOPICS:
        if topic not in distribution:
            raise ValueError(f"Missing topic in distribution: {topic}")
        for level in LEVELS:
            if level not in distribution[topic]:
                raise ValueError(f"Missing level {level} for topic {topic}")
            for qtype in QTYPES:
                if qtype not in distribution[topic][level]:
                    raise ValueError(f"Missing type {qtype} for {topic}/{level}")
                value = distribution[topic][level][qtype]
                if not isinstance(value, int) or value < 0:
                    raise ValueError(f"Invalid count for {topic}/{level}/{qtype}: {value}")


def rand_int_list(rng: random.Random, n: int, low: int = 1, high: int = 20) -> list[int]:
    return [rng.randint(low, high) for _ in range(n)]


def question_signature(q: Question) -> str:
    options = "\n".join(q.options or ())
    payload = f"{q.topic}|{q.level}|{q.qtype}|{q.prompt}\n{q.code or ''}\n{options}"
    return normalize_text(payload)


# -----------------------------
# Output question patterns
# -----------------------------
def sync_l1_patterns() -> list[Callable[[random.Random, int], tuple[str, str, str]]]:
    def p1(rng: random.Random, v: int) -> tuple[str, str, str]:
        d1 = rng.randint(1, 3)
        d2 = rng.randint(1, 3)
        return (
            "Predict the output for strictly sequential sync workflow.",
            (
                "def fetch(name, delay):\n"
                "    print(f'start-{name}')\n"
                "    # blocking call simulated\n"
                "    print(f'end-{name}', delay)\n\n"
                f"fetch('A', {d1})\n"
                f"fetch('B', {d2})\n"
                "print('done')"
            ),
            "sync_sequential_control_flow",
        )

    def p2(rng: random.Random, v: int) -> tuple[str, str, str]:
        fail_at = rng.randint(1, 3)
        return (
            "Predict output for sync retry loop with break/else.",
            (
                "for attempt in range(1, 4):\n"
                f"    if attempt == {fail_at}:\n"
                "        print('ok', attempt)\n"
                "        break\n"
                "    print('retry', attempt)\n"
                "else:\n"
                "    print('failed')"
            ),
            "sync_retry_pattern",
        )

    def p3(rng: random.Random, v: int) -> tuple[str, str, str]:
        timeout = rng.randint(2, 5)
        return (
            "Predict output for sync timeout fallback path.",
            (
                "def call(timeout):\n"
                "    if timeout < 3:\n"
                "        raise TimeoutError('slow')\n"
                "    return 'ok'\n\n"
                "try:\n"
                f"    print(call({timeout}))\n"
                "except TimeoutError:\n"
                "    print('fallback')\n"
                "finally:\n"
                "    print('cleanup')"
            ),
            "sync_timeout_handling",
        )

    def p4(rng: random.Random, v: int) -> tuple[str, str, str]:
        nums = rand_int_list(rng, 4, 1, 9)
        return (
            "Predict output for CPU-bound style sync aggregation.",
            (
                f"nums = {nums}\n"
                "total = 0\n"
                "for x in nums:\n"
                "    total += x * x\n"
                "print(total)\n"
                "print('cpu-bound')"
            ),
            "sync_cpu_bound_loop",
        )

    def p5(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict output for call stack order in sync functions.",
            (
                "def a():\n"
                "    print('a1')\n"
                "    b()\n"
                "    print('a2')\n\n"
                "def b():\n"
                "    print('b1')\n"
                "    c()\n"
                "    print('b2')\n\n"
                "def c():\n"
                "    print('c')\n\n"
                "a()"
            ),
            "sync_call_stack",
        )

    def p6(rng: random.Random, v: int) -> tuple[str, str, str]:
        attempts = rng.randint(2, 4)
        return (
            "Predict output for sync retry with exponential-style backoff marker.",
            (
                "delay = 1\n"
                f"for i in range({attempts}):\n"
                "    print('attempt', i + 1, 'delay', delay)\n"
                "    delay *= 2\n"
                "print('final-delay', delay)"
            ),
            "sync_backoff_strategy",
        )

    return [p1, p2, p3, p4, p5, p6]


def sync_l2_patterns() -> list[Callable[[random.Random, int], tuple[str, str, str]]]:
    def p1(rng: random.Random, v: int) -> tuple[str, str, str]:
        a = rng.randint(1, 4)
        b = rng.randint(5, 9)
        return (
            "Predict output for sync dependency timeout policy selection.",
            (
                "deps = {\n"
                f"    'auth': {a},\n"
                f"    'catalog': {b},\n"
                "}\n"
                "timeouts = {k: 3 if v <= 4 else 6 for k, v in deps.items()}\n"
                "print(timeouts)\n"
                "print(sum(timeouts.values()))"
            ),
            "sync_dependency_timeouts",
        )

    def p2(rng: random.Random, v: int) -> tuple[str, str, str]:
        vals = rand_int_list(rng, 5, 1, 15)
        return (
            "Predict output for sync critical-path analysis approximation.",
            (
                f"stages = {vals}\n"
                "critical = []\n"
                "for idx, ms in enumerate(stages):\n"
                "    if ms > 8:\n"
                "        critical.append((idx, ms))\n"
                "print(critical)\n"
                "print(len(critical))"
            ),
            "sync_critical_path",
        )

    def p3(rng: random.Random, v: int) -> tuple[str, str, str]:
        fail_code = rng.choice([500, 502, 503])
        return (
            "Predict output for sync error categorization and retry decision.",
            (
                "def classify(code):\n"
                "    if code >= 500:\n"
                "        return 'retry'\n"
                "    if code >= 400:\n"
                "        return 'no-retry'\n"
                "    return 'ok'\n\n"
                f"status = {fail_code}\n"
                "action = classify(status)\n"
                "print(status, action)"
            ),
            "sync_error_strategy",
        )

    def p4(rng: random.Random, v: int) -> tuple[str, str, str]:
        retries = rng.randint(2, 4)
        return (
            "Predict output for sync request wrapper with final exception path.",
            (
                "def request(attempt):\n"
                "    if attempt < 3:\n"
                "        raise TimeoutError\n"
                "    return 'ok'\n\n"
                f"max_attempts = {retries}\n"
                "for a in range(1, max_attempts + 1):\n"
                "    try:\n"
                "        print(request(a))\n"
                "        break\n"
                "    except TimeoutError:\n"
                "        print('timeout', a)\n"
                "else:\n"
                "    print('raise-final')"
            ),
            "sync_retry_exhaustion",
        )

    def p5(rng: random.Random, v: int) -> tuple[str, str, str]:
        cpu = rng.randint(40, 70)
        io = rng.randint(30, 60)
        return (
            "Predict output for CPU-bound vs I/O-bound decision helper.",
            (
                f"cpu_wait = {cpu}\n"
                f"io_wait = {io}\n"
                "if io_wait > cpu_wait:\n"
                "    model = 'async-or-threads'\n"
                "elif cpu_wait > io_wait:\n"
                "    model = 'process-or-optimized-sync'\n"
                "else:\n"
                "    model = 'mixed'\n"
                "print(model)"
            ),
            "sync_model_selection",
        )

    def p6(rng: random.Random, v: int) -> tuple[str, str, str]:
        n = rng.randint(3, 5)
        return (
            "Predict output for sync design with small pure functions and composition.",
            (
                "def parse(x):\n"
                "    return x.strip().upper()\n\n"
                "def validate(x):\n"
                "    return x.isalpha()\n\n"
                f"items = [' a ', 'b', 'c1', 'd'][:{n}]\n"
                "clean = [parse(i) for i in items]\n"
                "valid = [x for x in clean if validate(x)]\n"
                "print(clean)\n"
                "print(valid)"
            ),
            "sync_clean_pipeline",
        )

    def p7(rng: random.Random, v: int) -> tuple[str, str, str]:
        p50 = rng.randint(10, 30)
        p95 = p50 + rng.randint(20, 80)
        return (
            "Predict output for latency percentile interpretation helper.",
            (
                f"p50 = {p50}\n"
                f"p95 = {p95}\n"
                "spread = p95 - p50\n"
                "print('stable' if spread < 25 else 'tail-risk')\n"
                "print(spread)"
            ),
            "sync_latency_percentiles",
        )

    def p8(rng: random.Random, v: int) -> tuple[str, str, str]:
        x = rng.randint(2, 5)
        y = rng.randint(6, 9)
        return (
            "Predict output for deterministic sync fallback chain.",
            (
                "def primary():\n"
                "    raise ConnectionError\n\n"
                "def secondary():\n"
                f"    return {x} + {y}\n\n"
                "try:\n"
                "    print(primary())\n"
                "except ConnectionError:\n"
                "    print('using-secondary')\n"
                "    print(secondary())"
            ),
            "sync_fallback_chain",
        )

    return [p1, p2, p3, p4, p5, p6, p7, p8]


def async_l1_patterns() -> list[Callable[[random.Random, int], tuple[str, str, str]]]:
    def p1(rng: random.Random, v: int) -> tuple[str, str, str]:
        t1 = round(rng.uniform(0.01, 0.03), 2)
        t2 = round(rng.uniform(0.04, 0.06), 2)
        return (
            "Predict output for create_task concurrency and await order.",
            (
                "import asyncio\n\n"
                "async def work(name, delay):\n"
                "    await asyncio.sleep(delay)\n"
                "    return f'{name}-done'\n\n"
                "async def main():\n"
                f"    t1 = asyncio.create_task(work('A', {t1}))\n"
                f"    t2 = asyncio.create_task(work('B', {t2}))\n"
                "    r1 = await t1\n"
                "    r2 = await t2\n"
                "    print(r1, r2)\n\n"
                "asyncio.run(main())"
            ),
            "async_create_task",
        )

    def p2(rng: random.Random, v: int) -> tuple[str, str, str]:
        a = round(rng.uniform(0.01, 0.03), 2)
        b = round(rng.uniform(0.04, 0.06), 2)
        return (
            "Predict output for asyncio.gather result ordering.",
            (
                "import asyncio\n\n"
                "async def f(x, d):\n"
                "    await asyncio.sleep(d)\n"
                "    return x * 10\n\n"
                "async def main():\n"
                f"    out = await asyncio.gather(f(1, {b}), f(2, {a}))\n"
                "    print(out)\n\n"
                "asyncio.run(main())"
            ),
            "async_gather_order",
        )

    def p3(rng: random.Random, v: int) -> tuple[str, str, str]:
        timeout = round(rng.uniform(0.02, 0.04), 2)
        delay = round(timeout + 0.03, 2)
        return (
            "Predict output for asyncio.wait_for timeout handling.",
            (
                "import asyncio\n\n"
                "async def slow():\n"
                f"    await asyncio.sleep({delay})\n"
                "    return 'done'\n\n"
                "async def main():\n"
                "    try:\n"
                f"        print(await asyncio.wait_for(slow(), timeout={timeout}))\n"
                "    except TimeoutError:\n"
                "        print('timeout')\n\n"
                "asyncio.run(main())"
            ),
            "async_wait_for",
        )

    def p4(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict output for cancellation propagation in awaited task.",
            (
                "import asyncio\n\n"
                "async def job():\n"
                "    try:\n"
                "        await asyncio.sleep(1)\n"
                "    except asyncio.CancelledError:\n"
                "        print('job-cancelled')\n"
                "        raise\n\n"
                "async def main():\n"
                "    t = asyncio.create_task(job())\n"
                "    await asyncio.sleep(0)\n"
                "    t.cancel()\n"
                "    try:\n"
                "        await t\n"
                "    except asyncio.CancelledError:\n"
                "        print('main-cancelled')\n\n"
                "asyncio.run(main())"
            ),
            "async_cancellation",
        )

    def p5(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict output for asyncio.to_thread bridging blocking function.",
            (
                "import asyncio\n\n"
                "def blocking(n):\n"
                "    return n * n\n\n"
                "async def main():\n"
                "    x = await asyncio.to_thread(blocking, 7)\n"
                "    print(x)\n\n"
                "asyncio.run(main())"
            ),
            "async_to_thread",
        )

    def p6(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict output for TaskGroup structured concurrency success case.",
            (
                "import asyncio\n\n"
                "async def worker(name, d):\n"
                "    await asyncio.sleep(d)\n"
                "    return f'{name}:{d}'\n\n"
                "async def main():\n"
                "    results = []\n"
                "    async with asyncio.TaskGroup() as tg:\n"
                "        t1 = tg.create_task(worker('A', 0.01))\n"
                "        t2 = tg.create_task(worker('B', 0.02))\n"
                "    results.append(t1.result())\n"
                "    results.append(t2.result())\n"
                "    print(results)\n\n"
                "asyncio.run(main())"
            ),
            "async_taskgroup_basics",
        )

    def p7(rng: random.Random, v: int) -> tuple[str, str, str]:
        limit = rng.randint(2, 4)
        return (
            "Predict output for semaphore-limited async task completion shape.",
            (
                "import asyncio\n\n"
                "async def bounded(x, sem):\n"
                "    async with sem:\n"
                "        await asyncio.sleep(0.01)\n"
                "        return x * 2\n\n"
                "async def main():\n"
                f"    sem = asyncio.Semaphore({limit})\n"
                "    tasks = [bounded(i, sem) for i in range(5)]\n"
                "    print(await asyncio.gather(*tasks))\n\n"
                "asyncio.run(main())"
            ),
            "async_semaphore_limit",
        )

    def p8(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict output for producer-consumer using asyncio.Queue sentinel.",
            (
                "import asyncio\n\n"
                "async def producer(q):\n"
                "    for i in [1, 2, 3]:\n"
                "        await q.put(i)\n"
                "    await q.put(None)\n\n"
                "async def consumer(q):\n"
                "    out = []\n"
                "    while True:\n"
                "        item = await q.get()\n"
                "        if item is None:\n"
                "            q.task_done()\n"
                "            break\n"
                "        out.append(item * 10)\n"
                "        q.task_done()\n"
                "    return out\n\n"
                "async def main():\n"
                "    q = asyncio.Queue(maxsize=2)\n"
                "    c = asyncio.create_task(consumer(q))\n"
                "    await producer(q)\n"
                "    await q.join()\n"
                "    print(await c)\n\n"
                "asyncio.run(main())"
            ),
            "async_queue_sentinel",
        )

    return [p1, p2, p3, p4, p5, p6, p7, p8]


def async_l2_patterns() -> list[Callable[[random.Random, int], tuple[str, str, str]]]:
    def p1(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict output for async lock around shared mutable state.",
            (
                "import asyncio\n\n"
                "counter = 0\n"
                "lock = asyncio.Lock()\n\n"
                "async def inc_many(n):\n"
                "    global counter\n"
                "    for _ in range(n):\n"
                "        async with lock:\n"
                "            tmp = counter\n"
                "            await asyncio.sleep(0)\n"
                "            counter = tmp + 1\n\n"
                "async def main():\n"
                "    await asyncio.gather(inc_many(30), inc_many(30), inc_many(40))\n"
                "    print(counter)\n\n"
                "asyncio.run(main())"
            ),
            "async_lock_shared_state",
        )

    def p2(rng: random.Random, v: int) -> tuple[str, str, str]:
        timeout = round(rng.uniform(0.02, 0.04), 2)
        return (
            "Predict output for asyncio.timeout context manager.",
            (
                "import asyncio\n\n"
                "async def maybe_slow():\n"
                "    await asyncio.sleep(0.06)\n"
                "    return 'ok'\n\n"
                "async def main():\n"
                "    try:\n"
                f"        async with asyncio.timeout({timeout}):\n"
                "            print(await maybe_slow())\n"
                "    except TimeoutError:\n"
                "        print('ctx-timeout')\n\n"
                "asyncio.run(main())"
            ),
            "async_timeout_context",
        )

    def p3(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict output for asyncio.shield protecting inner critical operation.",
            (
                "import asyncio\n\n"
                "async def commit():\n"
                "    await asyncio.sleep(0.03)\n"
                "    return 'committed'\n\n"
                "async def main():\n"
                "    task = asyncio.create_task(commit())\n"
                "    try:\n"
                "        async with asyncio.timeout(0.01):\n"
                "            await asyncio.shield(task)\n"
                "    except TimeoutError:\n"
                "        print('outer-timeout')\n"
                "    print(await task)\n\n"
                "asyncio.run(main())"
            ),
            "async_shield",
        )

    def p4(rng: random.Random, v: int) -> tuple[str, str, str]:
        d1 = round(rng.uniform(0.01, 0.03), 2)
        d2 = round(rng.uniform(0.04, 0.06), 2)
        return (
            "Predict output for gather exception handling with return_exceptions.",
            (
                "import asyncio\n\n"
                "async def ok(delay):\n"
                "    await asyncio.sleep(delay)\n"
                "    return 'ok'\n\n"
                "async def fail(delay):\n"
                "    await asyncio.sleep(delay)\n"
                "    raise ValueError('bad')\n\n"
                "async def main():\n"
                f"    res = await asyncio.gather(ok({d1}), fail({d2}), return_exceptions=True)\n"
                "    print(type(res[1]).__name__, res[0])\n\n"
                "asyncio.run(main())"
            ),
            "async_gather_errors",
        )

    def p5(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict output for bounded queue backpressure signal handling.",
            (
                "import asyncio\n\n"
                "async def main():\n"
                "    q = asyncio.Queue(maxsize=1)\n"
                "    await q.put('first')\n"
                "    print(q.full())\n"
                "    print(await q.get())\n"
                "    q.task_done()\n"
                "    print(q.empty())\n\n"
                "asyncio.run(main())"
            ),
            "async_backpressure_queue",
        )

    def p6(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict output for create_task naming and introspection.",
            (
                "import asyncio\n\n"
                "async def work():\n"
                "    await asyncio.sleep(0)\n"
                "    return 42\n\n"
                "async def main():\n"
                "    t = asyncio.create_task(work(), name='fetch-42')\n"
                "    print(t.get_name())\n"
                "    print(await t)\n\n"
                "asyncio.run(main())"
            ),
            "async_task_naming",
        )

    def p7(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict output for cancellation-safe cleanup with finally in coroutine.",
            (
                "import asyncio\n\n"
                "async def worker():\n"
                "    try:\n"
                "        await asyncio.sleep(1)\n"
                "    finally:\n"
                "        print('cleanup')\n\n"
                "async def main():\n"
                "    t = asyncio.create_task(worker())\n"
                "    await asyncio.sleep(0)\n"
                "    t.cancel()\n"
                "    try:\n"
                "        await t\n"
                "    except asyncio.CancelledError:\n"
                "        print('cancelled')\n\n"
                "asyncio.run(main())"
            ),
            "async_cleanup_on_cancel",
        )

    def p8(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict output for mixed async + blocking style with to_thread fanout.",
            (
                "import asyncio\n\n"
                "def blocking_io(x):\n"
                "    return x + 100\n\n"
                "async def main():\n"
                "    tasks = [asyncio.to_thread(blocking_io, i) for i in [1, 2, 3]]\n"
                "    print(await asyncio.gather(*tasks))\n\n"
                "asyncio.run(main())"
            ),
            "async_blocking_integration",
        )

    def p9(rng: random.Random, v: int) -> tuple[str, str, str]:
        base = rng.randint(2, 6)
        return (
            "Predict output for async design checklist scoring helper.",
            (
                "checks = {\n"
                "    'timeout': True,\n"
                "    'retry': True,\n"
                "    'cancellation': False,\n"
                "    'backpressure': True,\n"
                "}\n"
                f"weight = {base}\n"
                "score = sum(weight for ok in checks.values() if ok)\n"
                "print(score)\n"
                "print('pass' if score >= weight * 3 else 'fix')"
            ),
            "async_design_checklist",
        )

    def p10(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict output for TaskGroup ensuring child completion before exit.",
            (
                "import asyncio\n\n"
                "async def child(i):\n"
                "    await asyncio.sleep(0.01 * i)\n"
                "    return i\n\n"
                "async def main():\n"
                "    async with asyncio.TaskGroup() as tg:\n"
                "        t1 = tg.create_task(child(1))\n"
                "        t2 = tg.create_task(child(2))\n"
                "    print(t1.result() + t2.result())\n\n"
                "asyncio.run(main())"
            ),
            "async_taskgroup_lifecycle",
        )

    return [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]


def thread_l1_patterns() -> list[Callable[[random.Random, int], tuple[str, str, str]]]:
    def p1(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict output for start() vs run() thread behavior trap.",
            (
                "import threading\n\n"
                "def task():\n"
                "    print('from', threading.current_thread().name)\n\n"
                "t = threading.Thread(target=task, name='W1')\n"
                "t.run()\n"
                "t.start()\n"
                "t.join()"
            ),
            "thread_start_vs_run",
        )

    def p2(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict output for daemon flag configuration and join.",
            (
                "import threading\n\n"
                "def work():\n"
                "    print('work')\n\n"
                "t = threading.Thread(target=work, daemon=True)\n"
                "print(t.daemon)\n"
                "t.start()\n"
                "t.join()\n"
                "print('done')"
            ),
            "thread_daemon_basics",
        )

    def p3(rng: random.Random, v: int) -> tuple[str, str, str]:
        loops = rng.randint(2000, 4000)
        return (
            "Predict output for lock-protected shared counter update.",
            (
                "import threading\n\n"
                "counter = 0\n"
                "lock = threading.Lock()\n\n"
                "def inc(n):\n"
                "    global counter\n"
                "    for _ in range(n):\n"
                "        with lock:\n"
                "            counter += 1\n\n"
                f"n = {loops}\n"
                "t1 = threading.Thread(target=inc, args=(n,))\n"
                "t2 = threading.Thread(target=inc, args=(n,))\n"
                "t1.start(); t2.start()\n"
                "t1.join(); t2.join()\n"
                "print(counter)"
            ),
            "thread_lock_counter",
        )

    def p4(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict output for queue-based thread-safe communication.",
            (
                "import queue\n"
                "import threading\n\n"
                "q = queue.Queue()\n"
                "out = []\n\n"
                "def producer():\n"
                "    for i in [1, 2, 3]:\n"
                "        q.put(i)\n"
                "    q.put(None)\n\n"
                "def consumer():\n"
                "    while True:\n"
                "        x = q.get()\n"
                "        if x is None:\n"
                "            q.task_done()\n"
                "            break\n"
                "        out.append(x * 5)\n"
                "        q.task_done()\n\n"
                "tp = threading.Thread(target=producer)\n"
                "tc = threading.Thread(target=consumer)\n"
                "tp.start(); tc.start()\n"
                "tp.join(); q.join(); tc.join()\n"
                "print(out)"
            ),
            "thread_queue_sentinel",
        )

    def p5(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict output for Event synchronization pattern.",
            (
                "import threading\n\n"
                "evt = threading.Event()\n"
                "state = []\n\n"
                "def waiter():\n"
                "    evt.wait()\n"
                "    state.append('go')\n\n"
                "t = threading.Thread(target=waiter)\n"
                "t.start()\n"
                "state.append('ready')\n"
                "evt.set()\n"
                "t.join()\n"
                "print(state)"
            ),
            "thread_event_wait",
        )

    def p6(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict output for RLock re-entrant acquisition by same thread.",
            (
                "import threading\n\n"
                "lock = threading.RLock()\n"
                "value = 0\n\n"
                "def fn():\n"
                "    global value\n"
                "    with lock:\n"
                "        value += 1\n"
                "        with lock:\n"
                "            value += 2\n\n"
                "fn()\n"
                "print(value)"
            ),
            "thread_rlock",
        )

    def p7(rng: random.Random, v: int) -> tuple[str, str, str]:
        return (
            "Predict output for semaphore-bounded thread section accounting.",
            (
                "import threading\n\n"
                "sem = threading.Semaphore(2)\n"
                "active = 0\n"
                "max_active = 0\n"
                "mu = threading.Lock()\n\n"
                "def worker():\n"
                "    global active, max_active\n"
                "    with sem:\n"
                "        with mu:\n"
                "            active += 1\n"
                "            max_active = max(max_active, active)\n"
                "        with mu:\n"
                "            active -= 1\n\n"
                "threads = [threading.Thread(target=worker) for _ in range(5)]\n"
                "for t in threads: t.start()\n"
                "for t in threads: t.join()\n"
                "print(max_active)"
            ),
            "thread_semaphore_limit",
        )

    def p8(rng: random.Random, v: int) -> tuple[str, str, str]:
        workers = rng.randint(2, 4)
        return (
            "Predict output for basic ThreadPoolExecutor map behavior.",
            (
                "from concurrent.futures import ThreadPoolExecutor\n\n"
                "def sq(x):\n"
                "    return x * x\n\n"
                f"with ThreadPoolExecutor(max_workers={workers}) as pool:\n"
                "    print(list(pool.map(sq, [1, 2, 3, 4])))"
            ),
            "thread_pool_map",
        )

    return [p1, p2, p3, p4, p5, p6, p7, p8]


def thread_l2_patterns() -> list[Callable[[random.Random, int], tuple[str, str, str]]]:
    def p1(rng: random.Random, v: int) -> tuple[str, str, str]:
        workers = rng.randint(2, 4)
        return (
            "Predict output for submit + as_completed with deterministic post-processing.",
            (
                "from concurrent.futures import ThreadPoolExecutor, as_completed\n\n"
                "def job(x):\n"
                "    return x * 10\n\n"
                f"with ThreadPoolExecutor(max_workers={workers}) as pool:\n"
                "    futures = [pool.submit(job, i) for i in [3, 1, 2]]\n"
                "    out = [f.result() for f in as_completed(futures)]\n"
                "print(sorted(out))"
            ),
            "thread_pool_submit_as_completed",
        )

    def p2(rng: random.Random, v: int) -> tuple[str, str, str]:
        sleep_s = round(rng.uniform(0.03, 0.07), 2)
        timeout_s = round(max(0.01, sleep_s - 0.03), 2)
        ok_val = rng.randint(80, 130)
        return (
            "Predict output for Future timeout then successful result retrieval.",
            (
                "from concurrent.futures import ThreadPoolExecutor, TimeoutError\n"
                "import time\n\n"
                "def slow():\n"
                f"    time.sleep({sleep_s})\n"
                f"    return {ok_val}\n\n"
                "with ThreadPoolExecutor(max_workers=1) as pool:\n"
                "    f = pool.submit(slow)\n"
                "    try:\n"
                f"        print(f.result(timeout={timeout_s}))\n"
                "    except TimeoutError:\n"
                "        print('timeout')\n"
                "    print(f.result())"
            ),
            "thread_future_timeout",
        )

    def p3(rng: random.Random, v: int) -> tuple[str, str, str]:
        token = 100 + (v % 37)
        return (
            "Predict output for deadlock-avoidance lock-order helper.",
            (
                "import threading\n\n"
                "a = threading.Lock()\n"
                "b = threading.Lock()\n\n"
                "def with_two(l1, l2):\n"
                "    first, second = sorted((l1, l2), key=id)\n"
                "    with first:\n"
                "        with second:\n"
                "            return 'ok'\n\n"
                "print(with_two(a, b))\n"
                "print(with_two(b, a))\n"
                f"print({token})"
            ),
            "thread_deadlock_avoidance",
        )

    def p4(rng: random.Random, v: int) -> tuple[str, str, str]:
        a = rng.randint(8, 15)
        b = a + rng.randint(4, 10)
        return (
            "Predict output for graceful shutdown with queue sentinel.",
            (
                "import queue\n"
                "import threading\n\n"
                "q = queue.Queue()\n"
                "processed = []\n\n"
                "def worker():\n"
                "    while True:\n"
                "        item = q.get()\n"
                "        if item is None:\n"
                "            q.task_done()\n"
                "            break\n"
                "        processed.append(item + 1)\n"
                "        q.task_done()\n\n"
                "t = threading.Thread(target=worker)\n"
                "t.start()\n"
                f"for x in [{a}, {b}]:\n"
                "    q.put(x)\n"
                "q.put(None)\n"
                "q.join(); t.join()\n"
                "print(processed)"
            ),
            "thread_graceful_shutdown",
        )

    def p5(rng: random.Random, v: int) -> tuple[str, str, str]:
        marker = rng.randint(1, 9)
        return (
            "Predict output for condition-based handoff between producer and consumer.",
            (
                "import threading\n\n"
                "cond = threading.Condition()\n"
                "ready = False\n"
                "events = []\n\n"
                "def consumer():\n"
                "    global ready\n"
                "    with cond:\n"
                "        while not ready:\n"
                "            cond.wait()\n"
                "        events.append('consume')\n\n"
                "def producer():\n"
                "    global ready\n"
                "    with cond:\n"
                "        ready = True\n"
                "        events.append('produce')\n"
                "        cond.notify()\n\n"
                "tc = threading.Thread(target=consumer)\n"
                "tp = threading.Thread(target=producer)\n"
                "tc.start(); tp.start()\n"
                "tc.join(); tp.join()\n"
                "print(sorted(events))\n"
                f"print('m', {marker})"
            ),
            "thread_condition_handoff",
        )

    def p6(rng: random.Random, v: int) -> tuple[str, str, str]:
        s1 = rng.randint(2, 5)
        s2 = rng.randint(5, 9)
        s3 = rng.randint(1, 4)
        s4 = rng.randint(6, 10)
        return (
            "Predict output for lock granularity effect simulation.",
            (
                f"segments = [{s1}, {s2}, {s3}, {s4}]\n"
                "critical = [x for x in segments if x >= 5]\n"
                "print(sum(critical))\n"
                "print(len(critical))"
            ),
            "thread_lock_granularity",
        )

    def p7(rng: random.Random, v: int) -> tuple[str, str, str]:
        external_limit = rng.randint(6, 12)
        cpu = rng.randint(2, 8)
        return (
            "Predict output for thread pool sizing against external limit hint.",
            (
                f"external_limit = {external_limit}\n"
                f"cpu = {cpu}\n"
                "workers = min(external_limit, cpu * 2)\n"
                "print(workers)\n"
                "print('bounded')"
            ),
            "thread_pool_sizing",
        )

    def p8(rng: random.Random, v: int) -> tuple[str, str, str]:
        mul = rng.randint(2, 5)
        values = sorted(set(rand_int_list(rng, 3, 1, 4)))
        return (
            "Predict output for mixed async + ThreadPoolExecutor integration.",
            (
                "import asyncio\n"
                "from concurrent.futures import ThreadPoolExecutor\n\n"
                "def blocking(x):\n"
                f"    return x * {mul}\n\n"
                "async def main():\n"
                "    loop = asyncio.get_running_loop()\n"
                "    with ThreadPoolExecutor(max_workers=2) as pool:\n"
                f"        tasks = [loop.run_in_executor(pool, blocking, i) for i in {values}]\n"
                "        out = await asyncio.gather(*tasks)\n"
                "    print(out)\n\n"
                "asyncio.run(main())"
            ),
            "thread_async_integration",
        )

    def p9(rng: random.Random, v: int) -> tuple[str, str, str]:
        good_a = rng.randint(2, 6)
        good_b = rng.randint(7, 10)
        return (
            "Predict output for Future exception handling pattern.",
            (
                "from concurrent.futures import ThreadPoolExecutor\n\n"
                "def work(x):\n"
                "    if x == 0:\n"
                "        raise ValueError('bad')\n"
                "    return 10 // x\n\n"
                "with ThreadPoolExecutor(max_workers=2) as pool:\n"
                f"    futures = [pool.submit(work, x) for x in [{good_a}, 0, {good_b}]]\n"
                "    out = []\n"
                "    for f in futures:\n"
                "        try:\n"
                "            out.append(f.result())\n"
                "        except ValueError:\n"
                "            out.append('err')\n"
                "print(out)"
            ),
            "thread_future_error_pattern",
        )

    def p10(rng: random.Random, v: int) -> tuple[str, str, str]:
        io_pct = rng.randint(50, 90)
        cpu_pct = rng.randint(10, 60)
        blocking_sdk = "True" if (v % 2 == 0) else "False"
        return (
            "Predict output for interview-style model selection helper.",
            (
                f"workload = {{'io': {io_pct}, 'cpu': {cpu_pct}, 'blocking_sdk': {blocking_sdk}}}\n"
                "if workload['io'] > workload['cpu'] and not workload['blocking_sdk']:\n"
                "    pick = 'async'\n"
                "elif workload['io'] > workload['cpu']:\n"
                "    pick = 'threads-or-async+offload'\n"
                "else:\n"
                "    pick = 'sync-or-process'\n"
                "print(pick)"
            ),
            "thread_interview_decision",
        )

    return [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]


# -----------------------------
# MCQ banks (single-correct)
# -----------------------------
MCQ_BANK: dict[str, dict[str, list[tuple[str, tuple[str, str, str, str], str]]]] = {
    "sync": {
        "L1": [
            (
                "In sync code, what does a blocking call do?",
                ("A) Speeds up parallelism", "B) Pauses current thread progress", "C) Skips error handling", "D) Converts code to async"),
                "sync_blocking_call",
            ),
            (
                "What is the safest baseline for external HTTP call in sync code?",
                ("A) No timeout", "B) Very large retry count only", "C) Explicit timeout + exception handling", "D) `while True` retry"),
                "sync_timeout_best_practice",
            ),
            (
                "Which workload is usually a poor fit for pure sequential sync design?",
                ("A) Single local calculation", "B) Many concurrent remote calls", "C) One small script", "D) Deterministic pipeline"),
                "sync_workload_fit",
            ),
            (
                "If interviewer asks 'why slow?', strongest first check is:",
                ("A) Increase CPU blindly", "B) Look for blocking in critical path", "C) Remove all logs", "D) Convert everything to threads"),
                "sync_critical_path_check",
            ),
            (
                "CPU-bound task in default CPython generally benefits most from:",
                ("A) Blindly adding threads", "B) Better algorithms / native acceleration / multiprocessing", "C) Removing all exceptions", "D) Queue only"),
                "sync_cpu_bound_choice",
            ),
            (
                "Retries without timeout can cause:",
                ("A) Guaranteed success", "B) Infinite wait risk", "C) Lower latency always", "D) No side effects"),
                "sync_retry_timeout",
            ),
        ],
        "L2": [
            (
                "Best design for sync service calling flaky dependency:",
                ("A) No retry, no timeout", "B) Timeout + bounded retries + fallback", "C) Infinite retries", "D) Catch all and ignore"),
                "sync_flaky_dependency_strategy",
            ),
            (
                "Which metric best exposes tail-latency pain?",
                ("A) Only average latency", "B) p95/p99 latency", "C) Only success count", "D) CPU model name"),
                "sync_tail_latency",
            ),
            (
                "Strong interview answer for sync architecture includes:",
                ("A) Only happy path", "B) Timeout, retries, error categories, and cleanup", "C) Just class names", "D) No tradeoffs"),
                "sync_interview_completeness",
            ),
            (
                "For sync maintainability, prefer:",
                ("A) One giant function", "B) Small pure functions + clear boundaries", "C) Hidden globals everywhere", "D) Dynamic eval"),
                "sync_clean_code",
            ),
            (
                "If dependency is permanently failing, best retry posture is:",
                ("A) Aggressive unbounded retry", "B) Bounded retries and surface failure", "C) Silent ignore", "D) Block forever"),
                "sync_failure_escalation",
            ),
            (
                "In sync code, where should timeout be set?",
                ("A) Only at process start", "B) Per external dependency call", "C) Never", "D) Only in logging code"),
                "sync_timeout_scope",
            ),
        ],
    },
    "async": {
        "L1": [
            (
                "What does `await` do?",
                ("A) Creates a thread", "B) Blocks entire OS process", "C) Suspends coroutine and yields control to event loop", "D) Disables cancellation"),
                "async_await_rule",
            ),
            (
                "`asyncio.create_task(coro)` primarily:",
                ("A) Runs coro in new process", "B) Schedules coroutine concurrently", "C) Makes coroutine synchronous", "D) Deep copies state"),
                "async_create_task_mcq",
            ),
            (
                "Why is `time.sleep()` bad inside async coroutine?",
                ("A) Syntax error", "B) Blocks event loop thread", "C) Makes task faster", "D) Improves fairness"),
                "async_blocking_pitfall",
            ),
            (
                "`asyncio.gather` returns results in:",
                ("A) Completion order always", "B) Input order", "C) Random order", "D) Reverse order"),
                "async_gather_order_mcq",
            ),
            (
                "Timeout in asyncio fundamentals is usually done with:",
                ("A) `threading.Timer`", "B) `asyncio.wait_for`", "C) `os.alarm` only", "D) `time.sleep`"),
                "async_wait_for_mcq",
            ),
            (
                "Coroutine vs Task: task is:",
                ("A) Raw function object", "B) Scheduled wrapper managed by event loop", "C) Multiprocessing worker", "D) Lock primitive"),
                "async_coroutine_vs_task",
            ),
            (
                "When to use `asyncio.to_thread`?",
                ("A) For CPU SIMD kernels only", "B) To offload blocking sync call from event loop", "C) To replace await", "D) To disable retries"),
                "async_to_thread_mcq",
            ),
            (
                "Event loop is best described as:",
                ("A) Thread pool manager only", "B) Cooperative scheduler for awaitables", "C) Garbage collector", "D) Logging backend"),
                "async_event_loop",
            ),
        ],
        "L2": [
            (
                "Why is TaskGroup preferred over loose tasks in many cases?",
                ("A) Less typing only", "B) Structured lifecycle and safer error propagation", "C) It disables exceptions", "D) It uses OS threads"),
                "async_taskgroup_value",
            ),
            (
                "Cancellation in asyncio is observed at:",
                ("A) Import time", "B) Await points", "C) Function definition", "D) Random times only"),
                "async_cancel_points",
            ),
            (
                "Best way to cap concurrent async calls to remote API:",
                ("A) Unlimited tasks", "B) `asyncio.Semaphore`", "C) Global mutable counter without lock", "D) Busy waiting loop"),
                "async_semaphore_mcq",
            ),
            (
                "What is backpressure-friendly async pattern?",
                ("A) Unbounded queue always", "B) Bounded queue + workers", "C) Infinite recursion", "D) Spin locks"),
                "async_backpressure_pattern",
            ),
            (
                "`asyncio.shield` is used when:",
                ("A) You want outer cancellation to skip inner critical op cancellation", "B) You want to cancel everything quickly", "C) You disable timeout", "D) You need multiprocessing"),
                "async_shield_mcq",
            ),
            (
                "Ignoring cancellation handling often causes:",
                ("A) Better throughput", "B) Resource leaks / messy shutdown", "C) Stronger typing", "D) Reduced memory"),
                "async_cancel_risk",
            ),
            (
                "Common async code-review red flag:",
                ("A) Explicit timeout per dependency", "B) Blocking I/O inside coroutine", "C) Task supervision", "D) Graceful shutdown"),
                "async_review_redflag",
            ),
            (
                "For mixed async + blocking SDK, practical approach is:",
                ("A) Call blocking SDK directly in coroutine", "B) Offload to thread executor/to_thread", "C) Disable event loop", "D) Remove error handling"),
                "async_mixed_code_strategy",
            ),
            (
                "In interview, strongest async answer includes:",
                ("A) Only syntax", "B) Timeout + retries + cancellation + backpressure", "C) Just `await` keyword", "D) No tradeoffs"),
                "async_interview_depth",
            ),
            (
                "If task is destroyed while pending, likely issue is:",
                ("A) Too many dataclasses", "B) Task lifecycle not tracked/awaited during shutdown", "C) Typo in import", "D) Invalid f-string"),
                "async_pending_task_issue",
            ),
            (
                "Where should timeout policy live in async systems?",
                ("A) Global only", "B) At each external dependency boundary", "C) Never", "D) In test files only"),
                "async_timeout_boundary",
            ),
            (
                "Un-awaited coroutine warning usually means:",
                ("A) Coroutine was created but never awaited/scheduled", "B) Loop is too fast", "C) GIL is disabled", "D) Lock not recursive"),
                "async_unawaited_warning",
            ),
        ],
    },
    "multithreaded": {
        "L1": [
            (
                "In default CPython build, GIL means:",
                ("A) No threads allowed", "B) One thread executes Python bytecode at a time", "C) True parallel bytecode always", "D) No race conditions"),
                "thread_gil_default",
            ),
            (
                "Threads are still very useful in Python for:",
                ("A) I/O-bound concurrency", "B) Only sorting lists", "C) Replacing async always", "D) Eliminating locks"),
                "thread_io_fit",
            ),
            (
                "Race condition is:",
                ("A) Faster loop", "B) Outcome depends on timing/interleaving of shared state access", "C) Syntax warning", "D) Dead code"),
                "thread_race_condition",
            ),
            (
                "Primary primitive to guard critical section:",
                ("A) `Queue`", "B) `Lock`", "C) `Timer`", "D) `enumerate`"),
                "thread_lock_mcq",
            ),
            (
                "Thread-safe producer-consumer communication is commonly done with:",
                ("A) Global list without lock", "B) `queue.Queue`", "C) `set`", "D) `sorted`"),
                "thread_queue_mcq",
            ),
            (
                "`start()` vs `run()` on thread:",
                ("A) Same behavior always", "B) `start()` creates new thread; `run()` executes in current thread", "C) `run()` is async", "D) `start()` returns result"),
                "thread_start_run_mcq",
            ),
            (
                "Daemon thread means:",
                ("A) Higher priority", "B) It won't keep process alive on exit", "C) It is unkillable", "D) It has no shared memory"),
                "thread_daemon_mcq",
            ),
            (
                "`RLock` compared to `Lock`:",
                ("A) Slower sorting", "B) Allows same thread to acquire recursively", "C) Works only in async", "D) Prevents all deadlocks automatically"),
                "thread_rlock_mcq",
            ),
        ],
        "L2": [
            (
                "Best reason to use ThreadPoolExecutor over manual thread creation:",
                ("A) Always faster than async", "B) Easier task submission, pooling, futures, lifecycle management", "C) Removes need for locks", "D) Converts CPU to GPU"),
                "thread_pool_reason",
            ),
            (
                "Future represents:",
                ("A) Finished result only", "B) Handle for result/error/timeout of asynchronous execution", "C) Lock state", "D) Event loop"),
                "thread_future_mcq",
            ),
            (
                "Deadlock prevention basic rule:",
                ("A) Nested locks random order", "B) Consistent lock acquisition order", "C) Disable join", "D) Use daemon threads only"),
                "thread_deadlock_prevent",
            ),
            (
                "Cancellation on Future usually succeeds when:",
                ("A) Task already running long", "B) Task has not started yet", "C) Task completed", "D) Executor is shutdown"),
                "thread_future_cancel",
            ),
            (
                "Graceful shutdown of worker threads should include:",
                ("A) Kill process abruptly", "B) Stop intake, signal workers, drain queue, join", "C) Ignore pending tasks", "D) Remove timeouts"),
                "thread_graceful_shutdown_mcq",
            ),
            (
                "Event primitive is best for:",
                ("A) Protecting arithmetic", "B) One-to-many readiness signaling", "C) Hash lookups", "D) GC tuning"),
                "thread_event_mcq",
            ),
            (
                "Condition primitive is useful for:",
                ("A) Waiting on state transition under lock", "B) Replacing queue always", "C) CPU vectorization", "D) File compression"),
                "thread_condition_mcq",
            ),
            (
                "Semaphore in threading typically controls:",
                ("A) Function recursion depth", "B) Number of concurrent accesses to bounded resource", "C) Task priority queue", "D) Dict ordering"),
                "thread_semaphore_mcq",
            ),
            (
                "On free-threaded CPython builds, interview-safe statement is:",
                ("A) Locks are less important", "B) Thread-safety discipline becomes more important", "C) GIL semantics are identical", "D) Threads are obsolete"),
                "thread_free_threaded_implication",
            ),
            (
                "Strong performance tuning for thread pool starts with:",
                ("A) Max workers = 1000 always", "B) Profile workload and respect external limits", "C) Remove error handling", "D) Disable joins"),
                "thread_pool_tuning",
            ),
            (
                "For FastAPI async handlers with blocking DB driver, practical move is:",
                ("A) Keep blocking directly on loop", "B) Use async driver or offload blocking calls to thread pool", "C) Disable await", "D) Use only daemon threads"),
                "thread_mixed_fastapi",
            ),
            (
                "Why avoid sharing too much mutable state across threads?",
                ("A) More memory savings", "B) Higher race/deadlock coupling and debugging cost", "C) Better determinism", "D) Better cache always"),
                "thread_mutable_state_risk",
            ),
        ],
    },
}


def get_output_patterns(topic: str, level: str) -> list[Callable[[random.Random, int], tuple[str, str, str]]]:
    mapping = {
        ("sync", "L1"): sync_l1_patterns(),
        ("sync", "L2"): sync_l2_patterns(),
        ("async", "L1"): async_l1_patterns(),
        ("async", "L2"): async_l2_patterns(),
        ("multithreaded", "L1"): thread_l1_patterns(),
        ("multithreaded", "L2"): thread_l2_patterns(),
    }
    return mapping[(topic, level)]


def generate_output_questions(
    topic: str,
    level: str,
    count: int,
    rng: random.Random,
    signatures: set[str],
) -> list[Question]:
    patterns = get_output_patterns(topic, level)
    generated: list[Question] = []
    attempts = 0
    variant = 0
    max_attempts = max(250, count * 80)

    while len(generated) < count and attempts < max_attempts:
        attempts += 1
        pattern = rng.choice(patterns)
        prompt, code, concept = pattern(rng, variant)
        variant += 1
        q = Question(topic=topic, level=level, qtype="output", prompt=prompt, code=code, concept=concept)
        sig = question_signature(q)
        if sig in signatures:
            continue
        signatures.add(sig)
        generated.append(q)

    if len(generated) != count:
        raise RuntimeError(f"Could not generate output questions for {topic}/{level}: {len(generated)}/{count}")
    return generated


def generate_mcq_questions(
    topic: str,
    level: str,
    count: int,
    rng: random.Random,
    signatures: set[str],
) -> list[Question]:
    pool = MCQ_BANK[topic][level][:]
    rng.shuffle(pool)
    generated: list[Question] = []

    for prompt, options, concept in pool:
        mcq_prompt = prompt
        if "select all" not in prompt.lower():
            mcq_prompt = f"{prompt} (Select all that apply.)"
        q = Question(topic=topic, level=level, qtype="mcq", prompt=mcq_prompt, options=options, concept=concept)
        sig = question_signature(q)
        if sig in signatures:
            continue
        signatures.add(sig)
        generated.append(q)
        if len(generated) == count:
            break

    if len(generated) != count:
        raise RuntimeError(f"Could not generate MCQ questions for {topic}/{level}: {len(generated)}/{count}")
    return generated


def build_question_set(distribution: dict, rng: random.Random) -> list[Question]:
    signatures: set[str] = set()
    questions: list[Question] = []
    for topic in TOPICS:
        for level in LEVELS:
            out_count = distribution[topic][level]["output"]
            mcq_count = distribution[topic][level]["mcq"]
            questions.extend(generate_output_questions(topic, level, out_count, rng, signatures))
            questions.extend(generate_mcq_questions(topic, level, mcq_count, rng, signatures))
    return questions


def verify_totals(questions: list[Question], distribution: dict) -> dict[str, int]:
    topic_totals = {t: 0 for t in TOPICS}
    level_totals = {l: 0 for l in LEVELS}
    type_totals = {t: 0 for t in QTYPES}

    for q in questions:
        topic_totals[q.topic] += 1
        level_totals[q.level] += 1
        type_totals[q.qtype] += 1

    for topic in TOPICS:
        expected = sum(distribution[topic][level][qtype] for level in LEVELS for qtype in QTYPES)
        if topic_totals[topic] != expected:
            raise AssertionError(f"Topic count mismatch for {topic}: {topic_totals[topic]} vs {expected}")

    expected_l1 = sum(distribution[t]["L1"][qt] for t in TOPICS for qt in QTYPES)
    expected_l2 = sum(distribution[t]["L2"][qt] for t in TOPICS for qt in QTYPES)
    if level_totals["L1"] != expected_l1 or level_totals["L2"] != expected_l2:
        raise AssertionError("Level total mismatch.")

    expected_output = sum(distribution[t][l]["output"] for t in TOPICS for l in LEVELS)
    expected_mcq = sum(distribution[t][l]["mcq"] for t in TOPICS for l in LEVELS)
    if type_totals["output"] != expected_output or type_totals["mcq"] != expected_mcq:
        raise AssertionError("Question-type total mismatch.")

    return {
        "total": len(questions),
        "l1": level_totals["L1"],
        "l2": level_totals["L2"],
        "output": type_totals["output"],
        "mcq": type_totals["mcq"],
        "sync": topic_totals["sync"],
        "async": topic_totals["async"],
        "multithreaded": topic_totals["multithreaded"],
    }


def split_for_render(questions: list[Question], seed: int) -> dict[str, dict[str, list[Question]]]:
    rng = random.Random(seed + 777)
    bucket = {"L1": {"output": [], "mcq": []}, "L2": {"output": [], "mcq": []}}
    for q in questions:
        bucket[q.level][q.qtype].append(q)
    for level in LEVELS:
        rng.shuffle(bucket[level]["output"])
        rng.shuffle(bucket[level]["mcq"])
    return bucket


def line_count_for_output(_level: str, _code: str) -> int:
    return 2


def compact_code(code: str) -> str:
    lines = [ln.rstrip() for ln in code.splitlines() if ln.strip()]
    return "\n".join(lines)


def render_pdf(output_path: Path, rendered: dict[str, dict[str, list[Question]]], summary: dict[str, int]) -> None:
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=19,
        alignment=1,
        spaceAfter=4,
    )
    h1_style = ParagraphStyle(
        "H1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=12.5,
        leading=14.5,
        spaceBefore=5,
        spaceAfter=2,
    )
    h2_style = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=12.4,
        spaceBefore=4,
        spaceAfter=2,
    )
    q_style = ParagraphStyle(
        "Q",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=11.4,
        leading=13.8,
        spaceAfter=1.2,
    )
    code_style = ParagraphStyle(
        "CodeStyle",
        fontName="Courier-Bold",
        fontSize=10.4,
        leading=12.5,
        leftIndent=0,
        rightIndent=0,
        spaceBefore=0,
        spaceAfter=0,
        textColor=colors.HexColor("#111111"),
    )
    opt_style = ParagraphStyle(
        "Opt",
        parent=q_style,
        leftIndent=10,
        spaceAfter=0.9,
    )
    meta_style = ParagraphStyle(
        "Meta",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.8,
        leading=10.5,
        textColor=colors.HexColor("#303030"),
        spaceAfter=1,
    )

    def footer(canvas_obj, doc_obj) -> None:
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.setFillColor(colors.HexColor("#5a5a5a"))
        canvas_obj.drawRightString(A4[0] - 12 * mm, 8.5 * mm, f"Page {doc_obj.page}")

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=10 * mm,
        rightMargin=10 * mm,
        topMargin=10 * mm,
        bottomMargin=10 * mm,
        title="Python Week 5 Test",
        author="Auto Generator",
    )

    story = []
    story.append(Paragraph("PYTHON WEEK 5 TEST", title_style))
    story.append(Paragraph("Sync vs Async vs Multithreading (Interview Focus)", h2_style))
    story.append(
        Paragraph(
            (
                "Instructions: (1) Solve all questions. (2) For output questions, write exact output. "
                "(3) For MCQ, multiple options may be correct; select all correct options. "
                f"(4) Total: {summary['total']} | Sync: {summary['sync']} | Async: {summary['async']} | "
                f"Multithreaded: {summary['multithreaded']} | "
                f"Output: {summary['output']} | MCQ: {summary['mcq']}."
            ),
            meta_style,
        )
    )
    story.append(Spacer(1, 2))

    all_outputs = rendered["L1"]["output"] + rendered["L2"]["output"]
    all_mcqs = rendered["L1"]["mcq"] + rendered["L2"]["mcq"]

    q_number = 1
    story.append(Paragraph("Part A: Predict the Output", h1_style))
    for q in all_outputs:
        q_block = [Paragraph(f"Q{q_number}. {q.prompt}", q_style)]
        code_block = Preformatted(q.code or "", code_style)
        code_table = Table([[code_block]], colWidths=["100%"])
        code_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f6f8fa")),
                    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#7a7a7a")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        q_block.append(code_table)
        q_block.append(Spacer(1, 1))
        q_block.append(Paragraph("Answer:", meta_style))
        q_block.append(AnswerLines(line_count_for_output(q.level, q.code or "")))
        q_block.append(Spacer(1, 3))
        story.append(KeepTogether(q_block))
        q_number += 1

    story.append(Paragraph("Part B: MCQ (Multiple Correct; Select All That Apply)", h1_style))
    for q in all_mcqs:
        q_block = [Paragraph(f"Q{q_number}. {q.prompt}", q_style)]
        if q.options:
            for opt in q.options:
                q_block.append(Paragraph(opt, opt_style))
        q_block.append(Spacer(1, 2))
        story.append(KeepTogether(q_block))
        q_number += 1

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Week 5 Python concurrency test PDF.")
    parser.add_argument(
        "--output",
        default=str(Path("python/assignment/test/python-week-5-test.pdf")),
        help="Output PDF path.",
    )
    parser.add_argument("--seed", type=int, default=20260614, help="Random seed for reproducibility.")
    args = parser.parse_args()

    distribution = DEFAULT_DISTRIBUTION
    validate_distribution(distribution)

    rng = random.Random(args.seed)
    questions = build_question_set(distribution=distribution, rng=rng)
    summary = verify_totals(questions, distribution)
    rendered = split_for_render(questions, seed=args.seed)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    render_pdf(output_path=output_path, rendered=rendered, summary=summary)

    print("Generated:", output_path)
    print(
        "Summary:",
        f"total={summary['total']}, sync={summary['sync']}, async={summary['async']}, "
        f"multithreaded={summary['multithreaded']}, L1={summary['l1']}, L2={summary['l2']}, "
        f"output={summary['output']}, mcq={summary['mcq']}",
    )


if __name__ == "__main__":
    main()
