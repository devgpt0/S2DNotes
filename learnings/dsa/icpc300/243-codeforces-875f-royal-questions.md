# ICPC300 243: Codeforces 875F - Royal Questions

**Source:** [Codeforces 875F](https://codeforces.com/problemset/problem/875/F)  
**Difficulty:** 2400  
**Pattern:** maximum-weight pseudoforest matroid greedy

## Exact contract

Each question has a reward and can be assigned to either of two people. Every
person may answer at most one selected question. Choose questions and
assignments maximizing total reward.

## First principles

View people as vertices and questions as weighted edges. A selected component
can orient every edge toward its assigned answerer with indegree at most one
exactly when it has at most as many edges as vertices: each component is a tree
or has one cycle.

Such pseudoforests form a matroid, so process rewards from largest to smallest
and keep an edge whenever it does not create a second cycle in a component.

## Cases that decide correctness

- A self-loop consumes its vertex and creates the component's one cycle.
- Joining two already cyclic components is forbidden.
- Adding an internal edge is allowed only to an acyclic component.
- Parallel questions are independent edges.
- Rewards are accumulated only for accepted questions.

## Brute force: enumerate question subsets

```python
def royal_questions_brute(
    person_count: int, questions: list[tuple[int, int, int]]
) -> int:
    answer = 0
    for subset in range(1 << len(questions)):
        parent = list(range(person_count))
        vertices = [1] * person_count
        edge_count = [0] * person_count

        def find(vertex: int) -> int:
            while vertex != parent[vertex]:
                vertex = parent[vertex]
            return vertex

        reward = 0
        valid = True
        for index, (first, second, value) in enumerate(questions):
            if not (subset >> index & 1):
                continue
            reward += value
            first_root = find(first)
            second_root = find(second)
            if first_root != second_root:
                parent[second_root] = first_root
                vertices[first_root] += vertices[second_root]
                edge_count[first_root] += edge_count[second_root]
            root = find(first)
            edge_count[root] += 1
            if edge_count[root] > vertices[root]:
                valid = False
                break
        if valid:
            answer = max(answer, reward)
    return answer
```

This is exponential in the number of questions.

## Better insight: feasibility is one cycle bit per component

The complete assignment details are unnecessary during selection. A DSU only
needs to know whether each component already contains its single allowed cycle.

## Expert solution: descending-weight DSU greedy

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    person_count, question_count = map(int, input_stream.readline().split())
    questions = sorted(
        (
            (reward, first - 1, second - 1)
            for first, second, reward in (
                map(int, input_stream.readline().split()) for _ in range(question_count)
            )
        ),
        reverse=True,
    )
    parent = list(range(person_count))
    size = [1] * person_count
    cyclic = [False] * person_count

    def find(vertex: int) -> int:
        while vertex != parent[vertex]:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    answer = 0
    for reward, first, second in questions:
        first_root = find(first)
        second_root = find(second)
        if first_root == second_root:
            if cyclic[first_root]:
                continue
            cyclic[first_root] = True
            answer += reward
            continue
        if cyclic[first_root] and cyclic[second_root]:
            continue
        if size[first_root] < size[second_root]:
            first_root, second_root = second_root, first_root
        parent[second_root] = first_root
        size[first_root] += size[second_root]
        cyclic[first_root] = cyclic[first_root] or cyclic[second_root]
        answer += reward
    print(answer)


if __name__ == "__main__":
    solve()
```

The greedy keeps exactly the maximum-weight independent set of the pseudoforest
matroid, and every kept component admits an answerer assignment.

**Complexity:** `O(m log m + m alpha(n))` time and `O(n+m)` space.
