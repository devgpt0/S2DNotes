/**
 * Google Apps Script: Generate the Complete Software Engineering Week 3 Python
 * Fundamentals Test.
 *
 * Coverage includes the Python fundamentals notes except:
 * - file_io_pathlib_serialization_mastery.md
 * - iterators_generators_context_managers.md
 * - modern_packaging_pyproject_wheels.md
 * - python_fundamentals_mastery_roadmap.md
 *
 * The bank contains 25 theory questions and 75 code-snippet questions.
 */

function createBatch1CseWeek3TestForm() {
  createBatch1Week3PythonFundamentalsTest();
}

function createBatch1Week3PythonFundamentalsTest() {
  const config = {
    title: "Batch 1 Complete Software Engineering Week 3 Python Fundamentals Test",
    description: `Instructions:
- Total Questions: 100
- Each question carries 1 mark.
- All questions are mandatory.
- No negative marking.
- Submit the form only after answering all questions.
- Responses cannot be edited after submission.`,
    pointsPerQuestion: 1,
  };

  const questions = buildQuestionBank();
  validateQuestionBank(questions);
  const answerSlots = buildAnswerSlotSequence(questions.length);

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

  const courseInterestItem = form.addListItem();
  courseInterestItem
    .setTitle("Are you interesed for the bootcoding course ?")
    .setRequired(true)
    .setChoices(
      ["Very Interested", "Interested", "Not Interested"].map((choice) =>
        courseInterestItem.createChoice(choice),
      ),
    );

  const instructorFeedbackItem = form.addListItem();
  instructorFeedbackItem
    .setTitle("Instructor Feedback")
    .setRequired(true)
    .setChoices(
      ["Excellent", "Good", "Moderate", "Not Good"].map((choice) =>
        instructorFeedbackItem.createChoice(choice),
      ),
    );

  const departmentItem = form.addListItem();
  departmentItem.setTitle("Department").setRequired(true);
  departmentItem.setChoices(
    [
      "Computer Science",
      "Artifical Intelligence and Data Science",
      "Information Technology",
      "Electronics and Communication",
      "Electrical Engineering",
      "Mechanical Engineering",
      "Civil Engineering",
      "Other",
    ].map((department) => departmentItem.createChoice(department)),
  );

  const passOutYearItem = form.addListItem();
  passOutYearItem.setTitle("Student Pass-out Year").setRequired(true);
  passOutYearItem.setChoices(
    ["2026", "2027", "2028", "2029", "2030"].map((year) =>
      passOutYearItem.createChoice(year),
    ),
  );

  form.addPageBreakItem().setTitle("Complete Software Engineering - Week 3 Test");

  const generatedItems = [];
  questions.forEach((question, index) => {
    const item = form.addMultipleChoiceItem();
    const [questionTitle, code] = question.question.split("\n\n");
    const choices = question.options.map((option, optionIndex) => ({
      option,
      isCorrect: optionIndex === question.correctIndex,
    }));
    const arrangedChoices = arrangeChoicesForAnswerSlot(choices, answerSlots[index]);
    const title = `${index + 1}. ${questionTitle}`;

    writeQuestionContent(item, title, code || "", arrangedChoices);
    generatedItems.push({ item, title, code: code || "", choices: arrangedChoices });
  });

  applyQuestionContentWithRetry(generatedItems);
  applyPointsWithRetry(
    generatedItems.map(({ item }) => item),
    config.pointsPerQuestion,
  );
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
    "What is printed or raised?\n\n" + code,
    correctOption,
    ...incorrectOptions,
  );
}

function validateQuestionBank(questions) {
  if (questions.length !== 100) {
    throw new Error(`Question bank must contain 100 questions; found ${questions.length}`);
  }

  const questionTexts = new Set();
  let codeQuestionCount = 0;

  questions.forEach((question, index) => {
    if (!question || typeof question.question !== "string" || !question.question.trim()) {
      throw new Error(`Question text is missing at index ${index}`);
    }
    if (!Array.isArray(question.options) || question.options.length !== 4) {
      throw new Error(`Question ${index + 1} must have exactly four options`);
    }
    if (
      !Number.isInteger(question.correctIndex) ||
      question.correctIndex < 0 ||
      question.correctIndex > 3
    ) {
      throw new Error(`Question ${index + 1} has an invalid correct answer index`);
    }

    const normalizedQuestion = normalize(question.question);
    if (questionTexts.has(normalizedQuestion)) {
      throw new Error(`Duplicate question detected: ${question.question}`);
    }
    questionTexts.add(normalizedQuestion);

    const optionTexts = new Set();
    question.options.forEach((option) => {
      if (typeof option !== "string" || !option.trim()) {
        throw new Error(`Question ${index + 1} has an invalid option`);
      }
      const normalizedOption = normalize(option);
      if (optionTexts.has(normalizedOption)) {
        throw new Error(`Repeated option in question ${index + 1}: ${option}`);
      }
      optionTexts.add(normalizedOption);
    });

    if (question.question.includes("\n\n")) {
      codeQuestionCount += 1;
      const [title, code] = question.question.split("\n\n");
      if (!title.trim() || !code.trim()) {
        throw new Error(`Code question ${index + 1} is missing a title or description`);
      }
      const lineCount = code.split("\n").length;
      if (lineCount < 2 || lineCount > 12) {
        throw new Error(`Code question ${index + 1} must contain 2 to 12 lines`);
      }
    }
  });

  if (codeQuestionCount !== 75) {
    throw new Error(`Question bank must contain 75 code questions; found ${codeQuestionCount}`);
  }
}

function verifyGeneratedQuestions(form, questions, pointsPerQuestion) {
  const items = form
    .getItems(FormApp.ItemType.MULTIPLE_CHOICE)
    .map((item) => item.asMultipleChoiceItem());
  if (items.length !== questions.length) {
    throw new Error(`Generated ${items.length} MCQs; expected ${questions.length}`);
  }

  let totalPoints = 0;
  const correctPositions = [];
  items.forEach((item, index) => {
    const [questionTitle, code] = questions[index].question.split("\n\n");
    if (item.getTitle() !== `${index + 1}. ${questionTitle}`) {
      throw new Error(`Question ${index + 1} title was not saved correctly`);
    }
    if (item.getHelpText() !== (code || "")) {
      throw new Error(`Question ${index + 1} description was not saved correctly`);
    }

    const choices = item.getChoices();
    if (choices.length !== 4) {
      throw new Error(`Question ${index + 1} must have four rendered options`);
    }
    if (choices.filter((choice) => choice.isCorrectAnswer()).length !== 1) {
      throw new Error(`Question ${index + 1} must have exactly one correct choice`);
    }

    const renderedOptions = new Set();
    choices.forEach((choice) => {
      const normalizedOption = normalize(choice.getValue());
      if (renderedOptions.has(normalizedOption)) {
        throw new Error(`Question ${index + 1} has repeated rendered options`);
      }
      renderedOptions.add(normalizedOption);
    });

    const expectedOptions = new Set(
      questions[index].options.map((option) => normalize(option)),
    );
    if (
      expectedOptions.size !== renderedOptions.size ||
      [...expectedOptions].some((option) => !renderedOptions.has(option))
    ) {
      throw new Error(`Question ${index + 1} options were not saved correctly`);
    }

    const correctChoice = choices.find((choice) => choice.isCorrectAnswer());
    const expectedCorrectOption = normalize(
      questions[index].options[questions[index].correctIndex],
    );
    if (normalize(correctChoice.getValue()) !== expectedCorrectOption) {
      throw new Error(`Question ${index + 1} correct answer was not saved correctly`);
    }

    correctPositions.push(choices.findIndex((choice) => choice.isCorrectAnswer()));
    if (item.getPoints() !== pointsPerQuestion) {
      throw new Error(`Question ${index + 1} has incorrect points`);
    }
    totalPoints += item.getPoints();
  });

  if (totalPoints !== 100) {
    throw new Error(`Test must total 100 points; found ${totalPoints}`);
  }

  const positionCounts = [0, 0, 0, 0];
  correctPositions.forEach((position, index) => {
    positionCounts[position] += 1;
    if (index > 0 && position === correctPositions[index - 1]) {
      throw new Error(`Correct answer position repeated at question ${index + 1}`);
    }
  });
  if (positionCounts.some((count) => count !== 25)) {
    throw new Error(
      `Correct answer positions must be balanced 25 each; found ${JSON.stringify(positionCounts)}`,
    );
  }
}

function applyPointsWithRetry(items, pointsPerQuestion) {
  for (let attempt = 0; attempt < 3; attempt += 1) {
    items.forEach((item) => item.setPoints(pointsPerQuestion));
    Utilities.sleep(500);
    if (items.every((item) => item.getPoints() === pointsPerQuestion)) {
      return;
    }
  }

  const failedIndex = items.findIndex(
    (item) => item.getPoints() !== pointsPerQuestion,
  );
  throw new Error(`Question ${failedIndex + 1} could not be assigned ${pointsPerQuestion} point`);
}

function writeQuestionContent(item, title, code, choices) {
  item.setTitle(title);
  if (code) {
    item.setHelpText(code);
  }
  item.setChoices(
    choices.map(({ option, isCorrect }) =>
      item.createChoice(String(option), Boolean(isCorrect)),
    ),
  );
  item.setRequired(true);
}

function applyQuestionContentWithRetry(questionRecords) {
  for (let attempt = 0; attempt < 3; attempt += 1) {
    questionRecords.forEach(({ item, title, code, choices }) =>
      writeQuestionContent(item, title, code, choices),
    );
    Utilities.sleep(500);

    const incompleteIndex = questionRecords.findIndex(({ item, title, code }) => {
      const renderedChoices = item.getChoices();
      return (
        item.getTitle() !== title ||
        item.getHelpText() !== code ||
        renderedChoices.length !== 4 ||
        renderedChoices.some((choice) => !String(choice.getValue()).trim())
      );
    });
    if (incompleteIndex === -1) {
      return;
    }
  }

  const incompleteIndex = questionRecords.findIndex(({ item, title, code }) => {
    const renderedChoices = item.getChoices();
    return (
      item.getTitle() !== title ||
      item.getHelpText() !== code ||
      renderedChoices.length !== 4 ||
      renderedChoices.some((choice) => !String(choice.getValue()).trim())
    );
  });
  throw new Error(`Question ${incompleteIndex + 1} content was not saved correctly`);
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

function arrangeChoicesForAnswerSlot(choices, answerSlot) {
  const correctChoices = choices.filter((choice) => choice.isCorrect);
  const incorrectChoices = choices.filter((choice) => !choice.isCorrect);
  if (correctChoices.length !== 1 || answerSlot < 0 || answerSlot > 3) {
    throw new Error("Each question must have one correct answer and a valid answer slot");
  }
  fisherYatesShuffle(incorrectChoices);
  incorrectChoices.splice(answerSlot, 0, correctChoices[0]);
  return incorrectChoices;
}

function buildAnswerSlotSequence(questionCount) {
  if (questionCount % 4 !== 0) {
    throw new Error("Question count must be divisible by four for balanced answer positions");
  }

  const remainingCounts = [
    questionCount / 4,
    questionCount / 4,
    questionCount / 4,
    questionCount / 4,
  ];
  const slots = [];
  let previousSlot = -1;

  for (let position = 0; position < questionCount; position += 1) {
    const candidates = [];
    const remainingAfterChoice = questionCount - position - 1;
    for (let slot = 0; slot < remainingCounts.length; slot += 1) {
      if (remainingCounts[slot] === 0 || slot === previousSlot) {
        continue;
      }

      remainingCounts[slot] -= 1;
      const largestRemainingCount = Math.max(...remainingCounts);
      const canFinishWithoutAdjacentRepeats =
        largestRemainingCount <= Math.ceil(remainingAfterChoice / 2);
      remainingCounts[slot] += 1;

      if (canFinishWithoutAdjacentRepeats) {
        candidates.push(slot);
      }
    }

    if (candidates.length === 0) {
      throw new Error("Could not create a balanced answer sequence");
    }
    const selectedSlot = candidates[Math.floor(Math.random() * candidates.length)];
    slots.push(selectedSlot);
    remainingCounts[selectedSlot] -= 1;
    previousSlot = selectedSlot;
  }
  return slots;
}

function buildQuestionBank() {
  return [
    // 25 theory questions.
    createQuestion("What is the most precise description of a Python variable?", "A name bound to an object", "A fixed typed memory box", "A value that owns its name", "A compiler-only placeholder"),
    createQuestion("Why can a tuple containing a list change its visible contents?", "Tuple immutability is shallow and the nested list can mutate", "Tuple assignment recursively freezes every member", "List members are copied whenever indexed", "Tuple indexing replaces the tuple"),
    createQuestion("Why is a tuple containing a list not hashable?", "Its mutable member prevents a stable hash", "Tuples can never be hashable", "Lists become immutable inside tuples", "Hashing only rejects strings"),
    createQuestion("What is the key difference between // and /?", "// performs floor division while / performs true division", "// always truncates toward zero while / returns an integer", "// is exponentiation while / is modulo", "// compares operands while / assigns them"),
    createQuestion("What does a and b return when a is falsy?", "The first falsy operand without evaluating later operands", "Always the Boolean value False", "The last truthy operand", "A newly allocated Boolean wrapper"),
    createQuestion("What makes a comparison chain different from manually repeated comparisons?", "The shared middle expression is evaluated once", "Every comparison is evaluated from right to left", "It compares object identities instead of values", "It automatically converts every operand to bool"),
    createQuestion("When does a loop else block execute?", "When the loop finishes without break", "Whenever the loop body runs at least once", "Only when a continue statement runs", "Only when an exception is raised"),
    createQuestion("What does a match case guard add?", "A boolean condition that must also succeed", "A second pattern-matching syntax", "An automatic exception handler", "A conversion from case to class"),
    createQuestion("Why is a mutable default parameter dangerous?", "The same default object persists across calls", "Python copies it only on the first call", "Mutable defaults are converted to tuples", "The parameter becomes global"),
    createQuestion("What does / in a function parameter list enforce?", "Parameters before it are positional-only", "Parameters after it are positional-only", "Every parameter must be keyword-only", "It marks the return type"),
    createQuestion("What is the late-binding closure trap?", "Closures read a shared loop variable when called later", "Closures copy every local value immediately", "Closures cannot reference enclosing names", "Closures always resolve names globally"),
    createQuestion("What is required for safe recursion?", "A reachable base case that stops recursive calls", "A mutable global counter only", "A keyword-only parameter", "An exception in every recursive call"),
    createQuestion("What do Python type hints normally do at runtime?", "Provide metadata without enforcing the hinted type", "Convert all values to the hinted type", "Reject every incompatible argument automatically", "Replace the function's actual return value"),
    createQuestion("What is structural typing through a Protocol?", "Compatibility based on required behavior rather than inheritance", "A requirement that every class share a base class", "Runtime conversion of objects to dictionaries", "A restriction that prevents duck typing"),
    createQuestion("Why does except Exception not catch every possible failure?", "Some exceptions such as BaseException subclasses are outside Exception", "Exception only catches syntax errors", "Exception catches warnings but not errors", "Python has no exception hierarchy"),
    createQuestion("What is a major control-flow property of finally?", "It runs during normal completion and most exception paths", "It runs only when an except block matches", "It is skipped whenever return is used", "It catches exceptions without handling them"),
    createQuestion("What does raise NewError() from old_error express?", "Explicit exception chaining with old_error as the cause", "Suppression of both exceptions", "Conversion of an exception into a warning", "A retry of the original statement"),
    createQuestion("What is the main risk of catching Exception broadly?", "It can hide unrelated programming errors", "It makes all exceptions syntax errors", "It disables finally blocks", "It prevents custom exceptions from existing"),
    createQuestion("What happens on the first import of a module?", "Its top-level code executes and the module is cached", "Only its function bodies execute", "It is always executed once per import statement", "Its names are copied into every module"),
    createQuestion("What is the purpose of if __name__ == '__main__':?", "To run code only when the file is executed as the entry script", "To make all imports relative", "To force a module to reload", "To mark every function as private"),
    createQuestion("What does a leading dot in from .pricing import total mean?", "Import relative to the current package", "Import from the filesystem root", "Import a hidden built-in module", "Import only a compiled wheel"),
    createQuestion("What does LEGB describe?", "The order of local, enclosing, global, and built-in lookup", "The order of list, expression, generator, and bytecode execution", "The four Python collection types", "The stages of exception formatting"),
    createQuestion("Why is memory size not a portable Python-language guarantee?", "Object layout and sizes are implementation-dependent", "Every Python object has a fixed one-byte header", "Garbage collection fixes all object sizes", "Type hints determine object memory exactly"),
    createQuestion("What is the difference between bytes.decode and str.encode?", "decode turns bytes into text; encode turns text into bytes", "decode turns text into bytes; encode turns bytes into text", "Both always return strings", "Both always return bytearray objects"),
    createQuestion("What does Final communicate?", "A static intent that a name should not be reassigned", "A runtime lock that makes the object immutable", "A request to garbage-collect the object", "A declaration that the value must be a float"),

    // 75 code-snippet questions.
    createCodeQuestion("a = [1, 2]\nb = a\nb.append(3)\na = [9]\nprint(b, a, b is a)", "Output: [1, 2, 3] [9] False", "Output: [1, 2] [9] False", "Output: [1, 2, 3] [1, 2, 3] True", "Output: [9] [9] True"),
    createCodeQuestion("x = [[1], [2]]\ny = x.copy()\ny[0].append(8)\ny.append([9])\nprint(x, y)", "Output: [[1, 8], [2]] [[1, 8], [2], [9]]", "Output: [[1], [2]] [[1], [2], [9]]", "Output: [[1, 8], [2], [9]] [[1, 8], [2], [9]]", "Output: [[1], [2, 8]] [[1], [2], [9]]"),
    createCodeQuestion("import copy\na = [[1], [2]]\nb = copy.deepcopy(a)\nb[0].append(7)\nprint(a, b, a is b)", "Output: [[1], [2]] [[1, 7], [2]] False", "Output: [[1, 7], [2]] [[1, 7], [2]] True", "Output: [[1], [2, 7]] [[1], [2, 7]] False", "Output: [[1, 7], [2]] [[1], [2]] True"),
    createCodeQuestion("items = [1]\nalias = items\nitems += [2]\nprint(items is alias, alias)", "Output: True [1, 2]", "Output: False [1]", "Output: True [1]", "Output: False [1, 2]"),
    createCodeQuestion("first, *middle, last = [10, 20, 30, 40]\nmiddle.append(99)\nprint(first, middle, last)", "Output: 10 [20, 30, 99] 40", "Output: 10 [20, 30] 99", "Output: [10] [20, 30, 40, 99] []", "Output: 20 [10, 30, 99] 40"),
    createCodeQuestion("def change(value):\n    value.append(4)\n    value = [8]\n    return value\ndata = [1]\nprint(data, change(data))", "Output: [1, 4] [8]", "Output: [8] [1, 4]", "Output: [1] [1, 4, 8]", "Output: [1, 4] None"),
    createCodeQuestion("def add(value, bucket=[]):\n    bucket.append(value)\n    return bucket\nprint(add(1))\nprint(add(2))", "Output: [1] then [1, 2]", "Output: [1] then [2]", "Output: [1, 2] then [1, 2]", "Output: None then None"),
    createCodeQuestion("functions = []\nfor i in range(3):\n    functions.append(lambda: i)\nprint([fn() for fn in functions])", "Output: [2, 2, 2]", "Output: [0, 1, 2]", "Output: [3, 3, 3]", "Output: [0, 0, 0]"),
    createCodeQuestion("functions = []\nfor i in range(3):\n    functions.append(lambda i=i: i)\nprint([fn() for fn in functions])", "Output: [0, 1, 2]", "Output: [2, 2, 2]", "Output: [1, 2, 3]", "Output: [0, 0, 0]"),
    createCodeQuestion("def outer():\n    count = 0\n    def inner():\n        nonlocal count\n        count += 1\n        return count\n    return inner\nf = outer()\nprint(f(), f())", "Output: 1 2", "Output: 0 0", "Output: 1 1", "Output: UnboundLocalError"),
    createCodeQuestion("def show(a, /, b, *, c):\n    return a + b + c\nprint(show(1, 2, c=3))", "Output: 6", "Output: TypeError: c must be positional", "Output: TypeError: a must be keyword", "Output: 123"),
    createCodeQuestion("def collect(*args, **kwargs):\n    return args, kwargs\nprint(collect(1, 2, x=3))", "Output: ((1, 2), {'x': 3})", "Output: ([1, 2], {'x': 3})", "Output: ((1, 2, 3), {})", "Output: (1, 2, 'x', 3)"),
    createCodeQuestion("def f():\n    try:\n        return 'try'\n    finally:\n        return 'finally'\nprint(f())", "Output: finally", "Output: try", "Output: None", "Output: RuntimeError"),
    createCodeQuestion("def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)\nprint(factorial(5))", "Output: 120", "Output: 25", "Output: 24", "Output: RecursionError"),
    createCodeQuestion("print(7 / 2)\nprint(7 // 2, -7 // 2)\nprint(-10 % 3)", "Output: 3.5 then 3 -4 then 2", "Output: 3 then 3 -3 then 1", "Output: 3.5 then 3 -3 then -1", "Output: 3.0 then 4 -4 then 2"),
    createCodeQuestion("print(-3**2, (-3)**2)\nprint(2**3**2)", "Output: -9 9 then 512", "Output: 9 9 then 64", "Output: -9 -9 then 64", "Output: 9 -9 then 512"),
    createCodeQuestion("result = (n := 4) * 2\nprint(result, n)", "Output: 8 4", "Output: 8 2", "Output: 4 8", "Output: SyntaxError"),
    createCodeQuestion("print('' and 'later')\nprint('ready' or 'later')\nprint(0 or 5 and 6)", "Output: blank line, ready, 6", "Output: False, True, True", "Output: later, later, 0", "Output: blank line, later, 5"),
    createCodeQuestion("left = {1, 2, 3}\nright = {3, 4}\nprint(sorted(left & right))\nprint(sorted(left ^ right))", "Output: [3] then [1, 2, 4]", "Output: [1, 2, 3, 4] then [3]", "Output: [3] then [1, 2, 3, 4]", "Output: [] then [1, 2, 4]"),
    createCodeQuestion("value = 6\nprint(value & 3, value | 3, value ^ 3)\nprint(~value)", "Output: 2 7 5 then -7", "Output: 0 9 3 then 6", "Output: 3 6 2 then 7", "Output: 2 3 7 then -6"),
    createCodeQuestion("print(3 << 2)\nprint(20 >> 2)\nprint(-5 >> 1)", "Output: 12 then 5 then -3", "Output: 6 then 10 then -2", "Output: 12 then 5 then -2", "Output: 9 then 5 then 3"),
    createCodeQuestion("raw = 'caf\\u00e9'\ndata = raw.encode('utf-8')\nprint(type(data).__name__, data.decode('utf-8'))", "Output: bytes café", "Output: str b'caf\\xc3\\xa9'", "Output: bytearray café", "Output: bytes caf?"),
    createCodeQuestion("items = [0, '', [], [1]]\nprint([bool(item) for item in items])\nprint(any(items), all(items))", "Output: [False, False, False, True] then True False", "Output: [True, True, True, True] then True True", "Output: [False, False, True, True] then False True", "Output: [0, '', [], [1]] then 1 0"),
    createCodeQuestion("names = ['a', 'b', 'c']\nfor index, name in enumerate(names, start=1):\n    print(index, name)", "Output: 1 a; 2 b; 3 c", "Output: 0 a; 1 b; 2 c", "Output: a 1; b 2; c 3", "Output: 1 b; 2 c; 3 a"),
    createCodeQuestion("left = [1, 2, 3]\nright = ['a', 'b']\nprint(list(zip(left, right)))", "Output: [(1, 'a'), (2, 'b')]", "Output: [(1, 'a'), (2, 'b'), (3, None)]", "Output: [(1, 2, 3), ('a', 'b')]", "Output: [(1, 'a'), (2, 'b'), (None, 3)]"),
    createCodeQuestion("n = 0\nwhile n < 5:\n    n += 1\n    if n == 3:\n        continue\n    print(n)", "Output: 1 2 4 5", "Output: 1 2 3 4 5", "Output: 0 1 2 4", "Output: 1 3 4 5"),
    createCodeQuestion("for value in [1, 2, 3]:\n    if value == 4:\n        break\nelse:\n    print('completed')", "Output: completed", "Output: no output because else needs break", "Output: 4", "Output: SyntaxError"),
    createCodeQuestion("pairs = []\nfor row in range(2):\n    for column in range(3):\n        pairs.append((row, column))\nprint(pairs)", "Output: [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]", "Output: [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)]", "Output: [(0, 1), (0, 2), (1, 0), (1, 1)]", "Output: [(2, 3)]"),
    createCodeQuestion("def classify(value):\n    match value:\n        case int(n) if n > 0:\n            return 'positive'\n        case int():\n            return 'integer'\n        case _:\n            return 'other'\nprint(classify(-2), classify(3), classify('3'))", "Output: integer positive other", "Output: positive positive other", "Output: integer integer other", "Output: other positive integer"),
    createCodeQuestion("values = [2, 4, 6]\nprint(any(value % 2 for value in values))\nprint(all(value % 2 == 0 for value in values))", "Output: False then True", "Output: True then True", "Output: False then False", "Output: True then False"),
    createCodeQuestion("for value in [1, 2]:\n    pass\nprint('after')", "Output: after", "Output: 1 2 after", "Output: no output", "Output: IndentationError"),
    createCodeQuestion("try:\n    value = int('x')\nexcept ValueError:\n    print('bad')\nelse:\n    print('good')\nfinally:\n    print('done')", "Output: bad then done", "Output: good then done", "Output: bad only", "Output: ValueError traceback only"),
    createCodeQuestion("try:\n    {}['missing']\nexcept (KeyError, IndexError) as error:\n    print(type(error).__name__)", "Output: KeyError", "Output: IndexError", "Output: LookupError", "Output: TypeError"),
    createCodeQuestion("def convert(value):\n    try:\n        return int(value)\n    except ValueError as error:\n        raise TypeError('bad input') from error\ntry:\n    convert('x')\nexcept Exception as error:\n    print(type(error).__name__, type(error.__cause__).__name__)", "Output: TypeError ValueError", "Output: ValueError TypeError", "Output: TypeError NoneType", "Output: Exception ValueError"),
    createCodeQuestion("class ShortInputError(ValueError):\n    pass\ndef check(text):\n    if len(text) < 3:\n        raise ShortInputError('short')\n    return 'ok'\ntry:\n    check('x')\nexcept ValueError as error:\n    print(type(error).__name__, str(error))", "Output: ShortInputError short", "Output: ValueError short", "Output: TypeError short", "Output: short ShortInputError"),
    createCodeQuestion("try:\n    1 / 0\nexcept ZeroDivisionError:\n    print('handled')\n    raise", "Output: handled, then ZeroDivisionError propagates", "Output: ZeroDivisionError without handled", "Output: handled only", "Output: ValueError propagates"),
    createCodeQuestion("try:\n    [1][4]\nexcept LookupError:\n    print('lookup')\nexcept IndexError:\n    print('index')", "Output: lookup", "Output: index", "Output: both lookup and index", "Output: no output"),
    createCodeQuestion("def require(value):\n    assert value > 0, 'non-positive'\n    return value\ntry:\n    require(0)\nexcept AssertionError as error:\n    print(type(error).__name__, str(error))", "Output: AssertionError non-positive", "Output: ValueError non-positive", "Output: AssertionError 0", "Output: no output"),
    createCodeQuestion("namespace = {'__name__': '__main__'}\nexec(\"if __name__ == '__main__':\\n    print('run')\", namespace)", "Output: run", "Output: no output", "Output: NameError", "Output: __main__"),
    createCodeQuestion("import sys, types\nmodule = types.ModuleType('cached_demo')\nmodule.count = 7\nsys.modules['cached_demo'] = module\nimport cached_demo\nprint(cached_demo.count)", "Output: 7", "Output: ModuleNotFoundError", "Output: 0", "Output: cached_demo"),
    createCodeQuestion("import importlib\nmodule = importlib.import_module('math')\nprint(module.sqrt(81), module.__name__)", "Output: 9.0 math", "Output: 81 math", "Output: 9 math.sqrt", "Output: ModuleNotFoundError"),
    createCodeQuestion("import sys, types\nmodule = types.ModuleType('named_demo')\nmodule.value = 4\nsys.modules['named_demo'] = module\nprint(named_demo.value)", "Output: NameError", "Output: 4", "Output: ModuleNotFoundError", "Output: AttributeError"),
    createCodeQuestion("source = \"value = 3\\nprint(__name__)\"\nnamespace = {'__name__': 'demo_module'}\nexec(source, namespace)\nprint(namespace['value'])", "Output: demo_module then 3", "Output: __main__ then 3", "Output: demo_module then value", "Output: 3 then demo_module"),
    createCodeQuestion("from typing import get_type_hints\ndef add(x: int, y: int) -> int:\n    return x + y\nprint(add('a', 'b'))\nprint(get_type_hints(add)['return'].__name__)", "Output: ab then int", "Output: TypeError then int", "Output: ab then str", "Output: 2 then int"),
    createCodeQuestion("from typing import TypedDict\nclass User(TypedDict):\n    name: str\nuser = User(name='Ana')\nprint(type(user).__name__, user['name'])", "Output: dict Ana", "Output: User Ana", "Output: TypedDict Ana", "Output: dict name"),
    createCodeQuestion("from dataclasses import dataclass\n@dataclass(frozen=True)\nclass Point:\n    x: int\np = Point(2)\nprint(p)\ntry:\n    p.x = 3\nexcept Exception as error:\n    print(type(error).__name__)", "Output: Point(x=2) then FrozenInstanceError", "Output: Point(x=2) then TypeError", "Output: Point(2) then AttributeError", "Output: Point(x=3) only"),
    createCodeQuestion("from typing import Protocol\nclass Named(Protocol):\n    name: str\nclass User:\n    name = 'Ana'\ndef greet(value: Named):\n    return value.name\nprint(greet(User()))", "Output: Ana", "Output: Named", "Output: TypeError", "Output: User"),
    createCodeQuestion("from typing import Final\nLIMIT: Final = 3\nLIMIT = 4\nprint(LIMIT)", "Output: 4", "Output: TypeError", "Output: 3", "Output: FinalError"),
    createCodeQuestion("from typing import TypeVar\nT = TypeVar('T')\ndef first(value: list[T]) -> T:\n    return value[0]\nprint(first([1, 2]), first(['a', 'b']))", "Output: 1 a", "Output: 1 b", "Output: TypeError", "Output: [1, 2] ['a', 'b']"),
    createCodeQuestion("print(type(3).__name__)\nprint(isinstance(True, int))\nprint(isinstance(True, bool))", "Output: int then True then True", "Output: bool then False then True", "Output: int then False then True", "Output: bool then True then False"),
    createCodeQuestion("print(int('101', 2))\nprint(int('ff', 16))\nprint(int(3.9))", "Output: 5 then 255 then 3", "Output: 101 then 16 then 4", "Output: 5 then 15 then 3", "Output: ValueError then 255 then 3"),
    createCodeQuestion("print(float(5), str(5), bool([]), bool([0]))\nprint(ord('A'), chr(66))", "Output: 5.0 5 False True then 65 B", "Output: 5 5 False False then 65 A", "Output: 5.0 '5' True False then A 66", "Output: TypeError"),
    createCodeQuestion("print(hex(31), bin(5), oct(9))\nprint(int('0b101', 0))", "Output: 0x1f 0b101 0o11 then 5", "Output: 31 5 9 then 0", "Output: 0x1f 101 11 then 101", "Output: ValueError"),
    createCodeQuestion("value = 257\nother = int('257')\nprint(value == other)\nprint(value is other)", "Output: True then False", "Output: False then False", "Output: True then True", "Output: False then True"),
    createCodeQuestion("raw = bytearray(b'abc')\nraw[0] = 65\nprint(raw, bytes(raw))", "Output: bytearray(b'Abc') b'Abc'", "Output: b'abc' bytearray(b'Abc')", "Output: bytearray(b'Abc') b'Abd'", "Output: TypeError"),
    createCodeQuestion("def outer():\n    value = 'enclosing'\n    def inner():\n        return value\n    return inner\nfn = outer()\nprint(fn())", "Output: enclosing", "Output: global", "Output: None", "Output: NameError"),
    createCodeQuestion("value = 'global'\ndef show():\n    print(value)\nshow()", "Output: global", "Output: local", "Output: None", "Output: UnboundLocalError"),
    createCodeQuestion("value = 'global'\ndef show():\n    print(value)\n    value = 'local'\ntry:\n    show()\nexcept Exception as error:\n    print(type(error).__name__)", "Output: UnboundLocalError", "Output: global then local", "Output: NameError", "Output: local"),
    createCodeQuestion("events = []\ndef mark(name):\n    events.append(name)\n    return name\nresult = mark('left') + mark('right')\nprint(events, result)", "Output: ['left', 'right'] leftright", "Output: ['right', 'left'] rightleft", "Output: ['left', 'right'] left right", "Output: NameError"),
    createCodeQuestion("class Example:\n    value = 2\n    print('class body', value)\nprint(Example.value)", "Output: class body 2 then 2", "Output: 2 then class body 2", "Output: no output then 2", "Output: NameError"),
    createCodeQuestion("def decorator(fn):\n    print('decorate')\n    return fn\n@decorator\ndef task():\n    print('call')\ntask()", "Output: decorate then call", "Output: call then decorate", "Output: decorate only", "Output: call only"),
    createCodeQuestion("import asyncio\nasync def value():\n    return 7\nprint(asyncio.run(value()))", "Output: 7", "Output: coroutine object representation", "Output: None", "Output: RuntimeError"),
    createCodeQuestion("import threading\nevent = threading.Event()\nresult = []\ndef worker():\n    result.append('worker')\n    event.set()\nt = threading.Thread(target=worker)\nt.start()\nevent.wait()\nt.join()\nprint(result)", "Output: ['worker']", "Output: []", "Output: ['main', 'worker']", "Output: RuntimeError"),
    createCodeQuestion("import subprocess, sys\ncompleted = subprocess.run([sys.executable, '-c', 'print(4)'], capture_output=True, text=True, check=True)\nprint(completed.stdout.strip(), completed.returncode)", "Output: 4 0", "Output: 4 1", "Output: b'4\\n' 0", "Output: CalledProcessError"),
    createCodeQuestion("import weakref\nclass Item: pass\nobj = Item()\nreference = weakref.ref(obj)\nprint(reference() is obj)\ndel obj\nprint(reference() is None)", "Output: True then True", "Output: False then True", "Output: True then False", "Output: TypeError"),
    createCodeQuestion("from types import MappingProxyType\ndata = {'x': 1}\nview = MappingProxyType(data)\ndata['x'] = 2\nprint(view['x'])\ntry:\n    view['y'] = 3\nexcept TypeError:\n    print('read-only')", "Output: 2 then read-only", "Output: 1 then read-only", "Output: 2 then y", "Output: TypeError before 2"),
    createCodeQuestion("def make():\n    data = {'count': 1}\n    def read():\n        return data['count']\n    data['count'] = 2\n    return read\nprint(make()())", "Output: 2", "Output: 1", "Output: KeyError", "Output: None"),
    createCodeQuestion("def f(x):\n    return x if x > 0 else -x\nprint(f(-4))", "Output: 4", "Output: -4", "Output: False", "Output: None"),
    createCodeQuestion("values = [1, 2, 3, 4]\nresult = [value * 2 for value in values if value % 2 == 0]\nprint(result)", "Output: [4, 8]", "Output: [2, 4, 6, 8]", "Output: [2, 6]", "Output: [1, 3]"),
    createCodeQuestion("text = 'A\\tB'\nprint(len(text))\nprint(text.split('\\t'))", "Output: 3 then ['A', 'B']", "Output: 4 then ['A', 'B']", "Output: 3 then ['A\\tB']", "Output: 2 then ['A', 'B']"),
    createCodeQuestion("values = [True, 1, 1.0, 2]\nprint(len(set(values)))\nprint(True == 1 == 1.0)", "Output: 2 then True", "Output: 4 then False", "Output: 3 then True", "Output: 2 then False"),
    createCodeQuestion("class Box:\n    def __init__(self, value):\n        self.value = value\n    def __bool__(self):\n        return self.value > 0\nprint(bool(Box(0)), bool(Box(2)))", "Output: False True", "Output: True True", "Output: False False", "Output: TypeError"),
    createCodeQuestion("def apply(fn, value):\n    return fn(fn(value))\nprint(apply(lambda x: x + 2, 3))", "Output: 7", "Output: 5", "Output: 9", "Output: 3"),
    createCodeQuestion("def make():\n    return lambda value: value * 2\nfn = make()\nprint(fn(6), callable(fn))", "Output: 12 True", "Output: 12 False", "Output: 8 True", "Output: None True"),
    createCodeQuestion("class User:\n    def __init__(self, name):\n        self.name = name\n    def __repr__(self):\n        return f'User({self.name!r})'\nprint(User('Ana'))", "Output: User('Ana')", "Output: <User name=Ana>", "Output: User(Ana)", "Output: Ana"),
  ];
}
