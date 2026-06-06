# Worksheet 1 Answer Key: Clean Code Foundations + Why OOP Exists

## Section A: MCQ (1-50)

1. C  
2. C  
3. D  
4. B  
5. C  
6. B  
7. C  
8. C  
9. C  
10. B  
11. B  
12. B  
13. B  
14. B  
15. C  
16. B  
17. B  
18. C  
19. B  
20. B  
21. B  
22. B  
23. C  
24. B  
25. B  
26. B  
27. B  
28. C  
29. C  
30. A  
31. C  
32. B  
33. C  
34. A  
35. C  
36. B  
37. D  
38. C  
39. B  
40. B  
41. B  
42. A  
43. B  
44. A  
45. B  
46. B  
47. B  
48. B  
49. B  
50. A

---

## Section B: Predict the Output (51-80)

51. `18.0`  
52. `5`  
53. `Asha`  
54. `ABC ABC`  
55. `85.0`  
56. `B`  
57.
```text
[1]
[1, 1]
```
58. `['pen'] []`  
59. `99 10`  
60. `[5]`  
61. `150`  
62. `False True`  
63. `Ravi`  
64. `2`  
65.
```text
20
10
```
66. `15`  
67. `A-INACTIVE`  
68. `[80, 90]`  
69. `ok`  
70. `Demo`  
71. `0`  
72. `True False`  
73. `student admin student`  
74. `2.5`  
75. `8`  
76. `[1] []`  
77. `5.0 None`  
78. `2`  
79. `True`  
80. `{'name': 'Jay'}`

---

## Section C: Refactor the Code (81-100) - Model Answers

81. Use clear names + constant:
```python
GST_RATE = 0.18

def calculate_tax(amount: float, quantity: int) -> float:
    return amount * quantity * GST_RATE
```

82. Split responsibilities: `validate_student`, `calculate_grade`, `save_student`, `send_grade_email`.

83. Extract one reusable function:
```python
def calculate_average(marks): return sum(marks) / len(marks)
```

84. Rename class/fields meaningfully, add types:
`class Student(name, marks)`.

85. Replace magic numbers with constants:
`GRADE_A_THRESHOLD`, `GRADE_B_THRESHOLD`.

86. Use guard clauses for account null, amount <= 0, insufficient balance.

87. Remove hidden global mutation:
`def add_price(current_total, price): return current_total + price`.

88. Fix mutable default:
```python
def __init__(self, items=None):
    self.items = [] if items is None else items
```

89. Replace unnecessary class with function:
`def add_numbers(a, b): return a + b`.

90. Rename `f1` to intention-revealing method:
`calculate_annual_salary`.

91. Split orchestration into small functions:
`validate_order`, `reserve_inventory`, `create_invoice`, `charge_payment`, `send_confirmation`.

92. Prefer self-documenting code; keep comments only for non-obvious business rules.

93. Replace dictionary + short keys with class:
`Student(name, marks).calculate_average()`.

94. Add constructor validation:
balance cannot be negative.

95. Separate validation, persistence, notification, and presentation concerns.

96. Use constant:
`MIN_ATTENDANCE_PERCENTAGE = 75`.

97. Separate domain logic from file I/O and output printing.

98. Provide high-level API:
`car.start()` that calls private internal steps.

99. Catch specific exceptions, log context, re-raise when required.

100. Move `marks` to instance attribute in `__init__`, not class-level mutable list.

---

## Project Exercises - Evaluation Checklist

- meaningful naming and clear function boundaries  
- no duplicated business logic  
- no mutable default constructor arguments  
- constructor/domain validation for invariants  
- readable APIs and minimal side effects  
- testable, small, focused methods  

