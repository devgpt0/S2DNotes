```markdown
# Java Methods & Control Flow - 35 Questions

**Total Questions:** 35  
**Categories:**  
- Level 1 (Beginner): 10 Questions  
- Level 2 (Intermediate): 10 Questions  
- Level 3 (Advanced): 10 Questions  
- Code Quality: 5 Questions  

**Topics Covered:** Methods (functions), parameters, varargs, scope, return, recursion, method overloading, switch, loops (for, while, do-while, enhanced for), break/continue, labeled statements, plus Java 8+ features like lambdas, method references, and Streams for list traversal (forEach, map, filter, etc.).

**Note:** All code snippets are valid Java. Assume they are inside a `main` method or appropriate class context unless specified.

---

## Level 1: Beginner (10 Questions)

1. **What is the output of the following code?**
   ```java
   public static void greet(String name) {
       System.out.println("Hello, " + name + "!");
   }

   greet("Adarsh");
   greet(null);
   ```

2. **What will be printed?**
   ```java
   public static int add(int a, int b) {
       return a + b;
   }

   System.out.println(add(3, 5));
   System.out.println(add(10));
   ```

3. **Predict the output (scope):**
   ```java
   int x = 10;
   public static void func() {
       int x = 20;
       System.out.println(x);
   }

   func();
   System.out.println(x);
   ```

4. **What is the output? (Method overloading)**
   ```java
   public static void print(int n) {
       System.out.println("int: " + n);
   }

   public static void print(String s) {
       System.out.println("String: " + s);
   }

   print(5);
   print("Hello");
   ```

5. **What does this code print? (Enhanced for loop)**
   ```java
   int[] nums = {1, 2, 3, 4};
   for (int n : nums) {
       System.out.print(n + " ");
   }
   ```

6. **What is the output when using switch?**
   ```java
   int day = 3;
   switch (day) {
       case 1: System.out.println("Monday"); break;
       case 2: System.out.println("Tuesday"); break;
       case 3: System.out.println("Wednesday"); break;
       default: System.out.println("Other");
   }
   ```

7. **Predict the output (break and continue):**
   ```java
   for (int i = 0; i < 5; i++) {
       if (i == 2) continue;
       if (i == 4) break;
       System.out.print(i + " ");
   }
   ```

8. **What will be printed? (Varargs)**
   ```java
   public static void sum(int... numbers) {
       int total = 0;
       for (int n : numbers) total += n;
       System.out.println(total);
   }

   sum(1, 2, 3);
   sum();
   ```

9. **Rewrite the following using enhanced for loop:**
   ```java
   String[] fruits = {"apple", "banana", "cherry"};
   for (int i = 0; i < fruits.length; i++) {
       System.out.println(fruits[i]);
   }
   ```

10. **What is printed? (Do-while loop)**
    ```java
    int i = 5;
    do {
        System.out.print(i + " ");
        i--;
    } while (i > 0);
    ```

---

## Level 2: Intermediate (10 Questions)

1. **What is the output? (Fall-through in switch)**
   ```java
   int x = 2;
   switch (x) {
       case 1:
           System.out.print("A ");
       case 2:
           System.out.print("B ");
       case 3:
           System.out.print("C ");
           break;
       default:
           System.out.print("D");
   }
   ```

2. **What will be printed? (Labeled break)**
   ```java
   outer: for (int i = 0; i < 3; i++) {
       for (int j = 0; j < 3; j++) {
           if (i + j == 3) break outer;
           System.out.print(i + "," + j + " ");
       }
   }
   ```

3. **Predict the output (Recursion):**
   ```java
   public static int factorial(int n) {
       if (n <= 1) return 1;
       return n * factorial(n - 1);
   }

   System.out.println(factorial(5));
   ```

4. **What does this code produce? (Stream forEach)**
   ```java
   List<Integer> nums = Arrays.asList(1, 2, 3, 4, 5);
   nums.stream().forEach(n -> System.out.print(n * 2 + " "));
   ```

5. **What is the output? (Ternary operator)**
   ```java
   int a = 10, b = 20;
   String result = (a > b) ? "A is greater" : "B is greater or equal";
   System.out.println(result);
   ```

6. **What will be printed? (Method reference)**
   ```java
   List<String> names = Arrays.asList("alice", "bob", "charlie");
   names.stream().map(String::toUpperCase).forEach(System.out::println);
   ```

7. **Predict carefully (while vs do-while):**
   ```java
   int i = 0;
   while (i < 0) {
       System.out.print("While ");
       i++;
   }
   do {
       System.out.print("Do-While ");
   } while (i < 0);
   ```

8. **What does this return? (Stream map + filter)**
   ```java
   List<Integer> nums = Arrays.asList(1, 2, 3, 4, 5, 6);
   List<Integer> result = nums.stream()
       .filter(n -> n % 2 == 0)
       .map(n -> n * 2)
       .collect(Collectors.toList());
   System.out.println(result);
   ```

9. **What is the difference?**
   ```java
   // Traditional loop
   for (int i = 0; i < 10; i++) {
       if (i % 2 == 0) System.out.print(i + " ");
   }

   // Equivalent using Stream
   IntStream.range(0, 10).filter(i -> i % 2 == 0).forEach(i -> System.out.print(i + " "));
   ```

10. **What is printed? (Infinite loop risk)**
    ```java
    for (int i = 0; i < 5; ) {
        System.out.print(i + " ");
        // Missing update
    }
    ```

---

## Level 3: Advanced (10 Questions)

1. **What will be printed? (Closure-like behavior with lambda)**
   ```java
   List<Integer> list = new ArrayList<>();
   for (int i = 0; i < 5; i++) {
       final int x = i;  // or effectively final
       list.add(() -> System.out.print(x + " "));
   }
   list.forEach(Runnable::run);
   ```

2. **What is the output? (Labeled continue)**
   ```java
   outer: for (int i = 0; i < 4; i++) {
       for (int j = 0; j < 4; j++) {
           if (j == 2) continue outer;
           System.out.print(i + "" + j + " ");
       }
   }
   ```

3. **What does this recursive method return?**
   ```java
   public static int sumList(List<Integer> list, int index) {
       if (index >= list.size()) return 0;
       return list.get(index) + sumList(list, index + 1);
   }

   List<Integer> nums = Arrays.asList(1, 2, 3, 4, 5);
   System.out.println(sumList(nums, 0));
   ```

4. **Which is more efficient and why? (Large data)**
   ```java
   // Option A - Stream
   IntStream.range(0, 1_000_000).filter(i -> i % 2 == 0).sum();

   // Option B - Traditional loop
   long sum = 0;
   for (int i = 0; i < 1_000_000; i++) {
       if (i % 2 == 0) sum += i;
   }
   ```

5. **What is the output of this complex stream?**
   ```java
   List<List<Integer>> matrix = Arrays.asList(
       Arrays.asList(1, 2, 3),
       Arrays.asList(4, 5),
       Arrays.asList(6, 7, 8, 9)
   );
   List<Integer> result = matrix.stream()
       .flatMap(List::stream)
       .filter(n -> n % 2 == 0)
       .collect(Collectors.toList());
   System.out.println(result);
   ```

6. **What will be printed? (Varargs + overloading)**
   ```java
   public static void process(int... nums) {
       System.out.println("Varargs: " + Arrays.toString(nums));
   }

   public static void process(int a, int b) {
       System.out.println("Two params: " + a + ", " + b);
   }

   process(1, 2);
   process(1, 2, 3);
   ```

7. **Rewrite this using Stream API (map + collect):**
   ```java
   List<Integer> nums = Arrays.asList(1, 2, 3, 4, 5);
   List<Integer> cubes = new ArrayList<>();
   for (Integer n : nums) {
       cubes.add(n * n * n);
   }
   System.out.println(cubes);
   ```

8. **What is the output? (Switch expression - Java 14+)**
   ```java
   int day = 2;
   String result = switch (day) {
       case 1 -> "Monday";
       case 2 -> "Tuesday";
       default -> "Other";
   };
   System.out.println(result);
   ```

9. **What happens here? (Stream vs parallelStream performance discussion)**
   ```java
   List<Integer> largeList = ...; // assume 1 million elements
   largeList.parallelStream().filter(n -> n % 2 == 0).count();
   ```

10. **Very tricky (Effectively final variable in lambda):**
    ```java
    int x = 10;
    Runnable r = () -> System.out.println(x);
    // x = 20;  // What if this line is added?
    r.run();
    ```

---

## Code Quality Questions (5 Questions)

1. **Code Review:**  
   What issues do you see in this code and how would you improve it for readability and performance?
   ```java
   public static int processNumbers(int[] numbers) {
       int result = 0;
       for (int i = 0; i < numbers.length; i++) {
           if (numbers[i] > 10) {
               result += numbers[i] * 2;
           }
       }
       return result;
   }
   ```

2. **Refactor this method using Stream API:**
   ```java
   public static List<Integer> getEvenSquares(List<Integer> lst) {
       List<Integer> evens = new ArrayList<>();
       for (Integer num : lst) {
           if (num % 2 == 0) {
               evens.add(num * num);
           }
       }
       return evens;
   }
   ```

3. **When should you prefer traditional loops over Streams / lambdas?**  
   Give one scenario where a classic `for` loop is clearly better than using `Stream.forEach()` or `map()`, and explain why (consider performance, readability, or debugging).

4. **Improve this code (better loop and method design):**
   ```java
   public static int calculateTotal(int[] prices) {
       int total = 0;
       int i = 0;
       while (i < prices.length) {
           total += prices[i];
           i++;
       }
       return total;
   }
   ```

5. **Best Practice Discussion:**  
   a) Explain the risks of using `switch` without `break` statements.  
   b) When writing a method that processes a collection (List/Array), should you modify it in-place or return a new collection? Why? Support your answer with a Stream example.

---

s!