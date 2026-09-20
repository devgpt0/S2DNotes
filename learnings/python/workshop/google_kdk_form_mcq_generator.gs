/**
 * Google Apps Script: Generate Python Variables and Name Binding MCQ Google Form
 */

function createPythonConceptsQuizForm() {
  const config = {
    title: "KDK VAC Assessment No.1 Python Variables MCQ Quiz",
    description: `Instructions:
 - Total Questions: 100
 - Section 2 MCQs are optional.
 - Each correct answer carries 1 mark.
 - No negative marking.
 - Passing Criteria: Minimum 40 marks.
 - Once submitted, responses cannot be edited.`,
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

  form.addPageBreakItem().setTitle("Python Variables and Name Binding MCQ Quiz");

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
    item.setRequired(false);
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
  return [
    ...buildVariableModelCodeQuestionBank(),
    ...buildVariableModelTheoryQuestionBank(),
  ];
}

function createCodeQuestion(code, options, correctIndex) {
  return {
    question: "What is printed?\n\n" + code,
    options,
    correctIndex,
  };
}

function createTheoryQuestion(question, options, correctIndex) {
  return {
    question,
    options,
    correctIndex,
  };
}

function buildVariableModelCodeQuestionBank() {
  return [
    createCodeQuestion(
      "score = 95\nprint(score)",
      ["95", "int", "None", "score"],
      0,
    ),
    createCodeQuestion(
      "score = 95\nprint(type(score).__name__)",
      ["str", "float", "int", "object"],
      2,
    ),
    createCodeQuestion(
      'result = 10\nresult = "complete"\nprint(result)',
      ["10", "complete", "result", "None"],
      1,
    ),
    createCodeQuestion(
      'user_name = "Ana"\nuser2 = "Ravi"\nprint(user_name, user2)',
      ["Ana Ravi", "Ravi Ana", "user_name user2", "None None"],
      0,
    ),
    createCodeQuestion(
      'name = "lower"\nName = "upper"\nprint(name, Name)',
      ["upper lower", "lower upper", "lower lower", "Name name"],
      1,
    ),
    createCodeQuestion(
      "item_count = 3\nunit_price = 10\ntotal_price = item_count * unit_price\nprint(total_price)",
      ["13", "30", "310", "total_price"],
      1,
    ),
    createCodeQuestion(
      "first = [1, 2]\nsecond = first\nprint(first is second)",
      ["False", "True", "1", "None"],
      1,
    ),
    createCodeQuestion(
      "first = [1, 2]\nsecond = first\nsecond.append(3)\nprint(first)",
      ["[1, 2]", "[3]", "[1, 2, 3]", "None"],
      2,
    ),
    createCodeQuestion(
      "first = [1, 2]\nsecond = first\nsecond = [9, 10]\nprint(first)",
      ["[9, 10]", "[1, 2]", "[]", "NameError"],
      1,
    ),
    createCodeQuestion(
      "first = [1, 2]\nsecond = first\nsecond = [9, 10]\nprint(second)",
      ["[1, 2]", "[9, 10]", "first", "None"],
      1,
    ),
    createCodeQuestion(
      "first = [1, 2]\nsecond = first\nsecond = [9, 10]\nprint(first is second)",
      ["True", "False", "2", "TypeError"],
      1,
    ),
    createCodeQuestion(
      "numbers = [1, 2]\nidentity_before = id(numbers)\nnumbers.append(3)\nprint(id(numbers) == identity_before)",
      ["False", "True", "3", "None"],
      1,
    ),
    createCodeQuestion(
      "number = 10\nidentity_before = id(number)\nnumber += 1\nprint(id(number) == identity_before)",
      ["True", "False", "11", "NameError"],
      1,
    ),
    createCodeQuestion(
      'name, age, active = "Ana", 25, True\nprint(name)',
      ["Ana", "25", "True", "name"],
      0,
    ),
    createCodeQuestion(
      'name, age, active = "Ana", 25, True\nprint(age)',
      ["Ana", "25", "True", "active"],
      1,
    ),
    createCodeQuestion(
      'name, age, active = "Ana", 25, True\nprint(active)',
      ["Ana", "25", "True", "1"],
      2,
    ),
    createCodeQuestion(
      'first = second = []\nfirst.append("shared")\nprint(second)',
      ["[]", "['shared']", "['first']", "NameError"],
      1,
    ),
    createCodeQuestion(
      'first = second = []\nfirst.append("shared")\nprint(first is second)',
      ["False", "True", "shared", "None"],
      1,
    ),
    createCodeQuestion(
      "point = (4, 7)\nx, y = point\nprint(x)",
      ["4", "7", "(4, 7)", "x"],
      0,
    ),
    createCodeQuestion(
      "point = (4, 7)\nx, y = point\nprint(y)",
      ["4", "7", "point", "None"],
      1,
    ),
    createCodeQuestion(
      "first, *middle, last = [1, 2, 3, 4, 5]\nprint(middle)",
      ["[1, 2]", "[2, 3, 4]", "(2, 3, 4)", "5"],
      1,
    ),
    createCodeQuestion(
      "first, *middle, last = [1, 2, 3, 4, 5]\nprint(first)",
      ["1", "[2, 3, 4]", "5", "first"],
      0,
    ),
    createCodeQuestion(
      "first, *middle, last = [1, 2, 3, 4, 5]\nprint(last)",
      ["1", "[2, 3, 4]", "5", "last"],
      2,
    ),
    createCodeQuestion(
      "left = 10\nright = 20\nleft, right = right, left\nprint(left, right)",
      ["10 20", "20 10", "(20, 10)", "right left"],
      1,
    ),
    createCodeQuestion(
      "number = 5\nnumber += 2\nprint(number)",
      ["5", "7", "52", "None"],
      1,
    ),
    createCodeQuestion(
      "items = [1]\nalias = items\nitems += [2]\nprint(alias)",
      ["[1]", "[2]", "[1, 2]", "None"],
      2,
    ),
    createCodeQuestion(
      "first = [1, 2]\nsecond = first\ndel first\nprint(second)",
      ["[1, 2]", "[]", "NameError", "None"],
      0,
    ),
    createCodeQuestion(
      "count: int = 3\nprint(count, type(count).__name__)",
      ["3 int", "3 str", "int 3", "None"],
      0,
    ),
    createCodeQuestion(
      'count: int = 3\ncount = "three"\nprint(count, type(count).__name__)',
      ["3 int", "three str", "three int", "count str"],
      1,
    ),
    createCodeQuestion(
      "def append_item(items):\n    items.append(3)\noriginal = [1, 2]\nappend_item(original)\nprint(original)",
      ["[1, 2]", "[1, 2, 3]", "[3]", "[1, 2, 3, 0]"],
      1,
    ),
    createCodeQuestion(
      "def replace(items):\n    items = [9]\noriginal = [1, 2]\nreplace(original)\nprint(original)",
      ["[9]", "[1, 2]", "[1, 2, 9]", "None"],
      1,
    ),
    createCodeQuestion(
      'status = "global"\ndef show_status():\n    status = "local"\n    print(status)\nshow_status()',
      ["global", "local", "status", "NameError"],
      1,
    ),
    createCodeQuestion(
      'status = "global"\ndef show_status():\n    status = "local"\nshow_status()\nprint(status)',
      ["local", "global", "status", "None"],
      1,
    ),
    createCodeQuestion(
      'try:\n    print(total)\nexcept NameError:\n    print("NameError")',
      ["total", "NameError", "None", "0"],
      1,
    ),
    createCodeQuestion(
      "a = []\nb = a\nb.append(1)\nprint(a is b)",
      ["False", "True", "1", "[]"],
      1,
    ),
    createCodeQuestion(
      "a = [1]\nb = a\na = [2]\nprint(a is b)",
      ["True", "False", "[1]", "TypeError"],
      1,
    ),
    createCodeQuestion(
      "a = [1]\nbefore = id(a)\na.append(2)\nprint(id(a) == before)",
      ["False", "True", "2", "None"],
      1,
    ),
    createCodeQuestion(
      "value = 10\nother = value\nvalue += 1\nprint(other, value)",
      ["10 10", "11 11", "10 11", "11 10"],
      2,
    ),
    createCodeQuestion(
      "a, b, c = (1, 2, 3)\nprint(a, b, c)",
      ["1 2 3", "3 2 1", "(1, 2, 3)", "None"],
      0,
    ),
    createCodeQuestion(
      "first, *middle, last = [1, 2]\nprint(middle)",
      ["[]", "[1]", "[2]", "None"],
      0,
    ),
    createCodeQuestion(
      "first, *middle, last = [1, 2, 3]\nprint(type(middle).__name__)",
      ["object", "list", "name", "integer"],
      1,
    ),
    createCodeQuestion(
      "left = 10\nright = 20\nleft, right = right, left\nprint(right)",
      ["10", "20", "left", "None"],
      0,
    ),
    createCodeQuestion(
      "number = 5\nalias = number\nnumber += 2\nprint(alias, number)",
      ["5 7", "7 7", "5 5", "7 5"],
      0,
    ),
    createCodeQuestion(
      "items = [1]\nalias = items\nbefore = id(items)\nitems += [2]\nprint(id(items) == before)",
      ["False", "True", "[1, 2]", "None"],
      1,
    ),
    createCodeQuestion(
      "first = [1, 2]\nsecond = first\ndel first\nprint(first)",
      ["[1, 2]", "NameError", "second", "None"],
      1,
    ),
    createCodeQuestion(
      "count: int = 3\ncount = 'three'\nprint(type(count).__name__)",
      ["int", "str", "type", "NoneType"],
      1,
    ),
    createCodeQuestion(
      "def show(items):\n    print(items is original)\noriginal = [1]\nshow(original)",
      ["True", "False", "original", "None"],
      0,
    ),
    createCodeQuestion(
      "def add_item(items):\n    items.append(3)\nitems = [1, 2]\nadd_item(items)\nprint(items)",
      ["[1, 2]", "[1, 2, 3]", "[3]", "[1, 2, 3, 3]"],
      1,
    ),
    createCodeQuestion(
      "def replace(items):\n    items = [9]\nitems = [1, 2]\nreplace(items)\nprint(items)",
      ["[9]", "[1, 2]", "[1, 2, 9]", "[9, 1]"],
      1,
    ),
    createCodeQuestion(
      'status = "global"\ndef show():\n    status = "local"\nshow()\nprint(status)',
      ["local", "global", "status", "unbound"],
      1,
    ),
    createCodeQuestion(
      'try:\n    print(total)\nexcept NameError as error:\n    print(type(error).__name__)',
      ["NameError", "total", "None", "int"],
      0,
    ),
    createCodeQuestion(
      "first = [1]\nsecond = first\nfirst = [2]\nprint(second)",
      ["[1]", "[2]", "[]", "[0]"],
      0,
    ),
    createCodeQuestion(
      "first = [1]\nsecond = first\nfirst.append(2)\nprint(second)",
      ["[1]", "[2]", "[1, 2]", "[0]"],
      2,
    ),
    createCodeQuestion(
      "a = 1\nb = a\na = 2\nprint(b)",
      ["1", "2", "a", "None"],
      0,
    ),
    createCodeQuestion(
      "a = []\nb = a\na += [1]\nprint(b)",
      ["[]", "[1]", "a", "[0]"],
      1,
    ),
    createCodeQuestion(
      "x, y = (4, 7)\nprint(x, y)",
      ["4 7", "7 4", "(4, 7)", "None"],
      0,
    ),
    createCodeQuestion(
      "first, *rest, last = [1, 2, 3, 4]\nprint(rest)",
      ["[2, 3]", "(2, 3)", "[1, 2, 3]", "None"],
      0,
    ),
    createCodeQuestion(
      "number = 10\nalias = number\nnumber += 1\nprint(alias)",
      ["10", "11", "number", "None"],
      0,
    ),
    createCodeQuestion(
      "items = [1]\nalias = items\nitems += [2]\nprint(items, alias)",
      ["[1] [1]", "[1, 2] [1, 2]", "[1, 2] [1]", "None"],
      1,
    ),
    createCodeQuestion(
      "item = [1]\nother = item\nitem.append(2)\nprint(other)",
      ["[1]", "[2]", "[1, 2]", "[1, 2, 2]"],
      2,
    ),
  ];
}

function buildVariableModelTheoryQuestionBank() {
  return [
    createTheoryQuestion(
      "In Python, what is a variable name primarily?",
      ["A label bound to an object", "A raw memory box", "A fixed register", "A compile-time value"],
      0,
    ),
    createTheoryQuestion(
      "What does assignment do first?",
      ["Evaluates the right side", "Deletes the left name", "Binds the left name twice", "Freezes the value"],
      0,
    ),
    createTheoryQuestion(
      "What is dynamically typed in Python?",
      ["Names can be rebound to objects of other types", "Names can never change", "Only lists have types", "Types belong to keywords"],
      0,
    ),
    createTheoryQuestion(
      "Where is a runtime type associated?",
      ["With the object", "With the spelling of a name", "With the line number", "With the assignment operator"],
      0,
    ),
    createTheoryQuestion(
      "Which characters may appear in a Python identifier?",
      ["Letters, digits, and underscores", "Spaces, hyphens, and dots", "Only digits", "Only punctuation"],
      0,
    ),
    createTheoryQuestion(
      "Which identifier is invalid because of its first character?",
      ["2nd_place", "place_2", "_place", "place"],
      0,
    ),
    createTheoryQuestion(
      "Which identifier rule is correct?",
      ["An identifier cannot be a Python keyword", "Every identifier must contain a digit", "Identifiers may contain spaces", "Identifiers ignore capitalization"],
      0,
    ),
    createTheoryQuestion(
      "What does it mean that Python identifiers are case-sensitive?",
      ["name and Name are different names", "name and Name are always aliases", "Capitalization is ignored", "Only class names use case"],
      0,
    ),
    createTheoryQuestion(
      "Which convention is recommended for a variable name?",
      ["snake_case", "PascalCase", "UPPERCASE_WITHOUT_UNDERSCORES", "kebab-case"],
      0,
    ),
    createTheoryQuestion(
      "Which convention is shown for a class name?",
      ["PascalCase", "snake_case", "lowercase-only", "leading-hyphen"],
      0,
    ),
    createTheoryQuestion(
      "Which convention is shown for a constant?",
      ["UPPER_SNAKE_CASE", "PascalCase", "single-letter lowercase", "space separated"],
      0,
    ),
    createTheoryQuestion(
      "What convention is shown for an internal name?",
      ["A leading underscore", "A trailing hyphen", "A leading digit", "A space prefix"],
      0,
    ),
    createTheoryQuestion(
      "What should a meaningful name describe?",
      ["Its purpose", "Its memory address", "Its source-code color", "Its line count"],
      0,
    ),
    createTheoryQuestion(
      "What does assigning one name to another copy?",
      ["The reference to the object", "A different object", "Only the object type", "The object into a keyword"],
      0,
    ),
    createTheoryQuestion(
      "What is an alias in the variables model?",
      ["A second name for the same object", "A different object with no relation", "A deleted binding", "A type annotation"],
      0,
    ),
    createTheoryQuestion(
      "What is rebinding?",
      ["Making a name refer to another object", "Mutating every object", "Renaming a keyword", "Removing all names"],
      0,
    ),
    createTheoryQuestion(
      "What happens to the old object during rebinding?",
      ["It is not altered by the rebinding", "It is always mutated", "It becomes a keyword", "It is always destroyed immediately"],
      0,
    ),
    createTheoryQuestion(
      "What does mutation change?",
      ["An existing object", "Only a name spelling", "The Python keyword list", "A source-file comment"],
      0,
    ),
    createTheoryQuestion(
      "What stays unchanged when an object is mutated?",
      ["Its identity", "Every alias name", "Its source line", "Its annotation text"],
      0,
    ),
    createTheoryQuestion(
      "What happens when an immutable value is apparently updated?",
      ["A new object is created and bound", "The old object is edited in place", "All names are deleted", "The operation is ignored"],
      0,
    ),
    createTheoryQuestion(
      "What does multiple assignment bind?",
      ["Several names in one statement", "Only one name in many files", "A name to a keyword", "Every object to one name"],
      0,
    ),
    createTheoryQuestion(
      "Without starred unpacking, what must match in multiple assignment?",
      ["The number of target names and values", "The spelling of every value", "The identity of every name", "The number of source files"],
      0,
    ),
    createTheoryQuestion(
      "What does chained assignment do?",
      ["Binds each name to the same object", "Creates independent mutable objects", "Converts names to constants", "Deletes the right side"],
      0,
    ),
    createTheoryQuestion(
      "What does sequence unpacking do?",
      ["Binds sequence items to separate names", "Sorts every sequence", "Copies all objects separately", "Changes names to strings"],
      0,
    ),
    createTheoryQuestion(
      "What does a starred unpacking target collect?",
      ["The remaining items in a list", "The remaining items in a tuple object", "Only the first item", "Only the last item"],
      0,
    ),
    createTheoryQuestion(
      "How many starred targets may appear at one assignment level?",
      ["One", "Two", "None", "Any number"],
      0,
    ),
    createTheoryQuestion(
      "What does Python evaluate before a swap binds the left side?",
      ["The right side", "The function name", "The next statement", "The type annotation only"],
      0,
    ),
    createTheoryQuestion(
      "What does augmented assignment do conceptually?",
      ["Reads, operates, then rebinds or mutates", "Only deletes a name", "Always creates a different object", "Always creates a tuple"],
      0,
    ),
    createTheoryQuestion(
      "What does integer += generally do?",
      ["Creates and binds a new integer", "Mutates the existing integer", "Creates a local function", "Deletes the integer name"],
      0,
    ),
    createTheoryQuestion(
      "What does list += generally do in the note's example?",
      ["Mutates the list", "Makes the list immutable", "Deletes the list alias", "Converts the list to a name"],
      0,
    ),
    createTheoryQuestion(
      "What does del name remove?",
      ["The name's binding", "The object from all aliases", "The object's type", "The entire function"],
      0,
    ),
    createTheoryQuestion(
      "Does del name necessarily destroy the object?",
      ["No, another reference may keep it alive", "Yes, always", "Only if the object is a list", "Only if the name is global"],
      0,
    ),
    createTheoryQuestion(
      "What does a variable annotation document?",
      ["The expected type", "A guaranteed runtime conversion", "The object's identity", "The name's memory address"],
      0,
    ),
    createTheoryQuestion(
      "Does a variable annotation enforce the type at runtime?",
      ["No", "Yes, always", "Only for strings", "Only inside functions"],
      0,
    ),
    createTheoryQuestion(
      "What is a function parameter?",
      ["A local name bound to the passed object", "A separate local object", "A global constant", "A new keyword"],
      0,
    ),
    createTheoryQuestion(
      "What can a parameter's mutation do to the caller's object?",
      ["The mutation can be visible", "It always creates a new local object", "It deletes the caller's name", "It changes the caller's type annotation"],
      0,
    ),
    createTheoryQuestion(
      "What does local rebinding inside a function do to the caller's name?",
      ["It does not rebind the caller's name", "It always changes the caller's name", "It deletes the caller's object", "It makes the caller global"],
      0,
    ),
    createTheoryQuestion(
      "What does assignment inside a function create by default?",
      ["A local name", "A new module", "A Python keyword", "A global name in every case"],
      0,
    ),
    createTheoryQuestion(
      "What error is raised when a name is read before it is bound?",
      ["NameError", "TypeError", "IndexError", "ValueError"],
      0,
    ),
    createTheoryQuestion(
      "What is the recommended alternative to mutable global state?",
      ["Parameters and return values", "More chained assignments", "Unbound names", "Extra annotations only"],
      0,
    ),
  ];
}
