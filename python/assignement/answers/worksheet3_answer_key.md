# Worksheet 3 Answer Key: Inheritance + Polymorphism + Composition vs Inheritance

## Section A: MCQ (1-40)

1. B  
2. C  
3. B  
4. C  
5. C  
6. B  
7. B  
8. B  
9. B  
10. B  
11. B  
12. B  
13. B  
14. B  
15. C  
16. B  
17. B  
18. C  
19. C  
20. C  
21. B  
22. B  
23. B  
24. B  
25. B  
26. B  
27. B  
28. B  
29. B  
30. C  
31. A  
32. C  
33. C  
34. B  
35. B  
36. C  
37. B  
38. B  
39. B  
40. B

---

## Section B: Code Reading / Predict Output (41-90)

41. `bark`  
42. `Asha 6`  
43. `B`  
44. `['D', 'B', 'C', 'A', 'object']`  
45.
```text
base
local base
```
46. `10`  
47. `True`  
48.
```text
INFO paid
AUDIT paid
```
49.
```text
B-start
C-start
A
C-end
B-end
```
50. `Card:500`  
51.
```text
EMAIL hello
SMS otp
```
52. `PUSH build done`  
53. `ok`  
54. `ValueError: invalid`  
55. `car -> engine started`  
56. `CONSOLE running`  
57.
```text
int:3
x
```
58. `4 6`  
59. `PDF:{'id': 1}`  
60. `B1 A A`  
61. `base`  
62. `7`  
63. `hello world`  
64. `amount must be >= 1000`  
65.
```text
CARD 100
UPI 100
```
66.
```text
False
True
```
67.
```text
connected
created ravi
```
68. `1 2 3`  
69. `A`  
70. `12`  
71. `{"msg":"ok"}`  
72. `BA`  
73. `True True`  
74. `True`  
75. `True`  
76. `start`  
77. `A`  
78. `['C', 'B', 'A', 'object']`  
79. `['Billed 300']`  
80.
```text
B
A
```
81. `21`  
82. `10`  
83. `True`  
84.
```text
9
a
```
85. `paid`  
86.
```text
1000
900.0
```
87. `['x'] []`  
88. `['x'] ['x']`  
89. `15`  
90. `B`

---

## Section C: Debug / Refactor / Improve Design (91-150) - Model Answers

91. Replace wrong inheritance with composition (`UserService` has `Database`).  
92. Call `super().__init__` and initialize parent fields first.  
93. Split parent responsibilities; keep base class minimal and stable.  
94. Replace role conditionals with `Employee` subclasses/polymorphism.  
95. Flatten deep hierarchy; keep shallow tree + composition.  
96. Add `PaymentProcessor(ABC)` with `process(amount)` contract.  
97. Keep child signatures compatible with parent contract.  
98. Use `super()` consistently, avoid explicit parent class calls.  
99. Use cooperative constructors (`super`, `**kwargs`) for multi-inheritance.  
100. Avoid overridable calls in parent constructor.  
101. Inject logger dependency through constructor.  
102. Depend on abstraction (ABC/Protocol), not concrete implementation.  
103. Rename generic methods to domain-intent methods.  
104. Use strategy/polymorphic provider classes for payment modes.  
105. Align child preconditions with parent (LSP-safe).  
106. Remove unnecessary tiny classes; compose behavior where simpler.  
107. Build shared contract tests for all payment implementations.  
108. Add `Protocol` and type-checkable structural contract.  
109. Replace forced inheritance with strategy composition.  
110. Use mixin only for small reusable behavior (e.g., timestamp).  
111. Keep mixins stateless/light, avoid complex init requirements.  
112. Document overridable hooks and expected behavior.  
113. Inject fake/mock collaborator for test isolation.  
114. Move shared mutable class list to instance field.  
115. Ensure child class behavior remains substitutable.  
116. Split fat interface into focused smaller contracts.  
117. Inject interchangeable dependency and swap at runtime.  
118. Use composition for logging concern; avoid deep logger hierarchy.  
119. Replace `isinstance` branching with polymorphic method calls.  
120. Make method lookup explicit and verify with `Class.mro()`.  
121. Keep return semantics consistent across overrides.  
122. Introduce notifier `Protocol` with `send(message)` method.  
123. Stabilize parent API, remove hidden side effects.  
124. Extract utility/helper collaborators instead of inheriting for reuse.  
125. Replace `Parent.__init__(self)` with `super().__init__()`.  
126. Add tests to verify parent expectations hold for every child.  
127. Convert to composition when relation is `has-a`.  
128. Keep guard clauses while preserving base contract semantics.  
129. Implement `DiscountStrategy` classes and inject strategy.  
130. Orchestrate via composed collaborators, each with one responsibility.  
131. Use behavior methods (`withdraw`, `remove_stock`) not direct mutation.  
132. Add integration tests through abstraction (not concrete coupling).  
133. Add tests for MRO-sensitive behavior if multiple inheritance exists.  
134. Extract shared code into composed component/helper.  
135. Constructor-inject dependencies; remove hidden hardcoded objects.  
136. Replace vague names with domain names (`PaymentGateway`, `OrderService`).  
137. Document preconditions/postconditions and exceptions in contract.  
138. Remove stricter child preconditions to satisfy LSP.  
139. Keep one stable base and move variations into strategies.  
140. Use `singledispatch` for function-level type-based variants.  
141. Replace format branches with polymorphic generators.  
142. Create export contract + `Csv/Json/Pdf` implementations.  
143. Move logging into composed logger dependency.  
144. Remove override side effects or document/standardize behavior.  
145. Shrink base class to essential reusable contract only.  
146. Introduce injected `RetryPolicy` component.  
147. Enforce same behavioral tests across subclasses.  
148. Clarify class/method names and document MRO-sensitive flow.  
149. Add new behavior via new classes, avoid modifying core logic.  
150. Final solution should show shallow hierarchy + composition-first + contract tests.

---

## Section D: Interview-Style Questions (151-200) - Model Points

151. Inheritance: specialized class deriving shared behavior from base (`Manager` is `Employee`).  
152. Composition: class uses another as dependency (`OrderService` has `PaymentGateway`).  
153. `is-a` -> inheritance; `has-a` -> composition.  
154. Composition lowers coupling and improves runtime flexibility/testing.  
155. Use inheritance for true hierarchy + stable base contract.  
156. `super()` follows MRO, important in multiple inheritance.  
157. MRO defines deterministic lookup order for methods/attributes.  
158. Diamond problem: two parents share one ancestor; ambiguity resolved by MRO.  
159. C3 ensures monotonic consistent linearization.  
160. Parent may call child override before child init completes.  
161. `_x` internal convention; `__x` mangled for collision avoidance.  
162. Fragile base class: small parent change breaks many children.  
163. Stabilize parent API, reduce scope, add contract tests.  
164. Polymorphism: same interface, different implementations at runtime.  
165. `checkout(payment)` works for Card/UPI/Wallet classes.  
166. Duck typing uses behavior compatibility, not inheritance.  
167. ABC is explicit runtime contract; Protocol is structural typing contract.  
168. Structural typing checks method shape, not inheritance chain.  
169. LSP: child must safely replace parent without breaking callers.  
170. Example violation: child requires stricter input than parent promises.  
171. Define clear preconditions/postconditions and keep them consistent.  
172. Run same contract tests across all implementations.  
173. Add new implementation class instead of editing core branches.  
174. Composition allows fake/mock injection for isolated tests.  
175. DI: pass dependency through constructor/interface.  
176. Type-switch chains increase churn and violate OCP.  
177. Extract contract, add implementations, migrate calls gradually.  
178. Use strategy for variable behavior, inheritance for true specialization.  
179. Mixins useful for small cross-cutting behavior; avoid heavy state/multi-responsibility.  
180. Keep hierarchy shallow and behavior-focused.  
181. Signals: deep chains, frequent breakage, unclear responsibilities.  
182. Payment module: contract + provider classes + injected usage.  
183. Logging design: `Logger` interface + swappable implementations.  
184. Abstractions hide implementation, reducing direct coupling.  
185. Too broad: hard to implement; too narrow: too many interfaces.  
186. Document input rules, outputs, side effects, and errors.  
187. Consistent semantics prevent surprises and LSP breaks.  
188. Misused operators can create non-intuitive behavior.  
189. `singledispatch` is good for function-level type variations.  
190. Use parametrized tests over list of implementations.  
191. Fakes verify interactions and make tests deterministic.  
192. Extract collaborators, inject dependencies, reduce inheritance depth.  
193. Composition supports easier runtime swap than inheritance hierarchy changes.  
194. Regression example: parent `log()` change breaks all subclasses.  
195. Composition win: swap notifier without changing order logic.  
196. MRO: ordered path Python follows to find methods in class graph.  
197. Checklist: signature compatibility, behavior compatibility, exception consistency.  
198. Signals: less branching, easier extension, fewer regressions in core.  
199. Report engine: `ReportGenerator` contract + `Pdf/Csv/Json` implementations + DI.  
200. Billing redesign: flatten hierarchy, introduce strategies/contracts, add substitution tests.

---

## Capstone Project - Expected Solution Characteristics

- clear contracts and substitution-safe implementations  
- composition-first orchestration with dependency injection  
- inheritance only for true `is-a` specialization  
- no large type-switch conditionals in core flow  
- tests for LSP behavior, contract conformance, and extension safety  

