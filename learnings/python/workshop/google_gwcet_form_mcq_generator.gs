/**
 * Google Apps Script: Generate the GWCET Python Lists MCQ assessment.
 * Scope: concepts 1-12 in ../notes/collection_framework/list.md.
 */

function createGwcetPythonListsQuizForm() {
  const config = {
    title: "GWCET Python and Agentic AI MCQ Assessment",
    description: [
      "College: GWCET",
      "Total Questions: 100",
      "Each question carries 1 mark.",
      "All questions are mandatory.",
      "No negative marking.",
      "Submit the form only after answering every question.",
      "Responses cannot be edited after submission.",
    ].join("\n"),
    pointsPerQuestion: 1,
  };
  const questions = buildQuestionBank();
  validateQuestionBank(questions);

  const form = FormApp.create(config.title)
    .setDescription(config.description)
    .setIsQuiz(true)
    .setShuffleQuestions(false)
    .setCollectEmail(true)
    .setProgressBar(true)
    .setAllowResponseEdits(false)
    .setLimitOneResponsePerUser(true);

  form.addTextItem().setTitle("Name of the Student").setRequired(true);
  form.addTextItem().setTitle("Email ID").setRequired(true);
  form
    .addTextItem()
    .setTitle("Phone Number of the Student")
    .setRequired(true)
    .setValidation(
      FormApp.createTextValidation()
        .requireTextMatchesPattern("^[0-9]{10}$")
        .setHelpText("Enter a valid 10-digit phone number.")
        .build(),
    );

  const departmentItem = form.addListItem();
  departmentItem.setTitle("Department").setRequired(true);
  departmentItem.setChoices(
    [
      "Artifical Intelligence and Data Science",
      "Electronics and Communication",
    ].map((department) => departmentItem.createChoice(department)),
  );

  form.addPageBreakItem().setTitle("Python Lists MCQ Assessment");

  questions.forEach((question, index) => {
    const item = form.addMultipleChoiceItem();
    const [questionTitle, code] = question.question.split("\n\n");
    const choices = question.options.map((option, optionIndex) => ({
      option,
      isCorrect: optionIndex === question.correctIndex,
    }));
    fisherYatesShuffle(choices);
    item
      .setTitle(`${index + 1}. ${questionTitle}`)
      .setHelpText(code || "")
      .setChoices(
        choices.map(({ option, isCorrect }) =>
          item.createChoice(option, isCorrect),
        ),
      )
      .setRequired(true)
      .setPoints(config.pointsPerQuestion);
  });

  verifyGeneratedQuestions(form, questions, config.pointsPerQuestion);
  Logger.log(`Form created: ${form.getPublishedUrl()}`);
  Logger.log(`Edit URL: ${form.getEditUrl()}`);
}

function createQuestion(question, correctOption, ...incorrectOptions) {
  return {
    question,
    options: [correctOption, ...incorrectOptions],
    correctIndex: 0,
  };
}

function createCodeQuestion(code, correctOption, ...incorrectOptions) {
  return createQuestion(
    `What is printed?\n\n${code}`,
    correctOption,
    ...incorrectOptions,
  );
}

function buildQuestionBank() {
  const codeQuestions = [
    createCodeQuestion("items = [1, 2, 3]\nprint(items)", "[1, 2, 3]", "(1, 2, 3)", "{1, 2, 3}", "TypeError"),
    createCodeQuestion("items = [1, \"two\", True]\nprint(items[1])", "two", "1", "True", "IndexError"),
    createCodeQuestion("items = list()\nprint(items)", "[]", "()", "{}", "None"),
    createCodeQuestion("letters = list(\"Ada\")\nprint(letters)", "['A', 'd', 'a']", "['Ada']", "Ada", "('A', 'd', 'a')"),
    createCodeQuestion("numbers = list(range(4))\nprint(numbers)", "[0, 1, 2, 3]", "[1, 2, 3, 4]", "[0, 1, 2, 3, 4]", "range(4)"),
    createCodeQuestion("fruits = [\"apple\", \"orange\", \"mango\"]\nprint(fruits[0])", "apple", "orange", "mango", "IndexError"),
    createCodeQuestion("fruits = [\"apple\", \"orange\", \"mango\"]\nprint(fruits[-1])", "mango", "apple", "orange", "-1"),
    createCodeQuestion("nums = [10, 20, 30, 40, 50]\nprint(nums[:3])", "[10, 20, 30]", "[10, 20, 30, 40]", "[20, 30, 40]", "[10, 20]"),
    createCodeQuestion("nums = [10, 20, 30, 40, 50]\nprint(nums[1::2])", "[20, 40]", "[10, 30, 50]", "[20, 30, 40]", "[50, 30, 10]"),
    createCodeQuestion("nums = [10, 20, 30, 40]\nprint(nums[::-1])", "[40, 30, 20, 10]", "[10, 20, 30, 40]", "[20, 30, 40]", "[40, 20]"),
    createCodeQuestion("nums = [1, 2, 3]\nprint(nums[10:])", "[]", "IndexError", "None", "[3]"),
    createCodeQuestion("fruits = [\"apple\", \"banana\", \"cherry\"]\nfruits[1] = \"blueberry\"\nprint(fruits)", "['apple', 'blueberry', 'cherry']", "['blueberry', 'banana', 'cherry']", "['apple', 'banana', 'blueberry']", "['apple', 'banana', 'cherry', 'blueberry']"),
    createCodeQuestion("values = [1, 2, 3, 4]\nvalues[1:3] = [8]\nprint(values)", "[1, 8, 4]", "[1, 8, 3, 4]", "[1, 2, 8, 4]", "[8, 1, 4]"),
    createCodeQuestion("values = [1, 2]\nvalues[1:2] = [7, 8]\nprint(values)", "[1, 7, 8]", "[1, 7]", "[7, 8]", "[1, 2, 7, 8]"),
    createCodeQuestion("fruits = [\"apple\", \"banana\"]\nfruits.append(\"mango\")\nprint(fruits)", "['apple', 'banana', 'mango']", "['mango', 'apple', 'banana']", "['apple', 'banana']", "['apple', 'banana', ['mango']]"),
    createCodeQuestion("items = [1, 2]\nitems.append([3, 4])\nprint(items)", "[1, 2, [3, 4]]", "[1, 2, 3, 4]", "[[1, 2], [3, 4]]", "[3, 4, 1, 2]"),
    createCodeQuestion("fruits = [\"apple\", \"mango\"]\nfruits.insert(1, \"banana\")\nprint(fruits)", "['apple', 'banana', 'mango']", "['banana', 'apple', 'mango']", "['apple', 'mango', 'banana']", "['apple', 'banana']"),
    createCodeQuestion("items = [1, 2]\nitems.extend([3, 4])\nprint(items)", "[1, 2, 3, 4]", "[1, 2, [3, 4]]", "[[1, 2], [3, 4]]", "[3, 4]"),
    createCodeQuestion("fruits = [\"apple\", \"banana\", \"banana\", \"mango\"]\nfruits.remove(\"banana\")\nprint(fruits)", "['apple', 'banana', 'mango']", "['apple', 'mango']", "['apple', 'banana', 'banana', 'mango']", "['apple', 'mango', 'banana']"),
    createCodeQuestion("items = [10, 20, 30]\nremoved = items.pop()\nprint(removed, items)", "30 [10, 20]", "10 [20, 30]", "30 [10, 20, 30]", "20 [10, 30]"),
    createCodeQuestion("items = [10, 20, 30]\nremoved = items.pop(0)\nprint(removed, items)", "10 [20, 30]", "30 [10, 20]", "0 [10, 20, 30]", "10 [10, 20, 30]"),
    createCodeQuestion("items = [1, 2, 3, 4]\ndel items[1:3]\nprint(items)", "[1, 4]", "[1, 2, 4]", "[2, 3]", "[1, 2, 3, 4]"),
    createCodeQuestion("items = [1, 2, 3]\nitems.clear()\nprint(items)", "[]", "None", "[1, 2, 3]", "()"),
    createCodeQuestion("a = [1, 2]\nb = a\nb.append(3)\nprint(a)", "[1, 2, 3]", "[1, 2]", "[3, 1, 2]", "TypeError"),
    createCodeQuestion("a = [1, 2, 3]\nb = a[:]\nb[0] = 99\nprint(a, b)", "[1, 2, 3] [99, 2, 3]", "[99, 2, 3] [99, 2, 3]", "[1, 2, 3] [1, 2, 3]", "[99, 2, 3] [1, 2, 3]"),
    createCodeQuestion("a = [[1, 2], [3, 4]]\nb = a.copy()\nb[0][0] = 99\nprint(a)", "[[99, 2], [3, 4]]", "[[1, 2], [3, 4]]", "[[99], [3, 4]]", "TypeError"),
    createCodeQuestion("a = [1, 2, 3]\nb = [4, 5]\nprint(a + b)", "[1, 2, 3, 4, 5]", "[5, 7, 3]", "[1, 2, 3, [4, 5]]", "TypeError"),
    createCodeQuestion("values = [1, 2]\nprint(values * 2)", "[1, 2, 1, 2]", "[2, 4]", "[1, 1, 2, 2]", "[[1, 2], [1, 2]]"),
    createCodeQuestion("fruits = [\"apple\", \"mango\"]\nprint(\"apple\" in fruits)", "True", "False", "apple", "1"),
    createCodeQuestion("fruits = [\"apple\", \"mango\"]\nprint(\"grape\" not in fruits)", "True", "False", "grape", "None"),
    createCodeQuestion("nums = [1, 2, 3, 8, 9]\nprint(len(nums))", "5", "4", "9", "23"),
    createCodeQuestion("nums = [4, 2, 7]\nprint(min(nums))", "2", "4", "7", "3"),
    createCodeQuestion("nums = [4, 2, 7]\nprint(max(nums))", "7", "4", "2", "13"),
    createCodeQuestion("nums = [4, 2, 7]\nprint(sum(nums))", "13", "7", "3", "28"),
    createCodeQuestion("nums = [1, 2, 3]\nnums.reverse()\nprint(nums)", "[3, 2, 1]", "[1, 2, 3]", "[2, 3, 1]", "None"),
    createCodeQuestion("nums = [1, 2, 3]\nprint(list(reversed(nums)))", "[3, 2, 1]", "[1, 2, 3]", "reversed([1, 2, 3])", "(3, 2, 1)"),
    createCodeQuestion("nums = [3, 1, 2]\nprint(sorted(nums))", "[1, 2, 3]", "[3, 1, 2]", "None", "[3, 2, 1]"),
    createCodeQuestion("nums = [3, 1, 2]\nresult = nums.sort()\nprint(nums, result)", "[1, 2, 3] None", "[3, 1, 2] [1, 2, 3]", "[1, 2, 3] [1, 2, 3]", "None [1, 2, 3]"),
    createCodeQuestion("nums = [-10, 5, -3, 2]\nnums.sort(key=abs, reverse=True)\nprint(nums)", "[-10, 5, -3, 2]", "[2, -3, 5, -10]", "[-10, -3, 2, 5]", "[5, 2, -3, -10]"),
    createCodeQuestion("names = [\"Alice\", \"alice\", \"Charlie\"]\nnames.sort(key=str.lower)\nprint(names)", "['Alice', 'alice', 'Charlie']", "['Alice', 'Charlie', 'alice']", "['alice', 'Alice']", "['Charlie', 'Alice', 'alice']"),
    createCodeQuestion("fruits = [\"apple\", \"banana\", \"apple\"]\nprint(fruits.count(\"apple\"))", "2", "1", "0", "3"),
    createCodeQuestion("fruits = [\"apple\", \"banana\", \"apple\"]\nprint(fruits.index(\"banana\"))", "1", "0", "2", "ValueError"),
    createCodeQuestion("fruits = [\"apple\", \"banana\", \"apple\"]\nprint(fruits.index(\"apple\", 1))", "2", "0", "1", "The value is absent"),
    createCodeQuestion("fruits = [\"apple\", \"mango\"]\nprint(list(enumerate(fruits)))", "[(0, 'apple'), (1, 'mango')]", "[('apple', 0), ('mango', 1)]", "['apple', 'mango']", "[0, 1]"),
    createCodeQuestion("fruits = [\"apple\", \"mango\"]\nprint(list(reversed(fruits)))", "['mango', 'apple']", "['apple', 'mango']", "('mango', 'apple')", "['mango']"),
    createCodeQuestion("fruits = [\"apple\", \"mango\"]\nfor i, fruit in enumerate(fruits):\n    print(i, fruit)", "0 apple then 1 mango", "apple 0 then mango 1", "1 apple then 2 mango", "mango then apple"),
    createCodeQuestion("items = [\"a\", \"b\", \"c\"]\nfor item in reversed(items):\n    print(item)", "c then b then a", "a then b then c", "2 then 1 then 0", "['c', 'b', 'a']"),
    createCodeQuestion("items = [1, 2, 3]\nfor index in range(len(items)):\n    print(index, items[index])", "0 1 then 1 2 then 2 3", "1 0 then 2 1 then 3 2", "1 then 2 then 3", "0 then 1 then 2"),
    createCodeQuestion("values = [\"a\", \"b\"]\nprint(values[5])", "IndexError", "None", "b", "[]"),
    createCodeQuestion("values = list((1, 2))\nprint(values)", "[1, 2]", "(1, 2)", "{1, 2}", "TypeError"),
  ];

  const theoryQuestions = [
    createQuestion("Which statement best describes a Python list?", "An ordered, mutable sequence", "An unordered immutable sequence", "A key-value mapping", "A numeric-only container"),
    createQuestion("Which list property enables access such as values[0]?", "Order", "Hashability", "Immutability", "Uniqueness"),
    createQuestion("Which list property permits replacing an existing element?", "Mutability", "Lexicographic order", "Fixed length", "Hashing"),
    createQuestion("What does heterogeneous mean for a list?", "It can contain mixed data types", "It stores only unique values", "It must contain nested lists", "It is sorted automatically"),
    createQuestion("Which statement about a Python list is true?", "It can be iterated with a for loop", "It cannot contain booleans", "It has no index positions", "It must contain one type only"),
    createQuestion("Which literal creates an empty list?", "[]", "{}", "()", "set()"),
    createQuestion("Which example is a nested list?", "[[1, 2], [3, 4]]", "(1, 2, 3)", "{1, 2, 3}", "'1, 2, 3'"),
    createQuestion("What can a list store?", "Values of different types", "Only integers", "Only strings", "Only immutable values"),

    createQuestion("What does list() return when called with no argument?", "An empty list", "An empty tuple", "None", "An empty dictionary"),
    createQuestion("What does list('Ada') produce?", "['A', 'd', 'a']", "['Ada']", "'Ada'", "('A', 'd', 'a')"),
    createQuestion("What does list(range(4)) produce?", "[0, 1, 2, 3]", "[1, 2, 3, 4]", "range(4)", "[0, 1, 2, 3, 4]"),
    createQuestion("What must be passed to list(value)?", "An iterable", "A hashable object", "A callable object", "An integer only"),
    createQuestion("What happens when list(123) is evaluated?", "It raises TypeError", "It returns [123]", "It returns 123", "It returns []"),
    createQuestion("Which expression creates a list from a tuple?", "list((1, 2))", "tuple([1, 2])", "set([1, 2])", "dict([1, 2])"),
    createQuestion("What is true about list({10, 20, 30})?", "Its element order is not guaranteed from the set", "It always returns a sorted list", "It raises TypeError", "It preserves an index order from the set"),

    createQuestion("What does items[0] select?", "The first item", "The last item", "The list length", "Every item"),
    createQuestion("What does items[-1] select?", "The last item", "The first item", "The second-last item", "No item"),
    createQuestion("Which error is raised by direct access using a bad list index?", "IndexError", "KeyError", "ValueError", "AttributeError"),
    createQuestion("What is excluded in the slice values[start:end]?", "The end index", "The start index", "Every even index", "All negative indices"),
    createQuestion("What does [10, 20, 30, 40][:2] return?", "[10, 20]", "[10, 20, 30]", "[20, 30]", "[30, 40]"),
    createQuestion("What does [10, 20, 30, 40][1:] return?", "[20, 30, 40]", "[10, 20]", "[10, 20, 30]", "[40]"),
    createQuestion("What does [0, 1, 2, 3, 4][1::2] return?", "[1, 3]", "[0, 2, 4]", "[1, 2, 3, 4]", "[4, 2, 0]"),
    createQuestion("What does [1, 2, 3][::-1] return?", "[3, 2, 1]", "[1, 2, 3]", "[2, 3]", "[1, 3]"),
    createQuestion("How does out-of-range list slicing behave?", "It returns the available items without IndexError", "It always raises IndexError", "It returns None", "It clears the list"),
    createQuestion("Which slice notation means start, end, and step?", "seq[start:end:step]", "seq[start, end, step]", "seq(start:end:step)", "seq{start:end:step}"),
    createQuestion("What does ['a', 'b', 'c'][-2] return?", "'b'", "'a'", "'c'", "IndexError"),
    createQuestion("What does [0, 1, 2, 3, 4][::2] return?", "[0, 2, 4]", "[1, 3]", "[0, 1]", "[4, 2, 0]"),
    createQuestion("What does [0, 1, 2, 3, 4][3:1] return?", "[]", "[3, 2]", "[1, 2, 3]", "IndexError"),

    createQuestion("How can the second element of fruits be replaced?", "fruits[1] = 'pear'", "fruits.append('pear')", "fruits.remove(1)", "fruits.clear(1)"),
    createQuestion("What does slice assignment allow?", "Replacing multiple positions at once", "Only reading a list", "Only sorting a list", "Only copying a list"),
    createQuestion("Can slice assignment change a list's length?", "Yes, when replacement length differs", "No, list length is fixed", "Only when the list is empty", "Only for numeric lists"),
    createQuestion("What is the result after values = [1, 2, 3]; values[1] = 9?", "[1, 9, 3]", "[9, 2, 3]", "[1, 2, 9]", "[1, 2, 3, 9]"),
    createQuestion("What is the result after values = [1, 2, 3, 4]; values[1:3] = [8]?", "[1, 8, 4]", "[1, 8, 3, 4]", "[8, 1, 4]", "[1, 2, 8, 4]"),
    createQuestion("What is the result after values = [1, 2]; values[1:2] = [7, 8]?", "[1, 7, 8]", "[1, 7]", "[7, 8]", "[1, 2, 7, 8]"),
    createQuestion("Which operation updates an item without adding a new position?", "values[index] = replacement", "values.append(replacement)", "values.extend([replacement])", "values.insert(len(values), replacement)"),

    createQuestion("What does list.append(value) add?", "One item at the end", "Every item from an iterable", "One item at the beginning", "Only a unique item"),
    createQuestion("What does list.insert(index, value) do?", "Places a value at the specified index", "Replaces every matching value", "Adds values only at the end", "Sorts the list before adding"),
    createQuestion("What does list.extend(iterable) add?", "Each item from the iterable", "The iterable as one nested item", "Only the first iterable item", "A sorted copy of the iterable"),
    createQuestion("What is the result after values = [1, 2]; values.append([3, 4])?", "[1, 2, [3, 4]]", "[1, 2, 3, 4]", "[[1, 2], [3, 4]]", "[3, 4, 1, 2]"),
    createQuestion("What is the result after values = [1, 2]; values.extend([3, 4])?", "[1, 2, 3, 4]", "[1, 2, [3, 4]]", "[[1, 2], [3, 4]]", "[3, 4]"),
    createQuestion("Where does values.insert(0, 'x') place 'x'?", "At the beginning", "At the end", "After the last item only", "At a random position"),
    createQuestion("What is the result after values = ['a', 'c']; values.insert(1, 'b')?", "['a', 'b', 'c']", "['b', 'a', 'c']", "['a', 'c', 'b']", "['a', 'b']"),
    createQuestion("Which method is suitable for adding several values from another list?", "extend", "append", "remove", "clear"),
    createQuestion("Which method adds exactly one new outer-list element?", "append", "extend", "sort", "reverse"),

    createQuestion("What does list.remove(value) remove?", "The first matching value", "Every matching value", "The value at the same index", "The last matching value"),
    createQuestion("What does list.remove(value) return after a successful removal?", "None", "The removed value", "True", "The updated list"),
    createQuestion("What happens when remove(value) cannot find value?", "It raises ValueError", "It raises IndexError", "It returns None", "It appends the value"),
    createQuestion("What does list.pop() remove and return?", "The last item", "The first item", "All items", "No item"),
    createQuestion("What does list.pop(0) remove and return?", "The first item", "The last item", "The item with value zero", "Every item at an even index"),
    createQuestion("What error can pop() raise on an empty list?", "IndexError", "KeyError", "ValueError", "ZeroDivisionError"),
    createQuestion("What does del values[1] do?", "Deletes the item at index 1", "Removes the value 1", "Returns the item at index 1", "Clears the whole list"),
    createQuestion("What does del values[1:3] do?", "Deletes the selected slice", "Deletes only index 3", "Returns a copied slice", "Sorts the selected slice"),
    createQuestion("What remains after values.clear()?", "[]", "None", "The final value", "A tuple"),

    createQuestion("What does b = a create when a is a list?", "An alias to the same list object", "An independent shallow copy", "An independent deep copy", "A tuple view"),
    createQuestion("What happens after a = [1]; b = a; b.append(2)?", "Both a and b are [1, 2]", "Only b is [1, 2]", "Only a is [1, 2]", "Both lists are unchanged"),
    createQuestion("Which expression makes a shallow copy of a list?", "a[:]", "b = a", "id(a)", "a is b"),
    createQuestion("Which method makes a shallow copy of a list?", "a.copy()", "a.alias()", "a.cloneDeep()", "a.freeze()"),
    createQuestion("For a flat list, what happens after b = a[:]; b[0] = 99?", "a remains unchanged", "a changes at index 0", "Both names become invalid", "a becomes a tuple"),
    createQuestion("What do a shallow copy and original share for nested lists?", "Their inner list objects", "Their outer list object", "No objects at all", "Only their lengths"),
    createQuestion("Which function creates independent copies of nested lists?", "copy.deepcopy", "list.copy", "list.extend", "reversed"),
    createQuestion("Why does d[0][0] = 99 affect c after d = c[:]?", "The inner list is shared by the shallow copy", "The outer list is immutable", "Indexing always deep-copies values", "Slicing reverses nested lists"),

    createQuestion("What does a + b do for two lists?", "Creates a concatenated list", "Performs element-wise numeric addition", "Mutates only a", "Creates a set"),
    createQuestion("What does [1, 2] * 2 produce?", "[1, 2, 1, 2]", "[2, 4]", "[1, 2, 2, 1]", "A TypeError"),
    createQuestion("Which expression is valid list concatenation?", "a + b + [6]", "a + b + 6", "a + 6", "6 + a"),
    createQuestion("What does 'apple' in fruits test?", "Whether the value appears in the list", "Whether apple is a valid index", "Whether the list is sorted", "Whether fruit values are unique"),
    createQuestion("What does 'grape' not in fruits test?", "Whether grape is absent from the list", "Whether grape is the final item", "Whether the list is empty", "Whether grape is immutable"),
    createQuestion("What is the typical complexity of list membership testing?", "O(n)", "O(1)", "O(log n)", "O(n squared)"),
    createQuestion("Why can list membership take longer as a list grows?", "It may search items linearly", "It sorts the list before every check", "It removes duplicates first", "It converts the list into a set"),

    createQuestion("What does len([4, 5, 6]) return?", "3", "2", "6", "0"),
    createQuestion("What does min([4, 2, 7]) return?", "2", "4", "7", "A ValueError"),
    createQuestion("What does max([4, 2, 7]) return?", "7", "4", "2", "The list length, 3"),
    createQuestion("What does sum([4, 2, 7]) return?", "13", "The largest value, 7", "The list length, 3", "The product, 56"),
    createQuestion("How are strings compared by min and max?", "Lexicographically", "By string length only", "By insertion position only", "As numeric values always"),
    createQuestion("What does max(['Alice', 'Bob', 'Charlie']) compare to choose a result?", "Lexicographic character order", "The shortest name", "The earliest inserted name", "The name with most vowels"),
    createQuestion("Which built-in reports the number of elements in a list?", "len", "sum", "max", "ord"),

    createQuestion("What does values.reverse() do?", "Reverses the same list in place", "Returns a sorted new list", "Creates a tuple in reverse order", "Removes duplicate values"),
    createQuestion("What does list(reversed(values)) produce?", "A new list in reverse order", "The same list reversed in place", "A sorted list", "A list of index values"),
    createQuestion("What does sorted(values) return?", "A new sorted list", "None after sorting in place", "A reversed iterator", "A set of unique items"),
    createQuestion("What does values.sort() do?", "Sorts the existing list in place", "Returns a new sorted list", "Reverses the existing list", "Raises an error for numbers"),
    createQuestion("What does values.sort() return?", "None", "The sorted list", "A sort iterator", "True"),
    createQuestion("What does sorted(words, key=len, reverse=True) prioritize?", "Longest strings first", "Shortest strings first", "Alphabetical order only", "Original index order only"),
    createQuestion("What does values.sort(key=abs, reverse=True) use for ordering?", "Descending absolute values", "Ascending raw values", "Descending string values", "Original insertion positions"),
    createQuestion("Which key can sort names without case sensitivity?", "str.lower", "str.uppercase", "len.lower", "casefold.index"),
    createQuestion("Which operation keeps the original list unchanged?", "sorted(values)", "values.sort()", "values.reverse()", "values.clear()"),

    createQuestion("What does fruits.count('apple') return?", "The number of 'apple' occurrences", "The first 'apple' index", "The final 'apple' index", "A list without apples"),
    createQuestion("What does fruits.index('apple') return?", "The first matching index", "The number of matches", "The final matching index", "A boolean result"),
    createQuestion("What happens when list.index(value) cannot find value?", "It raises ValueError", "It raises IndexError", "It returns -1", "It returns None"),
    createQuestion("What does fruits.index('apple', 1) control?", "The index where the search begins", "The count of apples to remove", "The list position to insert apple", "The length of the result"),
    createQuestion("What does ['a', 'b', 'a'].count('a') return?", "2", "1", "3", "A ValueError"),
    createQuestion("What does ['a', 'b', 'a'].index('a') return?", "0", "1", "2", "The value 'a'"),
    createQuestion("Which method is useful for checking how many times one value appears?", "count", "index", "reverse", "clear"),

    createQuestion("Which loop iterates directly over list values?", "for fruit in fruits", "for fruit at fruits", "for fruits in fruit", "loop fruit from fruits"),
    createQuestion("Which loop provides both an index and a value?", "for i, fruit in enumerate(fruits)", "for i in fruits.index()", "for fruit in range(fruits)", "for i, fruit in reversed(enumerate)"),
    createQuestion("What does enumerate(fruits) provide during iteration?", "Index-value pairs", "Only index values", "Only list lengths", "Sorted values"),
    createQuestion("Which loop accesses items by explicit numeric index?", "for i in range(len(fruits))", "for i in fruits.values()", "for i in enumerate(len(fruits))", "for i in list(fruits, index)"),
    createQuestion("What does reversed(fruits) provide in a for loop?", "Items from last to first", "Items in sorted order", "Only even-index items", "A shallow copy"),
    createQuestion("Which pattern is preferred when both position and value are needed?", "enumerate(fruits)", "range(fruits)", "len(enumerate)", "fruits.index()"),
    createQuestion("What does this print: for item in ['x', 'y']: print(item)?", "x then y", "0 then 1", "y then x", "The list length only"),
    createQuestion("What is the first index produced by enumerate(['a', 'b']) by default?", "0", "1", "-1", "2"),
    createQuestion("What is the first value produced by reversed([1, 2, 3])?", "3", "1", "2", "The final index, 2"),
  ];

  return [...codeQuestions, ...theoryQuestions.slice(50)];
}

function validateQuestionBank(questions) {
  if (questions.length !== 100) {
    throw new Error(`Question bank must contain 100 questions; found ${questions.length}`);
  }

  const questionTexts = new Set();
  const optionSignatures = new Set();
  let codeQuestionCount = 0;

  questions.forEach((question, index) => {
    if (!question || typeof question.question !== "string" || !question.question.trim()) {
      throw new Error(`Question text is missing at index ${index}`);
    }
    if (!Array.isArray(question.options) || question.options.length !== 4) {
      throw new Error(`Question ${index + 1} must have exactly four options`);
    }
    if (!Number.isInteger(question.correctIndex) || question.correctIndex < 0 || question.correctIndex > 3) {
      throw new Error(`Question ${index + 1} has an invalid correct option index`);
    }

    if (question.question.includes("\n\n")) {
      codeQuestionCount += 1;
      const codeLineCount = question.question.split("\n\n")[1].split("\n").length;
      if (codeLineCount < 2 || codeLineCount > 5) {
        throw new Error(`Code question ${index + 1} must contain 2 to 5 lines`);
      }
    }

    const normalizedQuestion = normalize(question.question);
    if (questionTexts.has(normalizedQuestion)) {
      throw new Error(`Duplicate question detected: ${question.question}`);
    }
    questionTexts.add(normalizedQuestion);

    const normalizedOptions = question.options.map((option) => {
      if (typeof option !== "string" || !option.trim()) {
        throw new Error(`Question ${index + 1} has an invalid option`);
      }
      return normalize(option);
    });
    if (new Set(normalizedOptions).size !== 4) {
      throw new Error(`Question ${index + 1} contains duplicate options`);
    }

    const signature = normalizedOptions.slice().sort().join("|");
    if (optionSignatures.has(signature)) {
      throw new Error(`Question ${index + 1} duplicates an option set`);
    }
    optionSignatures.add(signature);
  });

  if (codeQuestionCount !== 50) {
    throw new Error(`Question bank must contain 50 code questions; found ${codeQuestionCount}`);
  }
}

function verifyGeneratedQuestions(form, questions, pointsPerQuestion) {
  const items = form
    .getItems(FormApp.ItemType.MULTIPLE_CHOICE)
    .map((item) => item.asMultipleChoiceItem());
  if (items.length !== questions.length) {
    throw new Error(`Generated ${items.length} questions; expected ${questions.length}`);
  }

  let totalPoints = 0;
  items.forEach((item, index) => {
    const [questionTitle, code] = questions[index].question.split("\n\n");
    if (item.getTitle() !== `${index + 1}. ${questionTitle}`) {
      throw new Error(`Question ${index + 1} was not saved correctly`);
    }
    if (item.getHelpText() !== (code || "")) {
      throw new Error(`Question ${index + 1} code snippet was not saved correctly`);
    }
    if (item.getChoices().filter((choice) => choice.isCorrectAnswer()).length !== 1) {
      throw new Error(`Question ${index + 1} must have exactly one correct option`);
    }
    if (item.getPoints() !== pointsPerQuestion) {
      throw new Error(`Question ${index + 1} must be worth ${pointsPerQuestion} point`);
    }
    totalPoints += item.getPoints();
  });

  if (totalPoints !== 100) {
    throw new Error(`Quiz must total 100 points; found ${totalPoints}`);
  }
}

function normalize(value) {
  return value.trim().toLowerCase().replace(/\s+/g, " ");
}

function fisherYatesShuffle(values) {
  for (let index = values.length - 1; index > 0; index -= 1) {
    const randomIndex = Math.floor(Math.random() * (index + 1));
    [values[index], values[randomIndex]] = [values[randomIndex], values[index]];
  }
}
