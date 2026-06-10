# Python Sync, Async, and Multithreading: Learning Path and Setup

## 1. Why This Notes Set Exists

This folder is designed for two goals:
- teach from zero
- prepare for Python interview questions on concurrency

You should be able to go from basics to production-level reasoning by following files in order.

---

## 2. Recommended Learning Order

1. `Synchronous Programming in Python.md`
2. `Async Programming in Python - asyncio Fundamentals.md`
3. `Async Programming in Python - Advanced and Structured Concurrency.md`
4. `Multithreading in Python - Fundamentals.md`
5. `Multithreading in Python - Advanced and ThreadPoolExecutor.md`
6. `Sync vs Async vs Multithreading - Interview Decision Guide.md`
7. `Python Concurrency Interview Questions and Answers.md`

---

## 3. Environment Setup

Use Python 3.11+ (recommended 3.12+).

Check version:
```bash
python --version
```

Create virtual environment:
```bash
python -m venv .venv
```

Activate (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

---

## 4. How to Run Examples

Save each example in a separate `.py` file and run:
```bash
python filename.py
```

For async examples, always run from top-level:
```python
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

---

## 5. Interview Preparation Strategy

For each file:
1. read concept
2. run snippet
3. modify snippet
4. explain in your own words
5. answer "why this approach?"

If you can explain tradeoffs, you are interview-ready.

---

## 6. Core Mental Model

Concurrency in Python is not one thing:
- synchronous: one task at a time
- async: one thread, many waiting tasks, cooperative switching
- multithreading: many OS threads, context switching by scheduler
- multiprocessing: many processes (true CPU parallelism in CPython)
- free-threaded CPython (3.13+ build option): threads can run Python code in parallel

Most interview confusion comes from mixing these models.

---

## 7. Final Tip

Do not memorize APIs only.  
Understand:
- when work blocks
- where context switch happens
- what can race
- how failure/cancellation propagates

That is what interviewers test.
