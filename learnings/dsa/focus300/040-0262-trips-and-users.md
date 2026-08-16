# Focus300 040: LeetCode 262 - Trips and Users

**Source:** [LeetCode 262 - Trips and Users](https://leetcode.com/problems/trips-and-users/)  
**Difficulty:** Hard  
**Pattern:** relational filtering followed by grouped conditional aggregation  

## Exact contract

`Trips(id, client_id, driver_id, city_id, status, request_at)` references
`Users(users_id, banned, role)`. For each date from `2013-10-01` through
`2013-10-03` having at least one eligible trip, compute cancelled eligible
trips divided by eligible trips. Both client and driver must be unbanned.
Round to two decimals using SQL-style half-up rounding.

## First principles

Filtering belongs before aggregation: a trip with either banned participant is
absent from both numerator and denominator. After the two user joins, group by
date and count every status other than `completed` as cancelled under the
source status domain.


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

- Both the client and driver ban flags matter.
- Dates outside the three-day interval are ignored.
- A date with no eligible trips produces no row.
- Client- and driver-cancelled statuses both enter the numerator.
- Decimal half-up rounding differs from binary floating-point `round`.

## Brute force: repeated linear user joins per date

```python
from decimal import Decimal, ROUND_HALF_UP


User = tuple[int, str, str]
Trip = tuple[int, int, int, int, str, str]


def trip_cancellation_rates_brute(
    trips: list[Trip], users: list[User]
) -> list[tuple[str, Decimal]]:
    valid_roles = {"client", "driver", "partner"}
    user_ids: set[int] = set()
    for user_id, banned, role in users:
        if (
            type(user_id) is not int
            or user_id in user_ids
            or banned not in {"Yes", "No"}
            or role not in valid_roles
        ):
            raise ValueError("invalid user")
        user_ids.add(user_id)
    valid_statuses = {
        "completed",
        "cancelled_by_driver",
        "cancelled_by_client",
    }
    trip_ids: set[int] = set()
    for trip_id, client_id, driver_id, city_id, status, request_at in trips:
        if (
            type(trip_id) is not int
            or trip_id in trip_ids
            or type(client_id) is not int
            or type(driver_id) is not int
            or type(city_id) is not int
            or client_id not in user_ids
            or driver_id not in user_ids
            or status not in valid_statuses
            or not isinstance(request_at, str)
        ):
            raise ValueError("invalid trip")
        trip_ids.add(trip_id)

    result = []
    for date in ("2013-10-01", "2013-10-02", "2013-10-03"):
        eligible = []
        for trip in trips:
            _, client_id, driver_id, _, status, request_at = trip
            if request_at != date:
                continue
            client = next(user for user in users if user[0] == client_id)
            driver = next(user for user in users if user[0] == driver_id)
            if client[1] == "No" and driver[1] == "No":
                eligible.append(status)
        if eligible:
            cancelled = sum(status != "completed" for status in eligible)
            rate = (Decimal(cancelled) / Decimal(len(eligible))).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            result.append((date, rate))
    return result
```

**Complexity:** `O(3 * trips * users)` time and `O(trips + users)` validation
space.

## Better approach: two user hash joins, then group rows

Materialize eligible rows after `O(1)` user lookups and group their statuses by
date. The expert solution combines grouping and conditional counts in one pass.

## Expert solution: indexed joins and conditional aggregation

```python
from decimal import Decimal, ROUND_HALF_UP


User = tuple[int, str, str]
Trip = tuple[int, int, int, int, str, str]


def trip_cancellation_rates(
    trips: list[Trip], users: list[User]
) -> list[tuple[str, Decimal]]:
    valid_roles = {"client", "driver", "partner"}
    unbanned: dict[int, bool] = {}
    for user_id, banned, role in users:
        if (
            type(user_id) is not int
            or user_id in unbanned
            or banned not in {"Yes", "No"}
            or role not in valid_roles
        ):
            raise ValueError("invalid user")
        unbanned[user_id] = banned == "No"

    target_dates = {"2013-10-01", "2013-10-02", "2013-10-03"}
    valid_statuses = {
        "completed",
        "cancelled_by_driver",
        "cancelled_by_client",
    }
    counts: dict[str, list[int]] = {}
    trip_ids: set[int] = set()
    for trip_id, client_id, driver_id, city_id, status, request_at in trips:
        if (
            type(trip_id) is not int
            or trip_id in trip_ids
            or type(client_id) is not int
            or type(driver_id) is not int
            or type(city_id) is not int
            or client_id not in unbanned
            or driver_id not in unbanned
            or status not in valid_statuses
            or not isinstance(request_at, str)
        ):
            raise ValueError("invalid trip")
        trip_ids.add(trip_id)
        if request_at in target_dates and unbanned[client_id] and unbanned[driver_id]:
            date_counts = counts.setdefault(request_at, [0, 0])
            date_counts[0] += 1
            date_counts[1] += status != "completed"

    result = []
    for date in sorted(counts):
        total, cancelled = counts[date]
        rate = (Decimal(cancelled) / Decimal(total)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        result.append((date, rate))
    return result
```

The indexed user table reproduces both joins. Only rows satisfying both ban
predicates enter the grouped total and conditional cancelled count, matching
the SQL query order exactly.

**Complexity:** `O(trips + users)` expected time and `O(trips + users)` space.

