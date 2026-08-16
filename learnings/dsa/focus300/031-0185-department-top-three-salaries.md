# Focus300 031: LeetCode 185 - Department Top Three Salaries

**Source:** [LeetCode 185 - Department Top Three Salaries](https://leetcode.com/problems/department-top-three-salaries/)  
**Difficulty:** Hard  
**Pattern:** group-wise top distinct values  

## Exact contract

`Employee(id, name, salary, department_id)` and `Department(id, name)` are
relational rows. Return every employee whose salary is one of the three highest
**distinct** salaries in that employee's department. This Python model returns
`(department_name, employee_name, salary)` rows in deterministic department,
descending-salary, employee-name order.

## First principles

The rank is over distinct salary values, not employees. An employee qualifies
exactly when fewer than three different salaries in the same department are
strictly greater.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Read the table rows and keep only the rows that can still contribute to the answer.
2. Use joins, grouping, ranking, or filtering to turn the raw rows into one intermediate result set.
3. Apply tie rules or ordering rules before selecting the final row or value.
4. Project the requested column(s), which is the final output of the query.

In SQL problems, the database performs the transformation by moving rows through `WHERE`, `JOIN`, `GROUP BY`, window functions, and `ORDER BY` until only the requested result remains.


## Diagram: SQL rows to final answer

```text

            raw table rows
                |
                v
            filter / join / group / rank
                |
                v
            ordered result rows
                |
                v
            requested output column
```

The query turns table rows into one final answer by filtering, combining, and ranking the data in SQL.

## Cases that decide correctness

- Tied employees at the third distinct salary all qualify.
- A department with fewer than three salary levels returns every employee.
- Repeated department names are allowed; department IDs define the groups.
- Employee IDs and department IDs must be valid and unique where required.
- The source foreign-key contract requires every employee department to exist.

## Brute force: count higher distinct salaries per employee

```python
Employee = tuple[int, str, int, int]
Department = tuple[int, str]
SalaryRow = tuple[str, str, int]


def department_top_three_brute(
    employees: list[Employee], departments: list[Department]
) -> list[SalaryRow]:
    department_names: dict[int, str] = {}
    for department_id, name in departments:
        if (
            type(department_id) is not int
            or not isinstance(name, str)
            or not name
            or department_id in department_names
        ):
            raise ValueError("invalid or duplicate department")
        department_names[department_id] = name

    employee_ids: set[int] = set()
    for employee_id, name, salary, department_id in employees:
        if (
            type(employee_id) is not int
            or employee_id in employee_ids
            or not isinstance(name, str)
            or not name
            or type(salary) is not int
            or department_id not in department_names
        ):
            raise ValueError("invalid employee")
        employee_ids.add(employee_id)

    result = []
    for _, employee_name, salary, department_id in employees:
        higher = {
            other_salary
            for _, _, other_salary, other_department in employees
            if other_department == department_id and other_salary > salary
        }
        if len(higher) < 3:
            result.append((department_names[department_id], employee_name, salary))
    result.sort(key=lambda row: (row[0], -row[2], row[1]))
    return result
```

**Complexity:** `O(e^2)` time and `O(e + d)` space.

## Better approach: sort every department's employees

Sorting employees by department and descending salary allows a scan that
increments rank only when salary changes. It costs `O(e log e)` time.

## Expert solution: group once and select three salary levels

```python
Employee = tuple[int, str, int, int]
Department = tuple[int, str]
SalaryRow = tuple[str, str, int]


def department_top_three(
    employees: list[Employee], departments: list[Department]
) -> list[SalaryRow]:
    department_names: dict[int, str] = {}
    for department_id, name in departments:
        if (
            type(department_id) is not int
            or not isinstance(name, str)
            or not name
            or department_id in department_names
        ):
            raise ValueError("invalid or duplicate department")
        department_names[department_id] = name

    employee_ids: set[int] = set()
    grouped: dict[int, list[tuple[str, int]]] = {
        department_id: [] for department_id in department_names
    }
    for employee_id, name, salary, department_id in employees:
        if (
            type(employee_id) is not int
            or employee_id in employee_ids
            or not isinstance(name, str)
            or not name
            or type(salary) is not int
            or department_id not in department_names
        ):
            raise ValueError("invalid employee")
        employee_ids.add(employee_id)
        grouped[department_id].append((name, salary))

    result = []
    for department_id, people in grouped.items():
        top_salaries = set(sorted({salary for _, salary in people}, reverse=True)[:3])
        result.extend(
            (department_names[department_id], name, salary)
            for name, salary in people
            if salary in top_salaries
        )
    result.sort(key=lambda row: (row[0], -row[2], row[1]))
    return result
```

Grouping preserves the department boundary, and selecting three values from a
set implements dense rank `<= 3` exactly. Every tied employee is filtered by
the same selected salary set.

**Complexity:** `O(e log e + d)` time and `O(e + d)` space.

