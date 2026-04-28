Here is a complete set of **Control Flow** questions in Python 3, divided into three difficulty levels:

### Level 1 (Beginner) – 10 Tricky Questions

1. **What will be the output?**
   ```python
   x = 5
   if x > 10:
       print("A")
   elif x > 3:
       print("B")
   else:
       print("C")
   ```

2. **What is printed?**
   ```python
   for i in range(5):
       if i == 3:
           continue
       print(i, end=" ")
   ```

3. **Predict the output:**
   ```python
   i = 0
   while i < 5:
       print(i)
       i += 1
       if i == 3:
           break
   ```

4. **What happens here?**
   ```python
   x = 10
   if x > 5:
       pass
   print("Done")
   ```

5. **Tricky one:**
   ```python
   a = True
   b = False
   if a or b and not a:
       print("Yes")
   else:
       print("No")
   ```

6. **What is the output?**
   ```python
   for i in range(10):
       if i % 2 == 0:
           print(i, "even")
           continue
       print(i, "odd")
   ```

7. **Predict:**
   ```python
   x = 0
   while x < 10:
       x += 2
       if x == 6:
           continue
       print(x)
   ```

8. **What will print?**
   ```python
   num = 5
   if num := 10:          # Walrus operator
       print(num)
   ```

9. **Tricky nested:**
   ```python
   for i in range(3):
       for j in range(3):
           if i == j:
               break
       print(i, j)
   ```

10. **What is the final value of `count`?**
    ```python
    count = 0
    for i in range(5):
        for j in range(5):
            if i == j:
                break
            count += 1
    print(count)
    ```

---

### Level 2 (Intermediate) – 10 Tricky Questions

1. **What is printed?**
   ```python
   x = [1, 2, 3]
   for i in x:
       x.append(i*10)
       if len(x) > 6:
           break
   print(x)
   ```

2. **Predict the output:**
   ```python
   i = 5
   while i > 0:
       i -= 1
       if i == 2:
           continue
       print(i, end=" ")
   else:
       print("Loop ended normally")
   ```

3. **Tricky walrus + if:**
   ```python
   if (n := int(input("Enter number: "))) > 10:
       print(f"{n} is greater than 10")
   else:
       print(f"{n} is not greater than 10")
   ```

4. **What is the output?**
   ```python
   a = 0
   b = 10
   while a < b:
       a += 1
       b -= 1
       print(a, b)
   ```

5. **Complex condition:**
   ```python
   x = 5
   y = 10
   if x > 3 and y < 15 or x == 0:
       print("True")
   else:
       print("False")
   ```

6. **What will be printed?**
   ```python
   for i in range(1, 10):
       if i % 3 == 0 and i % 5 == 0:
           print("FizzBuzz")
       elif i % 3 == 0:
           print("Fizz")
       elif i % 5 == 0:
           print("Buzz")
       else:
           print(i)
   ```

7. **Tricky break + else:**
   ```python
   for i in range(5):
       if i == 3:
           break
       print(i)
   else:
       print("No break occurred")
   ```

8. **Predict carefully:**
   ```python
   x = True
   y = False
   z = True
   if not x or y and z:
       print("A")
   elif x and not y:
       print("B")
   else:
       print("C")
   ```

9. **What is the output?**
   ```python
   numbers = [1, 2, 3, 4, 5]
   result = []
   for num in numbers:
       if num % 2 == 0:
           result.append(num * 2)
           continue
       result.append(num * 3)
   print(result)
   ```

10. **Very tricky:**
    ```python
    i = 0
    while True:
        i += 1
        if i == 5:
            break
        if i % 2 == 0:
            continue
        print(i)
    ```

---

### Level 3 (Advanced) – 10 Tricky Questions

1. **What will be the output?**
   ```python
   def func():
       for i in range(3):
           try:
               if i == 1:
                   raise ValueError
               print(i)
           finally:
               print("Finally", i)
   func()
   ```

2. **Complex control flow:**
   ```python
   x = 0
   while x < 10:
       try:
           if x == 5:
               raise Exception("Stop")
           print(x)
       except:
           break
       finally:
           x += 1
   ```

3. **Nested loops with labeled behavior (Python style):**
   ```python
   for i in range(4):
       for j in range(4):
           if i * j > 6:
               break
           print(i, j, end=" | ")
       else:
           continue
       break
   ```

4. **Walrus operator in while:**
   ```python
   data = [1, 2, 3, 4, 5, 6]
   i = 0
   while (n := data[i]) < 6:
       print(n)
       i += 1
   ```

5. **Very tricky:**
   ```python
   x = 10
   if x > 5:
       x = 20
       if x > 15:
           x = 30
       elif x > 10:
           x = 25
   print(x)
   ```

6. **Match statement (Python 3.10+):**
   ```python
   def http_status(code):
       match code:
           case 200:
               return "OK"
           case 404:
               return "Not Found"
           case _ if code >= 500:
               return "Server Error"
           case _:
               return "Unknown"
   print(http_status(503))
   ```

7. **Control flow with generator:**
   ```python
   gen = (i for i in range(10) if i % 2 == 0)
   for num in gen:
       if num == 6:
           break
       print(num)
   ```

8. **What is printed?**
   ```python
   i = 0
   while i < 5:
       i += 1
       if i == 3:
           continue
       print(i)
   else:
       print("While loop completed")
   ```

9. **Advanced break/continue logic:**
   ```python
   for i in range(1, 6):
       print("Outer", i)
       for j in range(1, 6):
           if j == 3:
               continue
           if i * j > 10:
               break
           print("  Inner", j)
   ```

10. **Extremely tricky:**
    ```python
    x = [False, True, False]
    if any(x) and all(x):
        print("A")
    elif any(x) or all(x):
        print("B")
    else:
        print("C")
    ```

---

### Code Quality Questions (5 Questions)

These focus on best practices, readability, and proper use of control flow.

1. **Code Review:**  
   What is wrong with this code and how would you improve it?
   ```python
   i = 0
   while True:
       if i > 100:
           break
       print(i)
       i = i + 1
   ```

2. **Refactor this code for better readability:**
   ```python
   if score >= 90:
       grade = "A"
   elif score >= 80:
       grade = "B"
   elif score >= 70:
       grade = "C"
   elif score >= 60:
       grade = "D"
   else:
       grade = "F"
   ```

3. **What is a better way to write this?**
   ```python
   if x != 0:
       if y / x > 10:
           print("High")
   ```

4. **Improve this nested loop code:**
   ```python
   for i in range(10):
       for j in range(10):
           if i + j == 7:
               print(i, j)
   ```

5. **Best Practice Question:**  
   When should you prefer `for` loop over `while` loop?  
   Give an example where using `while` is more appropriate than `for`, and explain why.

---
