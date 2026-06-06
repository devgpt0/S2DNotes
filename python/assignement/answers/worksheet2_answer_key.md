# Worksheet 2 Answer Key: Encapsulation + Abstraction

## Section A: MCQ (1-40)

1. B  
2. B  
3. B  
4. B  
5. B  
6. B  
7. B  
8. A  
9. B  
10. B  
11. B  
12. B  
13. B  
14. B  
15. C  
16. B  
17. B  
18. B  
19. B  
20. B  
21. B  
22. B  
23. B  
24. B  
25. C  
26. B  
27. D  
28. B  
29. A  
30. B  
31. B  
32. B  
33. B  
34. B  
35. C  
36. B  
37. B  
38. B  
39. B  
40. B

---

## Section B: Code Reading / Predict Output (41-90)

41. `500`  
42. `10`  
43. `ValueError: invalid`  
44. `False True`  
45. `Ravi`  
46. `60`  
47. `2`  
48. `-100`  
49. `60000`  
50. `ValueError: negative`  
51. `0`  
52. `75`  
53. `Alex`  
54. `3`  
55. `ValueError: too much`  
56. `False`  
57. `True`  
58. `{'_A__x': 10}`  
59. `750`  
60. `30`  
61. `TypeError` (cannot instantiate abstract class)  
62. `UPI:500`  
63. `TypeError` (abstract method not implemented)  
64. `sms`  
65. `3`  
66. `simple`  
67. `sent`  
68. `read:a.txt`  
69. `saved:x.txt:5`  
70. `engine_started`  
71. `False`  
72. `True`  
73. `fast`  
74. `A`  
75. `push`  
76. `done`  
77. `deleted:a`  
78. `3`  
79. `HELLO`  
80. `processed`  
81. `ValueError: invalid`  
82. `True sent`  
83. `saved:tom`  
84. `7`  
85. `2`  
86. `AB`  
87. `True`  
88. `123`  
89. `True`  
90. `ok:notes.txt`

---

## Section C: Debug / Refactor / Improve Design (91-150) - Model Answers

91. Use protected field + validation (`balance >= 0`) in constructor and methods.  
92. Convert `salary` to validated property; reject negative values.  
93. Replace direct mutation with `withdraw(amount)` domain method.  
94. Add validated properties: `price > 0`, `quantity >= 0`.  
95. Replace get/set methods with `@property` and setter validation.  
96. Rename class/method/fields meaningfully; validate assignments.  
97. Hide list using `_items`; expose safe add/remove operations.  
98. Replace `order.status = ...` with `order.mark_shipped()` transition method.  
99. Replace arithmetic mutation with `remove_stock(units)` domain behavior.  
100. Add age validation (`>=0`, optional max range) in setter.  
101. Validate opening balance in constructor.  
102. Use `transfer()` method that validates and updates both accounts safely.  
103. Expose one high-level method (facade), keep steps private.  
104. Create single method like `send_message()` handling internals.  
105. Rename vague `do()` to concrete action (`register_user`, etc.).  
106. Introduce `PaymentProcessor(ABC)` + concrete classes for each mode.  
107. Define abstract methods required by payment contract.  
108. Implement missing abstract method(s) in subclass.  
109. Inject `Notification` abstraction via constructor (DIP).  
110. Replace low-level steps with `save()` abstraction.  
111. Replace stepwise API with one intention-revealing method.  
112. Use template/facade public method orchestrating private steps.  
113. Validate marks in constructor/setter (`0..100`).  
114. Prevent external direct mutation; expose validated methods/properties.  
115. Expose read-only safe view instead of internal history list.  
116. Validate discount range (`0 <= x <= 100`).  
117. Add `remove_stock()` with checks for positive units and sufficiency.  
118. Provide one orchestrating `process_payment()` API.  
119. Provide `login()` abstraction hiding inner steps.  
120. Rename `process()` to explicit behavior (`generate_payslip`, etc.).  
121. Expose high-level invoice API; hide SQL details internally.  
122. Define `Notification` abstraction with channel implementations.  
123. Hide socket details behind `send_request()` style API.  
124. Introduce `Storage(ABC)` with `save/read/delete` contract.  
125. Create `Exporter(ABC)` + `CsvExporter`, `JsonExporter`, `DbExporter`.  
126. Extract common validation helper used by all methods.  
127. Keep one public method, move details to private helpers.  
128. Replace public config with validated properties.  
129. Reduce public surface, expose only needed behavior methods.  
130. Add retry abstraction/policy class and inject into payment flow.  
131. Validate interest rate in setter/domain method; reject negative invalid values.  
132. Enforce `amount > 0` checks at constructor/method boundaries.  
133. Hide ordering constraints behind one public orchestrating method.  
134. Build one high-level method calling five private steps.  
135. Depend on `Logger` abstraction, inject concrete logger.  
136. Extract shared logic and use polymorphic channel implementations.  
137. Add non-empty customer ID validation in setter/constructor.  
138. Enforce finite-state transitions using explicit transition methods.  
139. Move business rules to domain object methods; keep controller thin.  
140. Make transfer atomic-style: validate first, then perform both updates safely.  
141. Create `Notification(ABC)` and implement `send()` in each channel.  
142. Split `FileManager` into abstraction + backend implementations.  
143. Replace provider branching with polymorphic classes.  
144. Provide `serialize()` abstraction and format-specific implementations.  
145. Introduce repository abstraction for CRUD/persistence contract.  
146. Remove SQL leakage from service layer via repository methods.  
147. `close_account()` should check pending dues before state transition.  
148. Add report abstraction with interchangeable format generators.  
149. Replace nesting with guard clauses + clear early returns.  
150. Final rewrite should show: protected state, validation, clear API, ABC extension point.

---

## Section D: Interview-Style Questions (151-200) - Model Points

151. Encapsulation: protect state via controlled behavior; example `BankAccount.withdraw`.  
152. Abstraction: expose essential API, hide internals; example `storage.save()`.  
153. Encapsulation protects validity, abstraction simplifies usage.  
154. Direct mutation bypasses rules and creates invalid states.  
155. Invariant = rule always true (`balance >= 0`, `0<=marks<=100`).  
156. Boundary checks belong in constructor, setters, and domain methods.  
157. Use `@property` when you need attribute syntax + validation/control.  
158. `_name`: convention protected; `__name`: mangled `_Class__name`.  
159. Python private is discouragement/anti-collision, not absolute access control.  
160. `deposit/withdraw/transfer` with positive checks + balance safety.  
161. Validate on creation and every mutation boundary.  
162. Expose safe methods; avoid raw field edits.  
163. Public only for stable API; internal fields protected/private.  
164. Signs: public mutable internals, no validation, bypassable invariants.  
165. Cognitive load = mental effort; good API hides multi-step internals.  
166. Vague names hide intent and increase onboarding/debug cost.  
167. Intuitive API = clear names, predictable behavior, small surface.  
168. Abstraction standardizes use and reduces onboarding overhead.  
169. Abstract class = non-instantiable contract template.  
170. Abstract classes have unimplemented required methods.  
171. `@abstractmethod` enforces implementation in subclasses.  
172. Prevents incomplete concrete classes from being instantiated.  
173. Polymorphism: same contract, different implementations (`pay()` variants).  
174. Replace concrete dependency with injected abstraction.  
175. Abstraction decouples callers from implementation details.  
176. Example analogy: car `start()` hides engine internals.  
177. Contract + implementations scales better than giant class.  
178. Add new implementation without editing core orchestrator.  
179. Anti-patterns: vague APIs, over-abstraction, leaked internals.  
180. Anti-patterns: public mutable state, missing invariants.  
181. Multi-cloud storage: `Storage` contract + provider implementations.  
182. Notification module: `Notification` abstraction + channel classes.  
183. Order lifecycle: explicit transition methods + state validation.  
184. Define payment interface and 3 concrete processors.  
185. Unit test invariants and forbidden mutations.  
186. Contract tests run same expectations across all implementations.  
187. Test setter valid/invalid values and error messages.  
188. Validate first, then atomic transfer update or rollback strategy.  
189. Move multi-step API to one facade method with private steps.  
190. Weak abstraction signs: too many steps, vague names, leaked details.  
191. Missing invariant signs: invalid values accepted silently.  
192. Trade-off: too much abstraction adds indirection; too little adds duplication/coupling.  
193. Trade-off: strict safety vs speed of ad-hoc changes.  
194. Logs/errors should be explicit, actionable, and preserve context.  
195. DIP: high-level module depends on `Notification` abstraction.  
196. Add new class implementing existing contract; keep core unchanged.  
197. Document preconditions/postconditions and extension points.  
198. Signals: fewer conditionals, easier extension, lower churn in core files.  
199. Signals: fewer invalid-state bugs, clearer validation boundaries.  
200. Fintech mini-core: encapsulated accounts + abstracted processors + tested contracts.

---

## Capstone Project - Expected Solution Characteristics

- clear contracts (`ABC`/`Protocol`)  
- encapsulated state and invariants  
- no giant `if/elif` provider switches  
- composition + dependency injection in orchestration layer  
- tests for invariants, contract behavior, and failure paths  

