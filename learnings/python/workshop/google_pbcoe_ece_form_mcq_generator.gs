/**
 * Google Apps Script: Generate PBCOE VAC Assessment No.1 Python Variables MCQ Quiz.
 * Scope: variables model.md, concepts 1 through 17.
 * Difficulty distribution is validated internally and is not shown in the form.
 */

function createPythonVariablesQuizForm() {
  createPbcoeEceVariablesAssessment();
}

function createPbcoeEceVariablesAssessment() {
  const config = {
    title: "PBCOE VAC Assessment No.1 Python Variables MCQ Quiz - ECE",
    description: `Instructions:
- Total Questions: 100
- Each question carries 1 mark.
- All questions are mandatory.
- No negative marking.
- Passing Criteria: Minimum 40 out of 100 marks (40%).
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

  form.addPageBreakItem().setTitle("Python Variables MCQ Quiz");

  const generatedItems = [];
  questions.forEach((question, index) => {
    const item = form.addMultipleChoiceItem();
    const [questionTitle, code] = question.question.split("\n\n");
    const choices = question.options.map((option, optionIndex) => ({
      option,
      isCorrect: optionIndex === question.correctIndex,
    }));
    const arrangedChoices = arrangeChoicesForAnswerSlot(choices, answerSlots[index]);
    item.setTitle(`${index + 1}. ${questionTitle}`);
    if (code) {
      item.setHelpText(code);
    }
    item.setChoices(
      arrangedChoices.map(({ option, isCorrect }) =>
        item.createChoice(option, isCorrect),
      ),
    );
    item.setRequired(true);
    generatedItems.push(item);
  });

  applyPointsWithRetry(generatedItems, config.pointsPerQuestion);
  verifyGeneratedQuestions(form, questions, config.pointsPerQuestion);
  Logger.log(`Form created: ${form.getPublishedUrl()}`);
  Logger.log(`Edit URL: ${form.getEditUrl()}`);
}

function createQuestion(difficulty, question, correctOption, ...incorrectOptions) {
  return {
    difficulty,
    question,
    options: [correctOption, ...incorrectOptions],
    correctIndex: 0,
  };
}

function createCodeQuestion(
  difficulty,
  code,
  correctOption,
  ...incorrectOptions
) {
  return createQuestion(
    difficulty,
    "What is printed?\n\n" + code,
    correctOption,
    ...incorrectOptions,
  );
}

function validateQuestionBank(questions) {
  if (questions.length !== 100) {
    throw new Error(`Question bank must contain 100 questions; found ${questions.length}`);
  }

  const questionTexts = new Set();
  const difficultyCounts = [0, 0, 0];
  let codeQuestionCount = 0;

  questions.forEach((question, index) => {
    if (!question || typeof question.question !== "string" || !question.question.trim()) {
      throw new Error(`Question text is missing at index ${index}`);
    }
    if (![1, 2, 3].includes(question.difficulty)) {
      throw new Error(`Question ${index + 1} has an invalid difficulty`);
    }
    difficultyCounts[question.difficulty - 1] += 1;
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
      const lineCount = question.question.split("\n\n")[1].split("\n").length;
      if (lineCount < 2 || lineCount > 8) {
        throw new Error(`Code question ${index + 1} must contain 2 to 8 lines`);
      }
    }
  });

  if (codeQuestionCount !== 50) {
    throw new Error(`Question bank must contain 50 code questions; found ${codeQuestionCount}`);
  }
  if (difficultyCounts[0] !== 40 || difficultyCounts[1] !== 20 || difficultyCounts[2] !== 40) {
    throw new Error(
      `Internal question distribution must be 40, 20, and 40; found ${JSON.stringify(difficultyCounts)}`,
    );
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
      throw new Error(`Question ${index + 1} was not saved correctly`);
    }
    if (item.getHelpText() !== (code || "")) {
      throw new Error(`Question ${index + 1} code snippet was not saved correctly`);
    }
    const choices = item.getChoices();
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
    correctPositions.push(choices.findIndex((choice) => choice.isCorrectAnswer()));
    if (item.getPoints() !== pointsPerQuestion) {
      throw new Error(`Question ${index + 1} has incorrect points`);
    }
    totalPoints += item.getPoints();
  });
  if (totalPoints !== 100) {
    throw new Error(`Quiz must total 100 points; found ${totalPoints}`);
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
      throw new Error("Could not create a non-patterned balanced answer sequence");
    }

    const selectedSlot =
      candidates[Math.floor(Math.random() * candidates.length)];
    slots.push(selectedSlot);
    remainingCounts[selectedSlot] -= 1;
    previousSlot = selectedSlot;
  }

  return slots;
}

function buildQuestionBank() {
  return [
    // 30 foundational theory questions: concepts 1 through 17.
    createQuestion(1, "What is a Python variable?", "A name bound to an object", "A fixed memory box", "A keyword only", "A function result only"),
    createQuestion(1, "What happens first in an assignment such as total = 4 + 5?", "The right side is evaluated", "The left name is deleted", "The name becomes a type", "The value is copied twice"),
    createQuestion(1, "In Python, where does the type belong?", "To the object", "To every name permanently", "Only to the source code", "Only to the function"),
    createQuestion(1, "Which statement demonstrates rebinding a name to another type?", "value = 3 followed by value = 'three'", "value = 3 followed by print(value)", "value = 3 followed by value + 1", "value = 3 followed by del print"),
    createQuestion(1, "Which character may appear in a Python identifier?", "Underscore", "Space", "Hyphen", "Colon"),
    createQuestion(1, "Which name is invalid because it starts with a digit?", "2nd_place", "second_place", "place2", "_place"),
    createQuestion(1, "Which name cannot be used as an ordinary variable name?", "class", "class_name", "class2", "_class_name"),
    createQuestion(1, "What does Python's case sensitivity mean?", "name and Name are different names", "Every name must use capitals", "Names ignore letter case", "Only keywords are case-sensitive"),
    createQuestion(1, "Which style is the usual convention for variable names?", "snake_case", "PascalCase", "UPPER-CASE", "space separated"),
    createQuestion(1, "Which style is commonly used for class names?", "PascalCase", "snake_case", "lower-dash", "single case"),
    createQuestion(1, "Which style is commonly used for constants?", "UPPER_SNAKE_CASE", "constant-case", "Pascal_snake", "lower space case"),
    createQuestion(1, "What does assignment do to an object by default?", "It binds a name; it does not copy the object", "It always makes a deep copy", "It converts the object to text", "It deletes the original object"),
    createQuestion(1, "If second = first for a list, what do the names initially share?", "The same list object", "Only the list length", "A new tuple", "Different list objects"),
    createQuestion(1, "What is rebinding?", "Making a name refer to another object", "Changing an object's identity in place", "Renaming a keyword", "Copying every nested value"),
    createQuestion(1, "What is mutation?", "Changing an existing object", "Making a name refer elsewhere", "Removing a variable name", "Changing a source-code comment"),
    createQuestion(1, "What normally happens when an immutable integer is incremented?", "A new integer is bound to the name", "The same integer is edited in place", "The integer becomes a list", "All aliases are deleted"),
    createQuestion(1, "What does multiple assignment bind in name, age, active = values?", "Several names in one statement", "Only the last name", "A single class name", "Only global names"),
    createQuestion(1, "For a, b = 1, 2, what must normally match?", "The number of targets and values", "The names' letter cases", "The values' memory addresses", "The variable annotations"),
    createQuestion(1, "What does first = second = [] create?", "Two names for one list", "Two independent lists", "A list and a tuple", "A list with two items"),
    createQuestion(1, "What does sequence unpacking do?", "Binds iterable items to separate names", "Converts every item to a string", "Sorts the sequence", "Deletes the sequence"),
    createQuestion(1, "What type does a starred unpacking target collect?", "list", "tuple", "set", "string"),
    createQuestion(1, "How many starred targets may appear at one unpacking level?", "One", "Two", "Three", "Any number"),
    createQuestion(1, "What is the purpose of left, right = right, left?", "Swap two values without a temporary name", "Add two values", "Make both names equal to zero", "Create two copies of the names"),
    createQuestion(1, "What does augmented assignment such as count += 1 do conceptually?", "Read, operate, then bind or mutate", "Only compare two names", "Always make a deep copy", "Only change the variable's type"),
    createQuestion(1, "What does del name remove?", "The binding of name", "Every reference to the object", "The object's type", "The entire Python process"),
    createQuestion(1, "After del first, can the old object still exist?", "Yes, if another name references it", "No, objects always vanish", "Only if it is an integer", "Only inside a class"),
    createQuestion(1, "What is the main purpose of a variable annotation?", "Document an expected type", "Enforce a type at runtime", "Create a constant", "Make a name global"),
    createQuestion(1, "What does a function parameter become when a function is called?", "A local name bound to the argument object", "A global constant", "A copied class", "A module-level alias only"),
    createQuestion(1, "If a function mutates a list parameter, what may the caller observe?", "The mutation", "Only a new local list", "A syntax error", "Nothing under any condition"),
    createQuestion(1, "If a function rebinds its parameter, what normally changes outside the function?", "Nothing about the caller's binding", "The caller's name always changes", "Every list is cleared", "The argument becomes immutable"),

    // 10 applied theory questions.
    createQuestion(2, "What is the difference between a == b and a is b?", "== tests equality; is tests identity", "== tests identity; is tests length", "Both always test identity", "Both always create copies"),
    createQuestion(2, "Why can a tuple containing a list still show changed list contents?", "The tuple is fixed, but the contained list is mutable", "Tuples always copy their contents", "Lists inside tuples are immutable", "Tuple indexing performs rebinding"),
    createQuestion(2, "What commonly happens to an integer's identity after number += 1?", "It may change because a new integer is created", "It never changes because integers mutate", "It changes only when printed", "The name is deleted"),
    createQuestion(2, "What commonly happens to a list's aliases after items += [2]?", "They can observe the list mutation", "They always point to a new list", "They become tuples", "They are all unbound"),
    createQuestion(2, "Why does a shallow copy not fully isolate nested lists?", "Nested objects are still shared", "The outer list is still shared", "Shallow copies are immutable", "A slice only copies strings"),
    createQuestion(2, "What does a starred target contain in first, *middle, last = data?", "All remaining items as a new list", "Only the second item as a tuple", "The original data object itself", "The first and last items"),
    createQuestion(2, "What do chained names reference when assigned to one mutable object?", "The same object", "Separate deep copies", "Only its first element", "A read-only proxy"),
    createQuestion(2, "What error is raised after reading a name whose binding was deleted?", "NameError", "TypeError", "IndexError", "ValueError"),
    createQuestion(2, "What does a parameter binding receive under Python's object-sharing model?", "A reference to the passed object", "A mandatory deep copy", "Only the object's type", "A text serialization"),
    createQuestion(2, "What can an annotation count: int = 3 be followed by at runtime?", "count = 'three' can still execute", "count becomes permanently integer-only", "count is automatically converted", "count is automatically deleted"),

    // 10 advanced theory questions.
    createQuestion(3, "Why can a local parameter mutation affect the caller while parameter rebinding does not?", "Both names share an object, but rebinding changes only the local name", "Parameters are always copied for rebinding", "Mutation changes only names, not objects", "The caller sees only immutable changes"),
    createQuestion(3, "What does an assignment statement bind when its right side is a list expression?", "The target name to the newly created list", "The target name to the list's source text", "Every existing alias to the new list", "The list to a fixed variable type"),
    createQuestion(3, "If a = b = [] and a = [1], what is b?", "The original empty list", "[1] because chained names stay linked", "An unbound name", "A tuple containing the lists"),
    createQuestion(3, "Why does x, *middle, y = [1, 2, 3, 4] work?", "The starred target absorbs the middle items", "The starred target absorbs every item", "The assignment silently drops item 3", "The values are first sorted"),
    createQuestion(3, "What does identity_before = id(items) help test after items.append(3)?", "Whether mutation preserved the object's identity", "Whether the list was deeply copied", "Whether the name became global", "Whether the list became immutable"),
    createQuestion(3, "What does an annotation change by itself?", "Documentation and metadata, not runtime type enforcement", "The object's runtime type", "The binding's scope", "The object's mutability"),
    createQuestion(3, "Why does del first not necessarily destroy a list?", "Object lifetime depends on remaining references", "del always affects names only in functions", "Lists are never destroyed", "The list is converted to a tuple"),
    createQuestion(3, "In left, right = right, left, why is the original left value not lost before the swap?", "The right side is evaluated before the targets are bound", "Python assigns targets from left to right immediately", "Python stores all variables globally", "Tuple unpacking mutates both names"),
    createQuestion(3, "What is the key risk of chained assignment with a mutable value?", "An unexpected mutation can be visible through every chained name", "The code always raises TypeError", "Only the last name gets the value", "The mutable object becomes immutable"),
    createQuestion(3, "What best describes a function's local parameter after items = [9] inside the function?", "The local name is rebound; the caller's name remains unchanged", "The caller's name is rebound automatically", "The original list is always mutated", "The parameter becomes a global name"),

    // 10 foundational code questions.
    createCodeQuestion(1, "score = 95\nprint(score)", "Output: 95", "Output: score", "Output: None", "Output: NameError"),
    createCodeQuestion(1, "value = 10\nvalue = 'complete'\nprint(value)", "Output: complete", "Output: 10", "Output: 10 complete", "Output: TypeError"),
    createCodeQuestion(1, "user_name = 'Ana'\nprint(user_name)", "Output: Ana", "Output: user_name", "Output: 'user_name'", "Output: NameError"),
    createCodeQuestion(1, "name = 'lower'\nName = 'upper'\nprint(name, Name)", "Output: lower upper", "Output: upper lower", "Output: lower lower", "Output: NameError"),
    createCodeQuestion(1, "item_count = 3\nunit_price = 10\ntotal_price = item_count * unit_price\nprint(total_price)", "Output: 30", "Output: 13", "Output: 3000", "Output: TypeError"),
    createCodeQuestion(1, "first = [1, 2]\nsecond = first\nprint(first is second)", "Output: True", "Output: False", "Output: [1, 2]", "Output: None"),
    createCodeQuestion(1, "first = [1, 2]\nsecond = first\nsecond = [9, 10]\nprint(first)", "Output: [1, 2]", "Output: [9, 10]", "Output: [1, 2, 9, 10]", "Output: NameError"),
    createCodeQuestion(1, "numbers = [1, 2]\nidentity_before = id(numbers)\nnumbers.append(3)\nprint(numbers)", "Output: [1, 2, 3]", "Output: [1, 2]", "Output: 3", "Output: None"),
    createCodeQuestion(1, "name, age, active = 'Ana', 25, True\nprint(name, age, active)", "Output: Ana 25 True", "Output: True 25 Ana", "Output: ('Ana', 25, True)", "Output: TypeError"),
    createCodeQuestion(1, "point = (4, 7)\nx, y = point\nprint(x, y)", "Output: 4 7", "Output: (4, 7)", "Output: 7 4", "Output: ValueError"),

    // 10 applied code questions.
    createCodeQuestion(2, "first, *middle, last = [1, 2, 3, 4, 5]\nprint(first, middle, last)", "Output: 1 [2, 3, 4] 5", "Output: 1 (2, 3, 4) 5", "Output: [1] [2, 3, 4] [5]", "Output: 2 [1, 3, 4] 5"),
    createCodeQuestion(2, "left = 10\nright = 20\nleft, right = right, left\nprint(left, right)", "Output: 20 10", "Output: 10 20", "Output: 30 30", "Output: (20, 10)"),
    createCodeQuestion(2, "first = second = []\nfirst.append('shared')\nprint(second)", "Output: ['shared']", "Output: []", "Output: ['first']", "Output: NameError"),
    createCodeQuestion(2, "a = [6]\nb = a\nc = [6]\nprint(a is b, a == c)", "Output: True True", "Output: False True", "Output: True False", "Output: False False"),
    createCodeQuestion(2, "x = [[7], [8]]\ny = x[:]\ny.append([9])\nprint(x, y)", "Output: [[7], [8]] [[7], [8], [9]]", "Output: [[7], [8], [9]] [[7], [8], [9]]", "Output: [[7], [8, 9]] [[7], [8]]", "Output: [[9]] [[7], [8]]"),
    createCodeQuestion(2, "x = [[8], [9]]\ny = x[:]\ny[0].append(10)\nprint(x)", "Output: [[8, 10], [9]]", "Output: [[8], [9]]", "Output: [[10], [9]]", "Output: TypeError"),
    createCodeQuestion(2, "t = ([9], 'k')\nt[0].append(10)\nprint(t)", "Output: ([9, 10], 'k')", "Output: ([9], 'k', 10)", "Output: TypeError", "Output: ('k', [9, 10])"),
    createCodeQuestion(2, "a = [10]\nb = a\ndel a\nprint(b)", "Output: [10]", "Output: []", "Output: NameError", "Output: None"),
    createCodeQuestion(2, "count: int = 3\ncount = 'three'\nprint(count, type(count).__name__)", "Output: three str", "Output: 3 int", "Output: three int", "Output: TypeError"),
    createCodeQuestion(2, "def append_item(items):\n    items.append(3)\noriginal = [1, 2]\nappend_item(original)\nprint(original)", "Output: [1, 2, 3]", "Output: [1, 2]", "Output: [3]", "Output: None"),

    // 30 advanced code questions.
    createCodeQuestion(3, "a = [1, 2]\nb = a\nb = [9, 10]\nprint(a, b, a is b)", "Output: [1, 2] [9, 10] False", "Output: [9, 10] [9, 10] True", "Output: [1, 2, 9, 10] [9, 10] False", "Output: [1, 2] [1, 2] True"),
    createCodeQuestion(3, "numbers = [1, 2]\nidentity_before = id(numbers)\nnumbers.append(3)\nprint(id(numbers) == identity_before)", "Output: True", "Output: False", "Output: 3", "Output: None"),
    createCodeQuestion(3, "number = 10\nidentity_before = id(number)\nnumber += 1\nprint(number, id(number) == identity_before)", "Output: 11 False", "Output: 11 True", "Output: 10 False", "Output: TypeError"),
    createCodeQuestion(3, "items = [1]\nalias = items\nitems += [2]\nprint(items, alias, items is alias)", "Output: [1, 2] [1, 2] True", "Output: [1, 2] [1] False", "Output: [1] [1] True", "Output: [2] [2] True"),
    createCodeQuestion(3, "items = [1]\nalias = items\nitems = items + [2]\nprint(items, alias, items is alias)", "Output: [1, 2] [1] False", "Output: [1, 2] [1, 2] True", "Output: [1] [1, 2] False", "Output: [2] [1] True"),
    createCodeQuestion(3, "first = second = []\nfirst = [1]\nsecond.append(2)\nprint(first, second)", "Output: [1] [2]", "Output: [1, 2] [1, 2]", "Output: [] [2]", "Output: [1] []"),
    createCodeQuestion(3, "first = second = []\nfirst.append(1)\nsecond = [2]\nprint(first, second)", "Output: [1] [2]", "Output: [1, 2] [1, 2]", "Output: [] [2]", "Output: [1] []"),
    createCodeQuestion(3, "first, *middle, last = [1, 2, 3, 4]\nmiddle.append(9)\nprint(first, middle, last)", "Output: 1 [2, 3, 9] 4", "Output: 1 [2, 3] 9", "Output: [1] [2, 3, 4, 9] []", "Output: 1 (2, 3, 9) 4"),
    createCodeQuestion(3, "left = [1]\nright = [2]\nleft, right = right, left\nright.append(3)\nprint(left, right)", "Output: [2] [1, 3]", "Output: [1, 3] [2]", "Output: [2, 3] [1]", "Output: [1] [2, 3]"),
    createCodeQuestion(3, "a = [1]\nb = a\nc = a[:]\nc.append(2)\na.append(3)\nprint(a, b, c)", "Output: [1, 3] [1, 3] [1, 2]", "Output: [1, 2, 3] [1, 2, 3] [1, 2, 3]", "Output: [1, 3] [1] [1, 2]", "Output: [1] [1] [1, 2, 3]"),
    createCodeQuestion(3, "x = [[1], [2]]\ny = x.copy()\ny[0].append(3)\ny.append([4])\nprint(x, y)", "Output: [[1, 3], [2]] [[1, 3], [2], [4]]", "Output: [[1], [2]] [[1], [2], [4]]", "Output: [[1, 3], [2], [4]] [[1, 3], [2], [4]]", "Output: [[1], [2, 3]] [[1], [2], [4]]"),
    createCodeQuestion(3, "a = [1]\nb = a\ndel a\ntry:\n    print(a)\nexcept NameError as error:\n    print(type(error).__name__)", "Output: NameError", "Output: [1]", "Output: None", "Output: TypeError"),
    createCodeQuestion(3, "def replace(values):\n    values = [9]\n    return values\ndata = [1, 2]\nresult = replace(data)\nprint(data, result)", "Output: [1, 2] [9]", "Output: [9] [1, 2]", "Output: [9] [9]", "Output: [1, 2] None"),
    createCodeQuestion(3, "def mutate(values):\n    values.append(9)\n    values = [0]\n    return values\ndata = [1, 2]\nresult = mutate(data)\nprint(data, result)", "Output: [1, 2, 9] [0]", "Output: [0] [1, 2, 9]", "Output: [1, 2] [0]", "Output: [1, 2, 9] None"),
    createCodeQuestion(3, "def f(value):\n    value += 1\n    return value\nnumber = 5\nresult = f(number)\nprint(number, result)", "Output: 5 6", "Output: 6 6", "Output: 5 5", "Output: TypeError"),
    createCodeQuestion(3, "def f(value):\n    value.append(1)\n    return value\nitems = []\nresult = f(items)\nprint(items is result, items)", "Output: True [1]", "Output: False [1]", "Output: True []", "Output: False []"),
    createCodeQuestion(3, "def f(value):\n    value = value + [2]\n    return value\nitems = [1]\nresult = f(items)\nprint(items, result, items is result)", "Output: [1] [1, 2] False", "Output: [1, 2] [1, 2] True", "Output: [1, 2] [1] False", "Output: [1] [1, 2] True"),
    createCodeQuestion(3, "def f(value):\n    value += [2]\n    return value\nitems = [1]\nresult = f(items)\nprint(items, result, items is result)", "Output: [1, 2] [1, 2] True", "Output: [1] [1, 2] False", "Output: [1, 2] [1] False", "Output: [2] [2] True"),
    createCodeQuestion(3, "def f(value):\n    value += 1\n    return value\nitems = [1]\ntry:\n    f(items)\nexcept TypeError as error:\n    print(type(error).__name__)", "Output: TypeError", "Output: [1, 1]", "Output: 2", "Output: NameError"),
    createCodeQuestion(3, "count: int = 3\ncount = 'three'\nprint(type(count).__name__)\nprint(count)", "Output: str then three", "Output: int then 3", "Output: int then three", "Output: TypeError"),
    createCodeQuestion(3, "a = [1]\nb = a\nc = [1]\nprint(a == b, a is b)\nprint(a == c, a is c)", "Output: True True then True False", "Output: True False then False True", "Output: False True then True False", "Output: False False then False False"),
    createCodeQuestion(3, "value = [1, 2]\nfirst, *middle = value\nmiddle.append(3)\nprint(value, middle)", "Output: [1, 2] [2, 3]", "Output: [1, 2, 3] [2, 3]", "Output: [1] [2, 3]", "Output: [1, 2] (2, 3)"),
    createCodeQuestion(3, "a = [1, 2]\nb = a\na = a[:]\na.append(3)\nb.append(4)\nprint(a, b)", "Output: [1, 2, 3] [1, 2, 4]", "Output: [1, 2, 3, 4] [1, 2, 3, 4]", "Output: [1, 2] [1, 2, 3, 4]", "Output: [1, 2, 4] [1, 2, 3]"),
    createCodeQuestion(3, "def f(items):\n    items = items[:]\n    items.append(9)\n    return items\noriginal = [1]\nresult = f(original)\nprint(original, result, original is result)", "Output: [1] [1, 9] False", "Output: [1, 9] [1, 9] True", "Output: [1, 9] [1] False", "Output: [1] [1, 9] True"),
    createCodeQuestion(3, "def f(items):\n    items.append(9)\n    items = items[:]\n    items.append(10)\n    return items\noriginal = [1]\nresult = f(original)\nprint(original, result)", "Output: [1, 9] [1, 9, 10]", "Output: [1, 9, 10] [1, 9, 10]", "Output: [1] [1, 9, 10]", "Output: [1, 9] [1, 10]"),
    createCodeQuestion(3, "a = b = [1]\nb = b + [2]\na.append(3)\nprint(a, b, a is b)", "Output: [1, 3] [1, 2] False", "Output: [1, 2, 3] [1, 2, 3] True", "Output: [1] [1, 2, 3] False", "Output: [1, 3] [1, 3] True"),
    createCodeQuestion(3, "a = b = [1]\nb += [2]\na.append(3)\nprint(a, b, a is b)", "Output: [1, 2, 3] [1, 2, 3] True", "Output: [1, 3] [1, 2] False", "Output: [1] [1, 2, 3] False", "Output: [1, 2] [1, 3] False"),
    createCodeQuestion(3, "def f(items):\n    print(items is original)\n    items.append(3)\noriginal = [1, 2]\nf(original)", "Output: True then [1, 2, 3] is the final original", "Output: False then [1, 2] is the final original", "Output: True then [3] is the final original", "Output: TypeError before printing"),
    createCodeQuestion(3, "def replace(items):\n    items = [9]\n    print(items)\noriginal = [1, 2]\nreplace(original)\nprint(original)", "Output: [9] then [1, 2]", "Output: [1, 2] then [9]", "Output: [9] then [9]", "Output: None then [1, 2]"),
    createCodeQuestion(3, "a = [1]\nb = a\nc = b\nb = [2]\nc.append(3)\nprint(a, b, c)", "Output: [1] [2] [1, 3]", "Output: [1, 2, 3] [2] [1, 3]", "Output: [1] [1, 3] [2]", "Output: [2] [2] [2, 3]"),
  ];
}
