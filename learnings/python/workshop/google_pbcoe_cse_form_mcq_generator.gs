/**
 * Google Apps Script: Generate PBCOE VAC Assessment No.1 Python MCQ Quiz.
 * Scope: Datatypes.md, variables model.md, and list.md through List Comprehension.
 */

function createPythonConceptsQuizForm() {
  createPbcoeVacAssessmentNo1();
}

function createPbcoeVacAssessmentNo1() {
  const config = {
    title: "PBCOE VAC Assessment No.1 Python MCQ Quiz",
    description: `Instructions:
• Total Questions: 100
• Each question carries 1 mark.
• All questions are mandatory.
• No negative marking.
• Passing Criteria: Minimum 40 out of 100 marks (40%).
• Submit the form only after answering all questions.
• Responses cannot be edited after submission.`,
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

  form.addPageBreakItem().setTitle("Python MCQ Quiz");

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
  return { question, options: [correctOption, ...incorrectOptions], correctIndex: 0 };
}

function createCodeQuestion(code, correctOption, ...incorrectOptions) {
  return createQuestion("What is printed?\n\n" + code, correctOption, ...incorrectOptions);
}

function validateQuestionBank(questions) {
  if (questions.length !== 100) {
    throw new Error(`Question bank must contain 100 questions; found ${questions.length}`);
  }

  const questionTexts = new Set();
  const optionTexts = new Set();
  let codeQuestionCount = 0;

  questions.forEach((question, index) => {
    if (!question || typeof question.question !== "string" || !question.question.trim()) {
      throw new Error(`Question text is missing at index ${index}`);
    }
    if (!Array.isArray(question.options) || question.options.length !== 4) {
      throw new Error(`Question ${index + 1} must have exactly four options`);
    }
    if (!Number.isInteger(question.correctIndex) || question.correctIndex < 0 || question.correctIndex > 3) {
      throw new Error(`Question ${index + 1} has an invalid correct answer index`);
    }

    const normalizedQuestion = normalize(question.question);
    if (questionTexts.has(normalizedQuestion)) {
      throw new Error(`Duplicate question detected: ${question.question}`);
    }
    questionTexts.add(normalizedQuestion);

    if (question.question.includes("\n\n")) {
      codeQuestionCount += 1;
      const lineCount = question.question.split("\n\n")[1].split("\n").length;
      if (lineCount < 2 || lineCount > 5) {
        throw new Error(`Code question ${index + 1} must contain 2 to 5 lines`);
      }
    }

    question.options.forEach((option) => {
      if (typeof option !== "string" || !option.trim()) {
        throw new Error(`Question ${index + 1} has an invalid option`);
      }
      const normalizedOption = normalize(option);
      if (optionTexts.has(normalizedOption)) {
        throw new Error(`Repeated option detected: ${option}`);
      }
      optionTexts.add(normalizedOption);
    });
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
    throw new Error(`Generated ${items.length} MCQs; expected ${questions.length}`);
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
      throw new Error(`Question ${index + 1} must have exactly one correct choice`);
    }
    if (item.getPoints() !== pointsPerQuestion) {
      throw new Error(`Question ${index + 1} has incorrect points`);
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

function buildQuestionBank() {
  return [
    // 50 concise theory questions
    createQuestion("Which list property allows changes after creation?", "Mutable", "Immutable", "Static", "Scalar"),
    createQuestion("Which list property supports index-based access?", "Ordered", "Unordered", "Keyed", "Random"),
    createQuestion("Which term means a list can hold mixed types?", "Heterogeneous", "Homogeneous", "Single type", "Boolean"),
    createQuestion("What does list() create without an argument?", "Empty list", "Empty tuple", "Null list", "Zero list"),
    createQuestion("What must list(value) receive?", "Iterable", "Hashable", "Callable", "Numeric"),
    createQuestion("Which error follows a bad direct list index?", "IndexError", "KeyError", "TypeError", "NameError"),
    createQuestion("In slicing, what happens to the end index?", "Excluded", "Included", "Reversed", "Duplicated"),
    createQuestion("What does index -1 select?", "Last item", "First item", "Middle item", "No item"),
    createQuestion("What does append add?", "One item", "All items", "Front item", "Unique item"),
    createQuestion("What does extend add?", "Separate items", "Nested item", "Random items", "Sorted items"),
    createQuestion("Where does insert place a value?", "Given index", "Final index", "Zero index", "Random index"),
    createQuestion("What does remove delete?", "First match", "Last match", "All matches", "Given value"),
    createQuestion("What does pop() return?", "Tail value", "Head value", "Whole list", "No value"),
    createQuestion("What remains after clear()?", "[]", "()", "{}", "None"),
    createQuestion("What does b = a create for a list?", "Alias created", "Full clone", "New tuple", "No binding"),
    createQuestion("What does a shallow copy share?", "Inner shared", "Outer shared", "Nothing shared", "All copied"),
    createQuestion("What does deepcopy provide?", "Nested independent", "Alias retained", "Outer only", "Syntax fail"),
    createQuestion("What does is compare?", "Same object", "Same value", "Same type", "Same size"),
    createQuestion("What does == compare?", "Equal values", "Equal ids", "Equal names", "Equal hashes"),
    createQuestion("What is Python argument passing called?", "Call sharing", "Local copy", "Global copy", "Value clone"),
    createQuestion("What does integer += 1 create?", "New integer", "Mutated integer", "List result", "Shared change"),
    createQuestion("What does list += [x] usually do?", "In place", "Fresh binding", "No change", "Type error"),
    createQuestion("What is list membership complexity?", "Linear time", "Constant time", "Log time", "Square time"),
    createQuestion("What must follow + for list concatenation?", "List operand", "Integer operand", "Set operand", "String operand"),
    createQuestion("What does list * 2 perform?", "Sequence repeat", "Numeric sum", "Value sort", "Deep clone"),
    createQuestion("What does reverse() do?", "Mutates list", "Returns copy", "Sorts list", "Drops values"),
    createQuestion("What does sorted() return?", "New result", "No result", "Same list", "Tuple output"),
    createQuestion("What does sort() return?", "Returns None", "Returns tuple", "Returns index", "Returns boolean"),
    createQuestion("What does count(value) report?", "Occurrence count", "First position", "Ending slot", "Truth value"),
    createQuestion("What does index(value) report?", "Starting position", "Item count", "Final slot", "Object id"),
    createQuestion("What does enumerate provide?", "Index value", "Value index", "Index only", "Values only"),
    createQuestion("What order does reversed(items) provide?", "Backward order", "Forward order", "Random order", "Sorted order"),
    createQuestion("What is a list comprehension useful for?", "Concise build", "Loop error", "In-place only", "Auto unique"),
    createQuestion("Which keyword filters a comprehension?", "If clause", "Else clause", "Try clause", "With clause"),
    createQuestion("What can a nested comprehension do?", "Flatten rows", "Copy rows", "Sort rows", "Delete rows"),
    createQuestion("What does [[0] * 3] * 3 create?", "Shared rows", "Unique rows", "Tuple rows", "Empty rows"),
    createQuestion("Which syntax makes a slice copy?", "Slice copy", "Tuple copy", "Set copy", "Name copy"),
    createQuestion("What does list(\"Ada\") produce?", "Characters", "Words", "Bytes", "Numbers"),
    createQuestion("What is the first value from range(5)?", "Zero start", "One start", "Five start", "Negative start"),
    createQuestion("How do min and max compare strings?", "Lexicographic", "Arithmetic", "Lengthwise", "Identity"),
    createQuestion("What is a Python variable?", "Reference label", "Value container", "Primitive slot", "Heap object"),
    createQuestion("How are Python values modeled?", "Universal object", "Raw primitive", "Stack literal", "Fixed address"),
    createQuestion("What is rebinding?", "New binding", "Shared mutation", "List deletion", "Value sorting"),
    createQuestion("What is mutation?", "Existing object", "Fresh object", "Copied name", "Freed object"),
    createQuestion("Which function copies nested lists independently?", "Deep copy", "Slice alias", "Name alias", "List view"),
    createQuestion("Which pattern safely creates grid rows?", "Row comprehension", "Row multiplication", "Row append", "Row extension"),
    createQuestion("Which slice step reverses a list?", "Negative step", "Positive step", "Zero step", "Missing step"),
    createQuestion("Which error follows remove on an absent value?", "Missing value", "Missing index", "Missing key", "Missing name"),
    createQuestion("Which error follows pop on an empty list?", "Empty index", "Empty value", "Empty key", "Empty type"),
    createQuestion("Which error follows index on an absent value?", "Absent value", "Absent object", "Absent slice", "Absent alias"),

    // 50 code-snippet questions
    createCodeQuestion("items = [1, 2]\nitems.append(3)\nprint(items)", "Output: [1, 2, 3]", "Output: [3, 1, 2]", "Output: [1, 2]", "Output: [1, 2, [3]]"),
    createCodeQuestion("items = [4]\nitems.append([5, 6])\nprint(items)", "Output: [4, [5, 6]]", "Output: [4, 5, 6]", "Output: [[4], [5, 6]]", "Output: [5, 6, 4]"),
    createCodeQuestion("items = [7]\nitems.extend([8, 9])\nprint(items)", "Output: [7, 8, 9]", "Output: [7, [8, 9]]", "Output: [9, 8, 7]", "Output: [8, 9]"),
    createCodeQuestion("items = [10, 20]\nitems.insert(1, 15)\nprint(items)", "Output: [10, 15, 20]", "Output: [15, 10, 20]", "Output: [10, 20, 15]", "Output: [10, 20]"),
    createCodeQuestion("items = [11, 12, 12, 13]\nitems.remove(12)\nprint(items)", "Output: [11, 12, 13]", "Output: [11, 13]", "Output: [11, 12, 12, 13]", "Output: [12, 12, 13]"),
    createCodeQuestion("items = [14, 15, 16]\nvalue = items.pop()\nprint(value, items)", "Output: 16 [14, 15]", "Output: 14 [15, 16]", "Output: 15 [14, 16]", "Output: 16 [14, 15, 16]"),
    createCodeQuestion("items = [17, 18]\nitems.clear()\nprint(items)", "Output: [] after clear", "Output: [17, 18] after clear", "Output: None after clear", "Output: [0] after clear"),
    createCodeQuestion("nums = [19, 20, 21, 22, 23]\nprint(nums[1:4])", "Output: [20, 21, 22]", "Output: [19, 20, 21, 22]", "Output: [21, 22, 23]", "Output: [20, 21, 22, 23]"),
    createCodeQuestion("nums = [24, 25, 26]\nprint(nums[-1])", "Output: 26", "Output: 24", "Output: -1", "Output: IndexError"),
    createCodeQuestion("nums = [27, 28, 29]\nprint(nums[::-1])", "Output: [29, 28, 27]", "Output: [27, 28, 29]", "Output: [28, 29, 27]", "Output: [27, 29, 28]"),
    createCodeQuestion("fruits = ['apple', 'banana']\nfruits[1] = 'berry'\nprint(fruits)", "Output: ['apple', 'berry']", "Output: ['berry', 'banana']", "Output: ['apple', 'banana', 'berry']", "Output: TypeError"),
    createCodeQuestion("values = [30, 31, 32]\nvalues[1:3] = [99]\nprint(values)", "Output: [30, 99]", "Output: [30, 99, 31, 32]", "Output: [30, 31, 99, 32]", "Output: [99, 30]"),
    createCodeQuestion("letters = list('Ada')\nprint(letters)", "Output: ['A', 'd', 'a']", "Output: ['Ada']", "Output: ('A', 'd', 'a')", "Output: Ada"),
    createCodeQuestion("numbers = list(range(4))\nprint(numbers)", "Output: [0, 1, 2, 3]", "Output: [1, 2, 3, 4]", "Output: [0, 1, 2, 3, 4]", "Output: range(4)"),
    createCodeQuestion("left = [33, 34]\nright = [35]\nprint(left + right)", "Output: [33, 34, 35]", "Output: [68, 35]", "Output: [[33, 34], [35]]", "Output: TypeError for plus"),
    createCodeQuestion("values = [36, 37]\nprint(values * 2)", "Output: [36, 37, 36, 37]", "Output: [72, 74]", "Output: [[36, 37], 2]", "Output: [36, 37, 2]"),
    createCodeQuestion("fruits = ['mango', 'pear']\nprint('mango' in fruits)", "Output: True", "Output: False", "Output: mango", "Output: 1"),
    createCodeQuestion("values = [38, 39, 40]\nprint(len(values))", "Output: length 3", "Output: length 117", "Output: length 40", "Output: length [3]"),
    createCodeQuestion("values = [41, 7, 18]\nprint(min(values))", "Output: minimum 7", "Output: minimum 41", "Output: minimum 18", "Output: minimum [7]"),
    createCodeQuestion("values = [9, 13, 12]\nprint(max(values))", "Output: maximum 13", "Output: maximum 9", "Output: maximum 12", "Output: maximum [13]"),
    createCodeQuestion("values = [4, 5, 6]\nprint(sum(values))", "Output: sum 15", "Output: sum 6", "Output: sum 456", "Output: sum [15]"),
    createCodeQuestion("values = [42, 43, 44]\nvalues.reverse()\nprint(values)", "Output: [44, 43, 42]", "Output: [42, 43, 44]", "Output: [43, 44, 42]", "Output: None"),
    createCodeQuestion("values = [45, 46, 47]\nprint(list(reversed(values)))", "Output: [47, 46, 45]", "Output: [45, 46, 47]", "Output: [46, 47, 45]", "Output: reversed(values)"),
    createCodeQuestion("values = [3, 1, 2]\nvalues.sort()\nprint(values)", "Output: sorted [1, 2, 3]", "Output: sorted [3, 1, 2]", "Output: sorted [3, 2, 1]", "Output: sorted None"),
    createCodeQuestion("values = [49, 48, 50]\nordered = sorted(values)\nprint(ordered, values)", "Output: [48, 49, 50] [49, 48, 50]", "Output: [48, 49, 50] [48, 49, 50]", "Output: [49, 48, 50] [48, 49, 50]", "Output: None [49, 48, 50]"),
    createCodeQuestion("items = ['x', 'y', 'x']\nprint(items.count('x'))", "Output: count 2", "Output: count 1", "Output: count 3", "Output: count -1"),
    createCodeQuestion("items = ['a', 'b', 'a']\nprint(items.index('a', 1))", "Output: index 2", "Output: index 0", "Output: index 1", "Output: index -1"),
    createCodeQuestion("items = ['p', 'q']\nprint(list(enumerate(items)))", "Output: [(0, 'p'), (1, 'q')]", "Output: [('p', 0), ('q', 1)]", "Output: ['p', 'q']", "Output: [0, 1]"),
    createCodeQuestion("items = [51, 52, 53]\nprint(list(reversed(items)))", "Output: [53, 52, 51]", "Output: [51, 52, 53]", "Output: [52, 53, 51]", "Output: [51, 53, 52]"),
    createCodeQuestion("values = [1, 2, 3]\nsquares = [x * x for x in values]\nprint(squares)", "Output: squares [1, 4, 9]", "Output: squares [2, 4, 6]", "Output: squares [1, 2, 3]", "Output: squares [1, 8, 27]"),
    createCodeQuestion("values = [4, 5, 6]\neven = [x for x in values if x % 2 == 0]\nprint(even)", "Output: even [4, 6]", "Output: even [5]", "Output: even [4, 5, 6]", "Output: even []"),
    createCodeQuestion("values = [2, 3, 4]\nresult = [x * 2 for x in values if x > 2]\nprint(result)", "Output: mapped [6, 8]", "Output: mapped [4, 6, 8]", "Output: mapped [3, 4]", "Output: mapped [2, 3, 4]"),
    createCodeQuestion("values = [1, 2, 3]\nlabels = ['even' if x % 2 == 0 else 'odd' for x in values]\nprint(labels)", "Output: labels ['odd', 'even', 'odd']", "Output: labels ['even', 'odd', 'even']", "Output: labels ['odd', 'odd', 'odd']", "Output: labels ['even', 'even', 'even']"),
    createCodeQuestion("matrix = [[1, 2], [3, 4]]\nflat = [item for row in matrix for item in row]\nprint(flat)", "Output: flat [1, 2, 3, 4]", "Output: flat [[1, 2], [3, 4]]", "Output: flat [1, 3]", "Output: flat [2, 4]"),
    createCodeQuestion("grid = [[0 for _ in range(2)] for _ in range(2)]\ngrid[0][1] = 8\nprint(grid)", "Output: [[0, 8], [0, 0]]", "Output: [[0, 8], [0, 8]]", "Output: [[8, 0], [0, 0]]", "Output: [[0, 0], [0, 8]]"),
    createCodeQuestion("grid = [[0] * 2] * 2\ngrid[0][1] = 9\nprint(grid)", "Output: [[0, 9], [0, 9]]", "Output: [[0, 9], [0, 0]]", "Output: [[9, 0], [9, 0]]", "Output: [[0, 0], [0, 9]]"),
    createCodeQuestion("a = [54, 55]\nb = a\nb.append(56)\nprint(a)", "Output: alias [54, 55, 56]", "Output: alias [54, 55]", "Output: alias [56]", "Output: alias TypeError"),
    createCodeQuestion("a = [[57], [58]]\nb = a[:]\nb[0].append(59)\nprint(a)", "Output: shared [[57, 59], [58]]", "Output: shared [[57], [58]]", "Output: shared [[59], [58]]", "Output: shared [[57], [58, 59]]"),
    createCodeQuestion("import copy\na = [[60], [61]]\nb = copy.deepcopy(a)\nb[0].append(62)\nprint(a)", "Output: deep [[60], [61]]", "Output: deep [[60, 62], [61]]", "Output: deep [[62], [61]]", "Output: deep TypeError"),
    createCodeQuestion("def add_item(values):\n    values.append(63)\ndata = [64]\nadd_item(data)\nprint(data)", "Output: function [64, 63]", "Output: function [64]", "Output: function [63]", "Output: function None"),
    createCodeQuestion("def replace(values):\n    values = [65]\ndata = [66]\nreplace(data)\nprint(data)", "Output: rebind [66]", "Output: rebind [65]", "Output: rebind [65, 66]", "Output: rebind None"),
    createCodeQuestion("a = [67]\nb = [67]\nprint(a == b, a is b)", "Output: True False", "Output: True True", "Output: False True", "Output: False False"),
    createCodeQuestion("a = [68]\nb = a\nprint(a is b)", "Output: identity True", "Output: identity False", "Output: identity 68", "Output: identity None"),
    createCodeQuestion("items = [69]\nalias = items\nitems += [70]\nprint(alias)", "Output: plus-equals [69, 70]", "Output: plus-equals [69]", "Output: plus-equals [70]", "Output: plus-equals TypeError"),
    createCodeQuestion("items = [71]\nalias = items\nitems = items + [72]\nprint(alias)", "Output: plus [71]", "Output: plus [71, 72]", "Output: plus [72]", "Output: plus None"),
    createCodeQuestion("original = [73, 74]\ncopied = original.copy()\ncopied[0] = 75\nprint(original)", "Output: copy [73, 74]", "Output: copy [75, 74]", "Output: copy [73, 75]", "Output: copy TypeError"),
    createCodeQuestion("items = [76, 77]\nresult = items.remove(76)\nprint(result, items)", "Output: None [77]", "Output: 76 [77]", "Output: None [76, 77]", "Output: 77 [76]"),
    createCodeQuestion("items = [78, 79, 80]\nresult = items.pop(1)\nprint(result, items)", "Output: 79 [78, 80]", "Output: 78 [79, 80]", "Output: 80 [78, 79]", "Output: 79 [78, 79, 80]"),
    createCodeQuestion("items = [81, 82]\nprint(items[5:9])", "Output: out-of-range []", "Output: out-of-range IndexError", "Output: out-of-range [82]", "Output: out-of-range None"),
    createCodeQuestion("items = [83, 84, 85, 86]\ndel items[1:3]\nprint(items)", "Output: deletion [83, 86]", "Output: deletion [83, 84, 85, 86]", "Output: deletion [84, 85]", "Output: deletion [83, 85, 86]"),
  ];
}
