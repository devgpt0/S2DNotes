/**
 * Google Apps Script: Generate Python Fundamentals + Collections MCQ Google Form
 */

function createPythonConceptsQuizForm() {
  const config = {
    title: "KDK VAC Assessment No.1 Python MCQ Quiz",
    description: `Instructions:
• Total Questions: 100
• Each question carries 1 mark.
• All questions are mandatory.
• No negative marking.
• Passing Criteria: Minimum 40 out of 100 marks (40%).
• Ensure you submit the form only after answering all questions.
• Once submitted, responses cannot be edited.`,
    isQuiz: true,
    shuffleQuestions: false,
    collectEmail: true,
    pointsPerQuestion: 1,
  };

  const selectedQuestions = buildQuestionBank();
  validateQuestionBank(selectedQuestions);

  const form = FormApp.create(config.title)
    .setDescription(config.description)
    .setIsQuiz(config.isQuiz)
    .setShuffleQuestions(config.shuffleQuestions)
    .setCollectEmail(config.collectEmail)
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
      "Computer Science",
      "Information Technology",
      "Electronics and Communication",
      "Electrical Engineering",
      "Mechanical Engineering",
      "Civil Engineering",
      "Other",
    ].map((department) => departmentItem.createChoice(department)),
  );

  const yearItem = form.addListItem();
  yearItem.setTitle("Academic Year").setRequired(true);
  yearItem.setChoices(
    ["2nd Year", "3rd Year"].map((year) => yearItem.createChoice(year)),
  );

  form.addPageBreakItem().setTitle("Python MCQ Quiz");

  for (const [index, q] of selectedQuestions.entries()) {
    const item = form.addMultipleChoiceItem();
    const [questionText, code] = q.question.split("\n\n");
    const questionTitle = `${index + 1}. ${questionText}`;

    const shuffledOptions = q.options.map((option, index) => ({
      option,
      isCorrect: index === q.correctIndex,
    }));
    fisherYatesShuffle(shuffledOptions);

    item.setChoices(
      shuffledOptions.map(({ option, isCorrect }) =>
        item.createChoice(option, isCorrect),
      ),
    );
    setQuestionContent(item, questionTitle, code || "");
    item.setRequired(true);
    setQuestionPoints(item, config.pointsPerQuestion);
  }

  verifyGeneratedQuestions(form, selectedQuestions);

  Logger.log(`Form created: ${form.getPublishedUrl()}`);
  Logger.log(`Edit URL: ${form.getEditUrl()}`);
}

function setQuestionPoints(item, points) {
  const maxAttempts = 3;

  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    item.setPoints(points);

    if (item.getPoints() === points) {
      return;
    }
  }

  throw new Error(
    `Failed to set ${points} point(s) after ${maxAttempts} attempts`,
  );
}

function setQuestionContent(item, title, helpText) {
  const maxAttempts = 3;

  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    item.setTitle(title);
    item.setHelpText(helpText);

    if (item.getTitle() === title && item.getHelpText() === helpText) {
      return;
    }
  }

  throw new Error(
    `Failed to set question content after ${maxAttempts} attempts: ${title}`,
  );
}

function verifyGeneratedQuestions(form, questions) {
  const items = form
    .getItems(FormApp.ItemType.MULTIPLE_CHOICE)
    .map((item) => item.asMultipleChoiceItem());

  if (items.length !== questions.length) {
    throw new Error(
      `Generated MCQ count mismatch. Expected: ${questions.length}, Actual: ${items.length}`,
    );
  }

  let totalPoints = 0;

  items.forEach((item, index) => {
    const [questionText, code] = questions[index].question.split("\n\n");
    const expectedTitle = `${index + 1}. ${questionText}`;
    const expectedHelpText = code || "";

    if (item.getTitle() !== expectedTitle) {
      throw new Error(`Question ${index + 1} title was not saved`);
    }

    if (item.getHelpText() !== expectedHelpText) {
      throw new Error(`Question ${index + 1} description was not saved`);
    }

    const correctChoiceCount = item
      .getChoices()
      .filter((choice) => choice.isCorrectAnswer()).length;
    if (correctChoiceCount !== 1) {
      throw new Error(
        `Question ${index + 1} must have exactly one correct answer; found ${correctChoiceCount}`,
      );
    }

    const points = item.getPoints();
    if (points !== 1) {
      throw new Error(
        `Question ${index + 1} must have 1 point; found ${points}`,
      );
    }
    totalPoints += points;
  });

  if (totalPoints !== 100) {
    throw new Error(`Quiz must total 100 points; found ${totalPoints}`);
  }
}

function validateQuestionBank(questionBank) {
  if (questionBank.length !== 100) {
    throw new Error(
      `Question bank must contain exactly 100 questions; found ${questionBank.length}`,
    );
  }

  const questionTextSeen = new Set();
  const optionSignatureSeen = new Set();
  let codeQuestionCount = 0;

  questionBank.forEach((q, i) => {
    if (!q || typeof q !== "object") {
      throw new Error(`Invalid question object at index ${i}`);
    }

    if (typeof q.question !== "string" || q.question.trim() === "") {
      throw new Error(`Question text missing at index ${i}`);
    }

    if (q.question.includes("\n\n")) {
      codeQuestionCount += 1;
      const codeLines = q.question.split("\n\n")[1].split("\n");
      const codeLineCount = codeLines.length;
      if (codeLineCount < 2 || codeLineCount > 5) {
        throw new Error(
          `Code question ${i + 1} must contain 2 to 5 lines; found ${codeLineCount}`,
        );
      }
      if (codeLines.some((line) => line.trim().startsWith("#"))) {
        throw new Error(
          `Code question ${i + 1} must not use comments as code-line padding`,
        );
      }
    }

    if (!Array.isArray(q.options) || q.options.length !== 4) {
      throw new Error(`Question must have exactly 4 options at index ${i}`);
    }

    const normalizedQuestion = normalizeText(q.question);
    if (questionTextSeen.has(normalizedQuestion)) {
      throw new Error(`Duplicate question text detected: ${q.question}`);
    }
    questionTextSeen.add(normalizedQuestion);

    const normalizedOptions = q.options.map((option) =>
      option.trim().replace(/\s+/g, " "),
    );
    const uniqueOptionCount = new Set(normalizedOptions).size;
    if (uniqueOptionCount !== 4) {
      throw new Error(`Duplicate options inside a question: ${q.question}`);
    }

    if (
      !Number.isInteger(q.correctIndex) ||
      q.correctIndex < 0 ||
      q.correctIndex > 3
    ) {
      throw new Error(`Invalid correctIndex for question: ${q.question}`);
    }

    const signature = normalizedOptions.slice().sort().join("||");
    if (optionSignatureSeen.has(signature)) {
      throw new Error(`Duplicate option-set signature detected: ${q.question}`);
    }
    optionSignatureSeen.add(signature);
  });

  if (codeQuestionCount !== 60) {
    throw new Error(
      `Question bank must contain exactly 60 code questions; found ${codeQuestionCount}`,
    );
  }
}

function normalizeText(value) {
  return String(value).trim().toLowerCase().replace(/\s+/g, " ");
}

function fisherYatesShuffle(arr) {
  for (let i = arr.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    const temp = arr[i];
    arr[i] = arr[j];
    arr[j] = temp;
  }
}

function buildQuestionBank() {
  const codeQuestions = buildCodeSnippetQuestionBank();
  const theoryQuestions = buildConceptQuestionBank();
  const easyTheoryQuestions = [
    42, 43, 44, 45, 56, 57, 58, 59, 70, 71, 72, 73, 84, 85, 86, 87, 0, 1, 14,
    15,
  ].map((index) => theoryQuestions[index]);
  const mediumTheoryQuestions = [46, 50, 60, 64, 78, 80, 94, 98, 3, 17].map(
    (index) => theoryQuestions[index],
  );

  return [
    ...codeQuestions,
    ...easyTheoryQuestions,
    ...mediumTheoryQuestions,
    ...buildAdditionalMediumTheoryQuestions(),
  ];
}

function buildAdditionalMediumTheoryQuestions() {
  return [
    {
      question:
        "What happens to a nested list when only the outer list is copied with copy()?",
      options: [
        "The nested lists become tuples",
        "Every nested value is deep-copied",
        "The original and copy still share nested list objects",
        "The copy operation raises TypeError",
      ],
      correctIndex: 2,
    },
    {
      question:
        "Which statement correctly compares sorted(values) with values.sort()?",
      options: [
        "sorted returns a new list; sort changes the list and returns None",
        "Both return new tuples",
        "sorted changes the input; sort creates a copy",
        "Both remove duplicate values",
      ],
      correctIndex: 0,
    },
    {
      question: "What does the set expression left - right contain?",
      options: [
        "Values common to both sets",
        "Every value from both sets",
        "Values found only in right",
        "Values found in left but not in right",
      ],
      correctIndex: 3,
    },
    {
      question:
        "Which set method should be used when a missing value must not raise an error?",
      options: ["pop", "discard", "remove", "clear"],
      correctIndex: 1,
    },
    {
      question:
        "During extended tuple unpacking, what type of value does a starred target receive?",
      options: ["set", "generator", "list", "dictionary"],
      correctIndex: 2,
    },
    {
      question: "Why can a list stored inside a tuple still be changed?",
      options: [
        "Tuple immutability prevents replacing positions, not mutating a contained list",
        "Python converts the tuple into a list",
        "Lists inside tuples become global variables",
        "Tuple values are copied before every access",
      ],
      correctIndex: 0,
    },
    {
      question:
        "Which dictionary access is appropriate when a missing key should return a fallback?",
      options: [
        "data[key] without validation",
        "data.popitem()",
        "del data[key]",
        "data.get(key, fallback)",
      ],
      correctIndex: 3,
    },
    {
      question:
        "What happens to an existing dict.items() view after the dictionary is updated?",
      options: [
        "It becomes an empty tuple",
        "It reflects the updated dictionary contents",
        "It raises IndexError when read",
        "It remains a permanent snapshot",
      ],
      correctIndex: 1,
    },
    {
      question:
        "Which operation creates a new object because strings are immutable?",
      options: [
        "Appending to a list",
        "Adding an item to a set",
        "Calling text.replace(old, new)",
        "Updating a dictionary value",
      ],
      correctIndex: 2,
    },
    {
      question:
        "When two different lists contain equal values, which result is expected?",
      options: [
        "Value equality can be True while identity is False",
        "Both equality and identity must be True",
        "Identity is True whenever lengths match",
        "Value equality is always False for lists",
      ],
      correctIndex: 0,
    },
  ];
}

function createCodeQuestion(code, options, correctIndex) {
  return {
    question: "What is printed?\n\n" + code,
    options,
    correctIndex,
  };
}

function buildCodeSnippetQuestionBank() {
  return [
    createCodeQuestion(
      "items = [1, 2]\nitems.append(3)\nprint(items)",
      ["[3, 1, 2]", "[1, 2, 3]", "[1, 2]", "[1, 2, [3]]"],
      1,
    ),
    createCodeQuestion(
      "items = [1]\nitems.extend([2, 3])\nprint(items)",
      ["[1, 2, 3]", "[1, [2, 3]]", "[2, 3, 1]", "[1, 2]"],
      0,
    ),
    createCodeQuestion(
      "items = [1, 3]\nitems.insert(1, 2)\nprint(items)",
      ["[2, 1, 3]", "[1, 3, 2]", "[1, 3]", "[1, 2, 3]"],
      3,
    ),
    createCodeQuestion(
      "items = [1, 2, 2, 3]\nitems.remove(2)\nprint(items)",
      ["[1, 3]", "[1, 2, 2]", "[1, 2, 3]", "[1, 2, 2, 3]"],
      2,
    ),
    createCodeQuestion(
      "items = [10, 20, 30]\nremoved = items.pop()\nprint(removed, items)",
      ["10 [20, 30]", "30 [10, 20, 30]", "30 [10, 20]", "20 [10, 30]"],
      2,
    ),
    createCodeQuestion(
      "nums = [0, 1, 2, 3, 4]\npart = nums[1:4]\nprint(part)",
      ["[0, 1, 2, 3]", "[1, 2, 3, 4]", "[1, 2, 3]", "[4, 3, 2]"],
      2,
    ),
    createCodeQuestion(
      "items = [10, 20, 30]\nlast = items[-1]\nprint(last)",
      ["10", "30", "-1", "IndexError"],
      1,
    ),
    createCodeQuestion(
      "nums = [3, 1, 2]\nnums.sort()\nprint(nums)",
      ["[3, 1, 2]", "[3, 2, 1]", "None", "[1, 2, 3]"],
      3,
    ),
    createCodeQuestion(
      "nums = [3, 1, 2]\nordered = sorted(nums)\nprint(ordered, nums)",
      [
        "[1, 2, 3] [3, 1, 2]",
        "[1, 2, 3] [1, 2, 3]",
        "[3, 1, 2] [1, 2, 3]",
        "None [3, 1, 2]",
      ],
      0,
    ),
    createCodeQuestion(
      "nums = [1, 2, 3]\nnums.reverse()\nprint(nums)",
      ["[1, 2, 3]", "[3, 2, 1]", "[1, 3, 2]", "None"],
      1,
    ),
    createCodeQuestion(
      "items = [1, 2, 2, 3]\nresult = items.count(2)\nprint(result)",
      ["1", "2", "3", "0"],
      1,
    ),
    createCodeQuestion(
      "nums = [1, 2, 3]\nsquares = [value * value for value in nums]\nprint(squares)",
      ["[1, 2, 3]", "[1, 4, 9]", "[2, 4, 6]", "[1, 8, 27]"],
      1,
    ),
    createCodeQuestion(
      "values = [1, 1, 2, 3]\nunique = set(values)\nprint(sorted(unique))",
      ["[1, 1, 2, 3]", "[3, 2, 1]", "[1, 2]", "[1, 2, 3]"],
      3,
    ),
    createCodeQuestion(
      "values = {1, 2}\nvalues.add(3)\nprint(sorted(values))",
      ["[3]", "[1, 2]", "[1, 2, 3]", "[1, 2, 3, 3]"],
      2,
    ),
    createCodeQuestion(
      "values = {1}\nvalues.update([2, 3])\nprint(sorted(values))",
      ["[1, [2, 3]]", "[2, 3]", "[1, 2]", "[1, 2, 3]"],
      3,
    ),
    createCodeQuestion(
      "values = {1, 2}\nvalues.discard(9)\nprint(sorted(values))",
      ["[1, 2]", "[1, 2, 9]", "[9]", "KeyError"],
      0,
    ),
    createCodeQuestion(
      "left = {1, 2}\nright = {2, 3}\nprint(sorted(left | right))",
      ["[2]", "[1]", "[1, 2, 3]", "[1, 3]"],
      2,
    ),
    createCodeQuestion(
      "left = {1, 2}\nright = {2, 3}\nprint(sorted(left & right))",
      ["[1, 2]", "[2, 3]", "[1, 3]", "[2]"],
      3,
    ),
    createCodeQuestion(
      "left = {1, 2, 3}\nright = {2, 3}\nprint(sorted(left - right))",
      ["[2, 3]", "[1]", "[1, 2, 3]", "[]"],
      1,
    ),
    createCodeQuestion(
      "left = {1, 2}\nright = {2, 3}\nprint(sorted(left ^ right))",
      ["[2]", "[1, 2, 3]", "[1, 3]", "[]"],
      2,
    ),
    createCodeQuestion(
      "small = {1, 2}\nlarge = {1, 2, 3}\nprint(small.issubset(large))",
      ["False", "True", "None", "TypeError"],
      1,
    ),
    createCodeQuestion(
      "first = {1, 2}\nsecond = {3, 4}\nprint(first.isdisjoint(second))",
      ["False", "None", "KeyError", "True"],
      3,
    ),
    createCodeQuestion(
      "nums = [1, 2, 3]\nsquares = {value * value for value in nums}\nprint(sorted(squares))",
      ["{1, 4, 9}", "[1, 4]", "[4, 9]", "[1, 4, 9]"],
      3,
    ),
    createCodeQuestion(
      "values = frozenset([1, 1, 2])\nexpected = frozenset({1, 2})\nprint(values == expected)",
      ["True", "False", "TypeError", "AttributeError"],
      0,
    ),
    createCodeQuestion(
      "single = (5,)\nsize = len(single)\nprint(size)",
      ["0", "2", "1", "5"],
      2,
    ),
    createCodeQuestion(
      "values = (10, 20, 30)\nresult = values[1]\nprint(result)",
      ["10", "30", "20", "1"],
      2,
    ),
    createCodeQuestion(
      "values = (0, 1, 2, 3)\npart = values[1:3]\nprint(part)",
      ["(1, 2)", "[1, 2]", "(0, 1, 2)", "(2, 3)"],
      0,
    ),
    createCodeQuestion(
      "first = (1, 2)\nsecond = (3,)\nprint(first + second)",
      ["((1, 2), (3,))", "[1, 2, 3]", "(1, 2, 3)", "(4, 2)"],
      2,
    ),
    createCodeQuestion(
      "values = (1, 2)\nrepeated = values * 2\nprint(repeated)",
      ["(1, 2, 1, 2)", "(2, 4)", "((1, 2), (1, 2))", "[1, 2, 1, 2]"],
      0,
    ),
    createCodeQuestion(
      "values = (1, 2, 2, 3)\nresult = values.count(2)\nprint(result)",
      ["4", "-1", "ValueError", "2"],
      3,
    ),
    createCodeQuestion(
      "values = (5, 6, 7)\nposition = values.index(6)\nprint(position)",
      ["6", "2", "0", "1"],
      3,
    ),
    createCodeQuestion(
      "values = (2, 3)\nfirst, second = values\nprint(first, second)",
      ["2 3", "3 2", "(2, 3)", "[2, 3]"],
      0,
    ),
    createCodeQuestion(
      "values = (1, 2, 3, 4)\nfirst, *middle, last = values\nprint(middle)",
      ["[2, 3]", "(2, 3)", "[1, 2, 3]", "[3, 4]"],
      0,
    ),
    createCodeQuestion(
      "values = (1, [2])\nvalues[1].append(3)\nprint(values)",
      ["(1, [2])", "(1, [2, 3])", "(1, (2, 3))", "TypeError"],
      1,
    ),
    createCodeQuestion(
      'key = ("math", 1)\nscores = {key: 90}\nprint(scores[("math", 1)])',
      ["1", "math", "KeyError", "90"],
      3,
    ),
    createCodeQuestion(
      "items = [1, 2, 3]\nvalues = tuple(items)\nprint(values)",
      ["(1, 2)", "(1, 2, 3)", "(3, 2, 1)", "TypeError"],
      1,
    ),
    createCodeQuestion(
      'data = {"a": 1}\nvalue = data["a"]\nprint(value)',
      ["1", "a", "None", "KeyError"],
      0,
    ),
    createCodeQuestion(
      'data = {"a": 1}\nvalue = data.get("b", 9)\nprint(value)',
      ["None", "1", "9", "KeyError"],
      2,
    ),
    createCodeQuestion(
      'data = {"a": 1}\ndata["b"] = 2\nprint(data)',
      ["{'a': 1, 'b': 2}", "{'a': 1}", "{'b': 2}", "KeyError"],
      0,
    ),
    createCodeQuestion(
      'data = {"a": 1}\ndata["a"] = 5\nprint(data)',
      ["{'a': 1, 'a': 5}", "{'a': 5}", "{'a': 1}", "ValueError"],
      1,
    ),
    createCodeQuestion(
      'data = {"a": 1, "b": 2}\nremoved = data.pop("a")\nprint(removed, data)',
      ["2 {'a': 1}", "1 {'a': 1, 'b': 2}", "1 {'b': 2}", "KeyError"],
      2,
    ),
    createCodeQuestion(
      'data = {"a": 1}\nvalue = data.pop("b", 7)\nprint(value, data)',
      ["7 {'a': 1}", "None {'a': 1}", "7 {}", "KeyError"],
      0,
    ),
    createCodeQuestion(
      'data = {"a": 1}\nvalue = data.setdefault("b", 2)\nprint(value, data)',
      ["None {'a': 1}", "2 {'a': 1, 'b': 2}", "2 {'a': 1}", "KeyError"],
      1,
    ),
    createCodeQuestion(
      'data = {"b": 2, "a": 1}\nkeys = list(data.keys())\nprint(keys)',
      ["['a', 'b']", "[2, 1]", "dict_keys(['b', 'a'])", "['b', 'a']"],
      3,
    ),
    createCodeQuestion(
      'data = {"a": 1, "b": 2}\nvalues = list(data.values())\nprint(values)',
      ["['a', 'b']", "[('a', 1), ('b', 2)]", "[1, 2]", "dict_values([1, 2])"],
      2,
    ),
    createCodeQuestion(
      'data = {"a": 1, "b": 2}\nitems = list(data.items())\nprint(items)',
      ["['a', 'b']", "[1, 2]", "[('a', 1), ('b', 2)]", "{'a': 1, 'b': 2}"],
      2,
    ),
    createCodeQuestion(
      'data = {"a": 1}\nresult = "a" in data\nprint(result)',
      ["True", "False", "1", "KeyError"],
      0,
    ),
    createCodeQuestion(
      "nums = [1, 2, 3]\ndata = {value: value * value for value in nums}\nprint(data)",
      ["{1, 2, 3}", "[1, 4, 9]", "{1: 2, 2: 4, 3: 6}", "{1: 1, 2: 4, 3: 9}"],
      3,
    ),
    createCodeQuestion(
      "result = 7 / 2\nprint(result)",
      ["3", "3.5", "4", "2.5"],
      1,
    ),
    createCodeQuestion(
      "result = 7 // 2\nprint(result)",
      ["3.5", "2", "3", "1"],
      2,
    ),
    createCodeQuestion(
      "result = 7 % 2\nprint(result)",
      ["7", "3.5", "ZeroDivisionError", "1"],
      3,
    ),
    createCodeQuestion(
      "value = []\nprint(bool(value))",
      ["True", "None", "[]", "False"],
      3,
    ),
    createCodeQuestion(
      "value = (1,)\nprint(type(value).__name__)",
      ["tuple", "int", "list", "set"],
      0,
    ),
    createCodeQuestion(
      'text = "python"\nchanged = text.replace("p", "P")\nprint(text, changed)',
      ["Python Python", "python Python", "python python", "Python python"],
      1,
    ),
    createCodeQuestion(
      "first = [1]\nsecond = first\nsecond.append(2)\nprint(first)",
      ["[1, 2]", "[1]", "[2]", "None"],
      0,
    ),
    createCodeQuestion(
      "first = [1]\nsecond = first.copy()\nsecond.append(2)\nprint(first, second)",
      ["[1, 2] [1, 2]", "[1] [2]", "[1] [1, 2]", "[1, 2] [1]"],
      2,
    ),
    createCodeQuestion(
      "first = [1]\nsecond = first\nprint(first is second)",
      ["False", "None", "1", "True"],
      3,
    ),
    createCodeQuestion(
      "value = 10\nother = value\nother = 20\nprint(value, other)",
      ["10 20", "20 20", "10 10", "20 10"],
      0,
    ),
    createCodeQuestion(
      "def add_item(values):\n    values.append(3)\nitems = [1, 2]\nadd_item(items)\nprint(items)",
      ["[1, 2]", "[1, 2, 3]", "[3]", "None"],
      1,
    ),
    createCodeQuestion(
      "def replace(values):\n    values = [9]\nitems = [1, 2]\nreplace(items)\nprint(items)",
      ["[9]", "[1, 2]", "[1, 2, 9]", "None"],
      1,
    ),
  ];
}

function buildConceptQuestionBank() {
  return [
    // ===== Datatypes (1-14) =====
    {
      question:
        "Which built-in type stores an immutable ordered sequence of characters?",
      options: ["list", "set", "str", "dict"],
      correctIndex: 2,
    },
    {
      question: "What is the type of value produced by 3 / 2 in Python 3?",
      options: ["int", "float", "complex", "bool"],
      correctIndex: 1,
    },
    {
      question: "Which value is treated as falsy in boolean context?",
      options: ["42", "0", '"python"', "[1]"],
      correctIndex: 1,
    },
    {
      question: "Which numeric type can represent real and imaginary parts?",
      options: ["float", "decimal", "fraction", "complex"],
      correctIndex: 3,
    },
    {
      question: "What does type(None) return?",
      options: ["null", "NoneType", "void", "empty"],
      correctIndex: 1,
    },
    {
      question: "Which statement about bool in Python is correct?",
      options: [
        "bool is a subclass of int",
        "bool is unrelated to int",
        "bool has three values",
        "bool cannot be compared",
      ],
      correctIndex: 0,
    },
    {
      question: "Which conversion can raise ValueError for invalid content?",
      options: ["str(12)", "list((1,2))", "tuple([1,2])", 'int("12a")'],
      correctIndex: 3,
    },
    {
      question: "Which type is mutable?",
      options: ["tuple", "str", "frozenset", "list"],
      correctIndex: 3,
    },
    {
      question: "Which expression yields the integer floor division result?",
      options: ["7 / 3", "7 // 3", "7 % 3", "7 ** 3"],
      correctIndex: 1,
    },
    {
      question: "What is the type of (1,)?",
      options: ["int", "list", "set", "tuple"],
      correctIndex: 3,
    },
    {
      question: "Which built-in type enforces unique elements?",
      options: ["list", "set", "tuple", "bytes"],
      correctIndex: 1,
    },
    {
      question: 'What does len("abc") return?',
      options: ["2", "4", "1", "3"],
      correctIndex: 3,
    },
    {
      question: "Which expression correctly creates a bytes object?",
      options: ['"ABC"b', 'bytes["ABC"]', 'byte("ABC")', 'b"ABC"'],
      correctIndex: 3,
    },
    {
      question: "Which operator checks object identity?",
      options: ["==", "is", "in", ">="],
      correctIndex: 1,
    },

    // ===== Variables Model (15-28) =====
    {
      question: "In Python, a variable name primarily acts as what?",
      options: [
        "A reference bound to an object",
        "A fixed memory slot with raw bits",
        "A compile-time constant location",
        "A typed register pointer",
      ],
      correctIndex: 0,
    },
    {
      question: "What does b = a do for a list object?",
      options: [
        "Copies the reference",
        "Performs deep copy",
        "Performs shallow copy of nested items",
        "Creates immutable clone",
      ],
      correctIndex: 0,
    },
    {
      question: "Which operation usually creates a new list object?",
      options: ["a.append(x)", "a.extend([x])", "a.sort()", "a + [x]"],
      correctIndex: 3,
    },
    {
      question: "Which operation mutates an existing list in place?",
      options: [
        "concatenation with +",
        "append",
        "slicing copy [:]",
        "list() constructor from list",
      ],
      correctIndex: 1,
    },
    {
      question: "Which comparison checks value equality?",
      options: ["is", "id()", "==", "hash()"],
      correctIndex: 2,
    },
    {
      question:
        "Which comparison checks whether two names point to same object?",
      options: ["==", "is", "!=", "<>"],
      correctIndex: 1,
    },
    {
      question: "What is true about function arguments in Python?",
      options: [
        "Reference to object is passed by assignment",
        "Arguments are always deep-copied",
        "Arguments are pass-by-reference in C++ sense",
        "Arguments are pass-by-value bytes",
      ],
      correctIndex: 0,
    },
    {
      question: "Which copy strategy avoids shared nested mutable objects?",
      options: ["list.copy", "slice copy", "dict.copy", "copy.deepcopy"],
      correctIndex: 3,
    },
    {
      question: "What is the default-argument trap with mutable values?",
      options: [
        "Default object is recreated each call",
        "Default object is created once at function definition",
        "Default object is deep-copied each call",
        "Default object is frozen automatically",
      ],
      correctIndex: 1,
    },
    {
      question: "What does rebinding mean?",
      options: [
        "Object memory is edited directly",
        "All aliases update to same new identity",
        "Garbage collection is disabled",
        "Name points to a different object",
      ],
      correctIndex: 3,
    },
    {
      question: "Which built-in reveals an object identity integer?",
      options: ["type", "id", "len", "repr"],
      correctIndex: 1,
    },
    {
      question: "Aliasing risk is highest with which type?",
      options: ["Nested mutable containers", "Integers", "Booleans", "Strings"],
      correctIndex: 0,
    },
    {
      question: "Which statement about interning is safe?",
      options: [
        "Interning guarantees all equal objects are same identity",
        "Do not rely on interning for correctness",
        "Interning applies to all container types",
        "Interning disables garbage collection",
      ],
      correctIndex: 1,
    },
    {
      question:
        "When no references remain to an object, what typically happens?",
      options: [
        "It is moved to stack memory",
        "It is converted to None",
        "It becomes eligible for garbage collection",
        "It is pinned forever",
      ],
      correctIndex: 2,
    },

    // ===== Control Flow (29-42) =====
    {
      question: "In if/elif/else chain, which branch executes?",
      options: [
        "All True conditions",
        "Only else block always",
        "First condition that evaluates to True",
        "Random matching block",
      ],
      correctIndex: 2,
    },
    {
      question: "Operator precedence among not, and, or is:",
      options: [
        "or > and > not",
        "not > and > or",
        "and > or > not",
        "not > or > and",
      ],
      correctIndex: 1,
    },
    {
      question: "What does break do in a loop?",
      options: [
        "Skips to next iteration",
        "Ends function unconditionally",
        "Restarts the loop",
        "Terminates nearest enclosing loop",
      ],
      correctIndex: 3,
    },
    {
      question: "What does continue do in a loop?",
      options: [
        "Skips remaining statements in current iteration",
        "Exits loop immediately",
        "Returns from function",
        "Raises StopIteration in caller",
      ],
      correctIndex: 0,
    },
    {
      question: "When does loop else run?",
      options: [
        "Only when loop ends without break",
        "Only when loop has break",
        "Only for while loops",
        "Never in Python",
      ],
      correctIndex: 0,
    },
    {
      question: "What does pass do?",
      options: [
        "Skips to next loop iteration",
        "Raises NotImplementedError",
        "No operation placeholder",
        "Terminates current block",
      ],
      correctIndex: 2,
    },
    {
      question: "What is true about finally block?",
      options: [
        "It executes before leaving try statement",
        "It runs only if exception occurs",
        "It runs only when no exception occurs",
        "It is skipped by return",
      ],
      correctIndex: 0,
    },
    {
      question: "Which is recommended for expected branch logic?",
      options: [
        "Broad try/except around everything",
        "Using assert for all runtime validation",
        "if/elif conditions, not exception abuse",
        "Using while True with no exit",
      ],
      correctIndex: 2,
    },
    {
      question: "In match/case, evaluation order is:",
      options: [
        "Bottom to top always",
        "Randomized for performance",
        "All matching cases execute",
        "Top to bottom; first match wins",
      ],
      correctIndex: 3,
    },
    {
      question: "What does any(iterable) return?",
      options: [
        "True only if all elements are truthy",
        "Count of truthy elements",
        "Index of first truthy element",
        "True if at least one element is truthy",
      ],
      correctIndex: 3,
    },
    {
      question: "What does all(iterable) return?",
      options: [
        "True only if every element is truthy",
        "True if one element is truthy",
        "False for empty iterable always",
        "A list of booleans",
      ],
      correctIndex: 0,
    },
    {
      question: "Why use with statement for files?",
      options: [
        "Faster parsing of all files",
        "Automatic encryption",
        "Deterministic cleanup via context manager",
        "Implicit retry on read errors",
      ],
      correctIndex: 2,
    },
    {
      question: "A robust retry loop should include:",
      options: [
        "Infinite retries with no delay",
        "Bounded attempts and explicit retryable errors",
        "Silent exception suppression",
        "Random exception ignoring",
      ],
      correctIndex: 1,
    },
    {
      question: "Mutating a collection while iterating over it can:",
      options: [
        "Always raise SyntaxError",
        "Cause skipped or duplicated processing",
        "Always be safe and deterministic",
        "Automatically clone the collection",
      ],
      correctIndex: 1,
    },

    // ===== List (43-56) =====
    {
      question: "Which statement about Python list is correct?",
      options: [
        "Unordered immutable mapping",
        "Ordered and mutable sequence",
        "Immutable hash-only container",
        "Sorted key-value store",
      ],
      correctIndex: 1,
    },
    {
      question: "What does list(123) do?",
      options: [
        "Raises TypeError",
        "Returns [1,2,3]",
        "Returns [123]",
        "Returns []",
      ],
      correctIndex: 0,
    },
    {
      question: "What is returned by nums[1:5:2] from [0,1,2,3,4,5]?",
      options: ["[1, 2, 3, 4]", "[0, 2, 4]", "[1, 3]", "[5, 3, 1]"],
      correctIndex: 2,
    },
    {
      question: "Which operation adds one element object at list end?",
      options: ["extend", "insert_all", "append", "merge"],
      correctIndex: 2,
    },
    {
      question: "What does extend do?",
      options: [
        "Adds iterable as single nested element",
        "Removes duplicates only",
        "Adds elements from iterable individually",
        "Sorts before insertion",
      ],
      correctIndex: 2,
    },
    {
      question: "remove(x) on list:",
      options: [
        "Deletes all matching values",
        "Deletes first matching value",
        "Deletes by numeric index x",
        "Returns removed value always",
      ],
      correctIndex: 1,
    },
    {
      question: "Which can raise ValueError when element absent?",
      options: [
        "list.remove(value)",
        "list.pop(index)",
        "list.clear()",
        "list.append(value)",
      ],
      correctIndex: 0,
    },
    {
      question: "Which can raise IndexError on empty list?",
      options: ["count()", "copy()", "reverse()", "pop()"],
      correctIndex: 3,
    },
    {
      question: "list.sort() behavior is:",
      options: [
        "Sorts in place and returns None",
        "Returns new sorted list",
        "Sorts descending by default only",
        "Works only for integers",
      ],
      correctIndex: 0,
    },
    {
      question: "sorted(list_obj) behavior is:",
      options: [
        "Mutates list and returns None",
        "Raises on strings",
        "Returns new sorted list",
        "Returns tuple",
      ],
      correctIndex: 2,
    },
    {
      question: "What does list comprehension primarily provide?",
      options: [
        "Guaranteed deep copy semantics",
        "Concise map/filter style list construction",
        "In-place mutation only",
        "Automatic deduplication",
      ],
      correctIndex: 1,
    },
    {
      question: "Why is [[0]] * 3 risky?",
      options: [
        "Inner lists are aliased",
        "It is syntax error",
        "It creates immutable lists",
        "It deep-copies each inner list",
      ],
      correctIndex: 0,
    },
    {
      question: "What does enumerate(seq) yield?",
      options: [
        "(value, index) pairs only",
        "(index, value) pairs",
        "Values only",
        "Indices only",
      ],
      correctIndex: 1,
    },
    {
      question: "Membership check in list is typically:",
      options: [
        "O(1) hash lookup",
        "O(log n) tree search",
        "O(n) linear search",
        "O(n^2) always",
      ],
      correctIndex: 2,
    },

    // ===== Tuple (57-70) =====
    {
      question: "Which statement about tuple is correct?",
      options: [
        "Tuple is immutable ordered sequence",
        "Tuple supports append and remove",
        "Tuple is unordered",
        "Tuple stores only numeric values",
      ],
      correctIndex: 0,
    },
    {
      question: "Correct one-element tuple syntax is:",
      options: ["(7)", "[7]", "{7}", "(7,)"],
      correctIndex: 3,
    },
    {
      question: "What does tuple([1,2,3]) return?",
      options: ["(1, 2, 3)", "[1, 2, 3]", "{1, 2, 3}", "TypeError"],
      correctIndex: 0,
    },
    {
      question: "Which tuple operation is valid?",
      options: [
        "Item assignment by index",
        "append method call",
        "clear method call",
        "Concatenation with +",
      ],
      correctIndex: 3,
    },
    {
      question: "Tuple unpacking requires:",
      options: [
        "Matching targets unless starred capture used",
        "Always exact two targets",
        "Only mutable RHS values",
        "Only explicit tuple literals",
      ],
      correctIndex: 0,
    },
    {
      question: "What does *rest capture in unpacking?",
      options: [
        "Remaining items as tuple always",
        "Only last item",
        "Remaining items as list",
        "Only first item",
      ],
      correctIndex: 2,
    },
    {
      question: "tuple.count(x) returns:",
      options: [
        "Index of first occurrence",
        "Number of occurrences",
        "Boolean presence",
        "Removed element",
      ],
      correctIndex: 1,
    },
    {
      question: "tuple.index(x) returns:",
      options: [
        "Last index of value",
        "Count of value",
        "None if not found",
        "First index of value",
      ],
      correctIndex: 3,
    },
    {
      question: "A tuple with nested list can appear to change because:",
      options: [
        "Tuple auto-converts to list",
        "Tuple mutability is dynamic",
        "Nested list is mutable",
        "Garbage collector rewrites tuple",
      ],
      correctIndex: 2,
    },
    {
      question: "Which is hashable when contents are hashable?",
      options: ["tuple", "list", "set", "dict"],
      correctIndex: 0,
    },
    {
      question: "Why might tuple be preferred over list for records?",
      options: [
        "Tuple provides O(1) append",
        "Immutability communicates fixed structure intent",
        "Tuple auto-validates field names",
        "Tuple deduplicates values",
      ],
      correctIndex: 1,
    },
    {
      question: "What is result type of slicing a tuple?",
      options: ["list", "iterator", "tuple", "view"],
      correctIndex: 2,
    },
    {
      question: "t *= 2 for tuple generally means:",
      options: [
        "Mutate tuple in place",
        "Create a new repeated tuple and rebind name",
        "Raise TypeError always",
        "Convert tuple to list",
      ],
      correctIndex: 1,
    },
    {
      question: "Which API is absent on tuple but present on list?",
      options: ["count", "append", "index", "len"],
      correctIndex: 1,
    },

    // ===== Dict (71-84) =====
    {
      question: "Dictionary primarily represents:",
      options: [
        "Ordered unique-only sequence",
        "Immutable index-based collection",
        "Key-value mapping",
        "Character buffer",
      ],
      correctIndex: 2,
    },
    {
      question: "Which key type is invalid in dict?",
      options: ["str", "int", "tuple of hashables", "list"],
      correctIndex: 3,
    },
    {
      question: "What happens with duplicate keys in a literal?",
      options: [
        "Syntax error",
        "Both values stored in list automatically",
        "First value is preserved always",
        "Last value overwrites earlier one",
      ],
      correctIndex: 3,
    },
    {
      question: "d[missing_key] does what?",
      options: [
        "Returns None",
        "Raises KeyError",
        "Inserts key with None",
        "Returns empty string",
      ],
      correctIndex: 1,
    },
    {
      question: "d.get(missing, default) does what?",
      options: [
        "Raises KeyError",
        "Inserts key with default",
        "Returns tuple (key, default)",
        "Returns default without inserting key",
      ],
      correctIndex: 3,
    },
    {
      question: "setdefault on absent key does:",
      options: [
        "Raise KeyError",
        "Return None and skip insert",
        "Insert default and return it",
        "Delete key immediately",
      ],
      correctIndex: 2,
    },
    {
      question: "In Python 3.7+, dict order guarantee is:",
      options: [
        "Sorted by key always",
        "Randomized each run",
        "Undefined and unstable always",
        "Insertion order is preserved",
      ],
      correctIndex: 3,
    },
    {
      question: "What does pop(key) do?",
      options: [
        "Only return value without deletion",
        "Remove random key",
        "Remove key and return its value",
        "Clear entire dictionary",
      ],
      correctIndex: 2,
    },
    {
      question: "popitem() in modern Python dict removes:",
      options: [
        "Last inserted item",
        "Random item",
        "Smallest key item",
        "First inserted item always",
      ],
      correctIndex: 0,
    },
    {
      question: "dict views (keys/items/values) are:",
      options: [
        "Static copies detached from dict",
        "Writable by numeric index",
        "Always tuples",
        "Dynamic views reflecting later updates",
      ],
      correctIndex: 3,
    },
    {
      question: "Membership test key in d checks:",
      options: ["Values", "Items tuples", "Keys", "Keys and values both"],
      correctIndex: 2,
    },
    {
      question: "dict.fromkeys(keys, []) pitfall is:",
      options: [
        "TypeError for list defaults",
        "Shared mutable default across keys",
        "Automatic deep copy per key",
        "Keys are sorted unexpectedly",
      ],
      correctIndex: 1,
    },
    {
      question: "Which creates dict from iterable pairs?",
      options: [
        'dict([("a",1),("b",2)])',
        '{("a",1),("b",2)}',
        '["a":1,"b":2]',
        'mapdict("a",1,"b",2)',
      ],
      correctIndex: 0,
    },
    {
      question: "Dictionary comprehension syntax uses:",
      options: [
        "{k: v for ...}",
        "[k: v for ...]",
        "(k: v for ...)",
        "{k, v for ...}",
      ],
      correctIndex: 0,
    },

    // ===== Set (85-100) =====
    {
      question: "Set is best described as:",
      options: [
        "Ordered mutable sequence with duplicates",
        "Key-value mapping preserving insertion",
        "Immutable numeric array",
        "Unordered collection of unique hashable elements",
      ],
      correctIndex: 3,
    },
    {
      question: "How do you create an empty set?",
      options: ["{}", "[]", "()", "set()"],
      correctIndex: 3,
    },
    {
      question: "What does set([1,2,2,3]) contain?",
      options: [
        "All original duplicates intact",
        "Only last element",
        "1,2,3 unique elements",
        "Raises ValueError",
      ],
      correctIndex: 2,
    },
    {
      question: "Which method adds one element to set?",
      options: ["append", "insert", "add", "extend_one"],
      correctIndex: 2,
    },
    {
      question: "Which method ignores missing element without error?",
      options: ["discard", "remove", "pop", "delete"],
      correctIndex: 0,
    },
    {
      question: "remove on missing set element raises:",
      options: ["KeyError", "ValueError", "IndexError", "TypeError"],
      correctIndex: 0,
    },
    {
      question: "Set pop removes:",
      options: [
        "The smallest element always",
        "An arbitrary element",
        "The oldest inserted element always",
        "A random index",
      ],
      correctIndex: 1,
    },
    {
      question: "Union operation symbol is:",
      options: ["|", "+", "&", "^"],
      correctIndex: 0,
    },
    {
      question: "Intersection operation symbol is:",
      options: ["|", "-", "&", "^"],
      correctIndex: 2,
    },
    {
      question: "Symmetric difference means:",
      options: [
        "Elements common to both sets",
        "Elements only in first set",
        "Elements in exactly one set",
        "Merged pairs of values",
      ],
      correctIndex: 2,
    },
    {
      question: "a.issubset(b) is True when:",
      options: [
        "Every element of b is in a",
        "a and b are identical objects",
        "Every element of a is in b",
        "a has fewer elements",
      ],
      correctIndex: 2,
    },
    {
      question: "isdisjoint checks whether:",
      options: [
        "Two sets have same size",
        "One set contains another",
        "Set is empty",
        "Two sets share no common elements",
      ],
      correctIndex: 3,
    },
    {
      question: "Why is set membership usually fast?",
      options: [
        "Binary search on sorted storage",
        "Linked list traversal",
        "Tree rotation balancing",
        "Hash-table based lookup",
      ],
      correctIndex: 3,
    },
    {
      question: "frozenset is useful because it is:",
      options: [
        "Mutable and order-preserving",
        "Indexable like list",
        "Immutable and hashable",
        "Key-value based",
      ],
      correctIndex: 2,
    },
    {
      question: "Can set reliably support index-based business logic?",
      options: [
        "Yes, insertion index is guaranteed",
        "Yes, natural sort order is guaranteed",
        "No, order is not a stable contract",
        "Only if all elements are integers",
      ],
      correctIndex: 2,
    },
    {
      question: "Which pattern preserves order while deduplicating sequence?",
      options: [
        "list(set(seq))",
        "sorted(set(seq))",
        "list(dict.fromkeys(seq))",
        "tuple(set(seq))",
      ],
      correctIndex: 2,
    },
  ];
}
