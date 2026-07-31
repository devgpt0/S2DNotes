/**
 * Generates the RCOE VAC Assessment Frontend Quiz.
 * Google Forms has no native timer, so the 30-minute limit is shown in the instructions.
 */

function createRcoeFrontendQuizForm() {
  const config = {
    title: "RCOE VAC Assessment Frontend Quiz",
    description: [
      "Total Score: 100 marks.",
      "Instructions:",
      "â€¢ Total Questions: 60",
      "â€¢ Duration: 30 minutes.",
      "â€¢ All questions are mandatory.",
      "â€¢ No negative marking.",
      "â€¢ Responses cannot be edited after submission.",
    ].join("\n"),
    onePointQuestionCount: 20,
    onePointValue: 1,
    twoPointValue: 2,
    totalPoints: 100,
  };
  const questions = buildQuestionBank();
  validateQuestionBank(questions);
  if (calculateTotalPoints(questions.length, config) !== config.totalPoints) {
    throw new Error("Question count and point configuration do not total 100.");
  }

  const form = FormApp.create(config.title)
    .setDescription(config.description)
    .setIsQuiz(true)
    .setShuffleQuestions(false)
    .setCollectEmail(true)
    .setProgressBar(true)
    .setAllowResponseEdits(false)
    .setLimitOneResponsePerUser(true);

  addSectionOne(form);
  form.addPageBreakItem().setTitle("Frontend MCQ Quiz");

  questions.forEach((question, index) => {
    const item = form.addMultipleChoiceItem();
    const choices = question.options.map((option, optionIndex) => ({
      option,
      isCorrect: optionIndex === question.correctIndex,
    }));
    shuffle(choices);
    item
      .setTitle(String(index + 1) + ". " + question.question)
      .setChoices(
        choices.map(({ option, isCorrect }) =>
          item.createChoice(option, isCorrect),
        ),
      )
      .setRequired(true)
      .setPoints(pointsForQuestion(index, config));
  });

  verifyGeneratedQuestions(form, questions, config);
  Logger.log("Form created: " + form.getPublishedUrl());
  Logger.log("Edit URL: " + form.getEditUrl());
}

function addSectionOne(form) {
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
      "Artificial Intelligence and Data Science",
      "Information Technology",
      "Electronics and Communication",
      "Electrical Engineering",
      "Mechanical Engineering",
      "Civil Engineering",
      "Other",
    ].map((department) => departmentItem.createChoice(department)),
  );

  const yearItem = form.addListItem();
  yearItem.setTitle("Student Pass-out Year").setRequired(true);
  yearItem.setChoices(
    ["2026", "2027", "2028", "2029", "2030"].map((year) =>
      yearItem.createChoice(year),
    ),
  );

  const interestItem = form.addMultipleChoiceItem();
  interestItem
    .setTitle(
      "How many of you are interested in knowing about Bootcoding Courses.",
    )
    .setChoices(
      ["Very interested", "Interested", "Not sure", "Not interested"].map(
        (option) => interestItem.createChoice(option),
      ),
    )
    .setRequired(true);
}

function createQuestion(category, question, correct, wrong1, wrong2, wrong3) {
  return {
    category,
    question,
    options: [correct, wrong1, wrong2, wrong3],
    correctIndex: 0,
  };
}

function buildQuestionBank() {
  const javascript = [
    ["What can a const object binding still allow?", "Changing an object property", "Reassigning the variable", "Deleting the object automatically", "Changing the object to a number"],
    ["What does 0 === false evaluate to?", "false", "true", "0", "It throws"],
    ["What does typeof null return?", "object", "null", "undefined", "boolean"],
    ["What does 0 || 3 return?", "3", "0", "null", "undefined"],
    ["What does 0 ?? 3 return?", "0", "3", "null", "undefined"],
    ["What does user.address?.city return when address is missing?", "undefined", "An error", "null", "An empty string"],
    ["Can a const array be changed with push()?", "Yes, its contents can change", "No, const freezes it", "Only in strict mode", "Only after reassignment"],
    ["What does '5' === 5 evaluate to?", "false", "true", "5", "It throws"],
    ["What does null ?? 'fallback' return?", "fallback", "null", "undefined", "false"],
    ["What does profile?.name return when profile is null?", "undefined", "An error", "null", "false"],
  ];

  const html = [
    ["What rendering mode does <!doctype html> request?", "Modern standards mode", "Quirks mode", "XML mode", "JavaScript strict mode"],
    ["What does a label for attribute connect to?", "An input id", "An input name", "Every input type", "A form method"],
    ["Which input attribute becomes the submitted field key?", "name", "id", "value", "type"],
    ["What is a button's default behavior inside a form?", "Submit the form", "Reset the form", "Open a link", "Do nothing"],
    ["What does alt='' communicate for a decorative image?", "Assistive technology should ignore it", "The image is hidden visually", "The image cannot load", "The image has no size"],
    ["Which rel value protects a target='_blank' link?", "noopener noreferrer", "stylesheet", "canonical", "alternate"],
    ["What does href='#practice' target?", "The element with id='practice'", "The first heading", "The document head", "The next link"],
    ["What does the main element represent?", "The page's primary content", "Site navigation", "A footer", "Only a sidebar"],
    ["Which heading order is logical?", "h1 then h2 then h3", "h3 then h1 then h2", "Only h1 tags", "Headings chosen only by size"],
    ["What does a checked radio with name='contact' value='email' submit?", "contact=email", "contact=phone", "email=contact", "Both radio values"],
    ["What does required do in a browser form?", "Blocks empty submission", "Encrypts data", "Makes a value unique", "Trims server data"],
    ["What does an option with value='' submit when selected?", "An empty value", "Its visible label", "The next option", "Nothing at all"],
    ["What does th scope='row' identify?", "A row header", "A column header", "A form field", "A page heading"],
    ["Why specify image width and height?", "To reserve layout space", "To change alt text", "To enable JavaScript", "To compress the image"],
    ["When does a defer script run?", "After HTML parsing", "Before the doctype", "Only after a click", "Before parsing begins"],
    ["What can JavaScript read from data-user-id?", "A custom data value", "A CSS color only", "A form method only", "A browser password"],
    ["Why use a button instead of a clickable div for an action?", "It has built-in keyboard semantics", "It cannot receive focus", "It removes all styling", "It always submits a form"],
    ["What do fieldset and legend communicate?", "A group of related controls", "A page footer", "A table row", "A media query"],
    ["What does a picture element help choose?", "A suitable image source", "A JavaScript module", "A CSS selector", "A form method"],
    ["What does aria-label provide?", "An accessible name", "A visible border", "A form submission key", "A new tab"],
    ["What does tabindex='-1' allow?", "Programmatic focus without tab order", "Normal tab navigation first", "No focus at all", "Automatic form submission"],
    ["What does method='post' indicate?", "Data is sent in the request body", "A link opens a new tab", "A page uses only CSS", "A form cannot submit"],
    ["What does input type='email' provide?", "Email-format validation", "Guaranteed server validation", "An encrypted value", "A required password"],
    ["What does the controls attribute add to audio?", "Built-in playback controls", "Automatic captions", "A video track", "Form validation"],
    ["What belongs inside a title element?", "The document title", "The visible page body", "A form input value", "A CSS declaration"],
  ];

  const css = [
    ["Which selector wins over p in p.notice?", ".notice", "p", "The browser default", "Both selectors equally"],
    ["Which selector has the highest specificity?", "#message", ".notice", "p", "*"],
    ["What wins when two equal-specificity rules conflict?", "The later rule", "The earlier rule", "The shorter rule", "The browser default"],
    ["With border-box, what is the rendered width of width: 200px with padding and border?", "200px", "240px", "250px", "The content width only"],
    ["With content-box, what is the total width of 200px plus 20px padding and 5px borders?", "250px", "200px", "240px", "210px"],
    ["What does .card > h2 match?", "A direct h2 child of .card", "Any h2 on the page", "Only an h2 before .card", "An element with id='card'"],
    ["When does :focus-visible apply?", "When visible focus indication is appropriate", "Only when disabled", "Only when hidden", "Only on page load"],
    ["What is Flexbox's default main axis?", "Horizontal row", "Vertical column", "Diagonal", "Grid columns"],
    ["Which property makes a Flexbox main axis vertical?", "flex-direction: column", "align-items: column", "display: grid", "gap: column"],
    ["What does gap add in Flexbox?", "Space between items", "Space outside the container only", "A border", "Font size"],
    ["What does repeat(auto-fit, minmax(16rem, 1fr)) create?", "Responsive grid columns", "Exactly sixteen columns", "A hidden grid", "A Flexbox row"],
    ["What anchors an absolute child when a card has position: relative?", "The card", "The viewport only", "The document title", "The next sibling"],
    ["What happens to an absolutely positioned element in normal flow?", "It is removed from normal flow", "It becomes a block", "It becomes hidden", "It gains margin"],
    ["What does overflow: auto do when content exceeds the box?", "Adds scrolling when needed", "Always hides content", "Always shows scrollbars", "Resizes the viewport"],
    ["What does 50vw measure?", "Half the viewport width", "Half the parent width", "Fifty pixels", "Half the font size"],
    ["What value does a child normally inherit for color?", "Its parent's color", "Its parent's width", "Its parent's margin", "Its parent's border"],
    ["Which viewport matches @media (min-width: 768px)?", "768px or wider", "767px or narrower", "Only exactly 768px", "Any height"],
    ["What must be set for a container query to work?", "A query container", "A global reset", "A JavaScript listener", "A fixed viewport"],
    ["What does transform: scale(1.1) change?", "Visual size", "Document source order", "Text content", "Form method"],
    ["What does transition: color 200ms animate?", "Color changes", "Only layout changes", "HTML parsing", "JavaScript execution"],
    ["What does prefers-reduced-motion respect?", "A user's motion preference", "A color preference only", "A font download", "A server timeout"],
    ["Which property is inherited by default?", "color", "margin", "border", "width"],
    ["What does .card .title select?", "A title descendant of .card", "Only a direct title child", "Every title on the page", "The card itself"],
    ["Why can min-width: 0 be needed on a flex child?", "To allow shrinking and prevent overflow", "To force a larger width", "To disable Flexbox", "To add a border"],
    ["What does margin-inline change?", "Logical left and right margins", "Only top margin", "Only border width", "Font weight"],
  ];

  return [
    ...javascript.map((entry) => createQuestion("JavaScript", ...entry)),
    ...html.map((entry) => createQuestion("HTML", ...entry)),
    ...css.map((entry) => createQuestion("CSS", ...entry)),
  ];
}

function validateQuestionBank(questions) {
  if (questions.length !== 60) {
    throw new Error("Question bank must contain 60 questions.");
  }

  const expectedCounts = { JavaScript: 10, HTML: 25, CSS: 25 };
  const counts = { JavaScript: 0, HTML: 0, CSS: 0 };
  const questionTexts = new Set();

  questions.forEach((question, index) => {
    if (!Object.prototype.hasOwnProperty.call(expectedCounts, question.category)) {
      throw new Error("Question " + (index + 1) + " has an invalid category.");
    }
    counts[question.category] += 1;
    if (questionTexts.has(question.question)) {
      throw new Error("Duplicate question: " + question.question);
    }
    questionTexts.add(question.question);
    if (question.options.length !== 4 || new Set(question.options).size !== 4) {
      throw new Error("Question " + (index + 1) + " must have four unique options.");
    }
  });

  Object.keys(expectedCounts).forEach((category) => {
    if (counts[category] !== expectedCounts[category]) {
      throw new Error("Incorrect " + category + " question count.");
    }
  });
}

function verifyGeneratedQuestions(form, questions, config) {
  const items = form
    .getItems(FormApp.ItemType.MULTIPLE_CHOICE)
    .map((item) => item.asMultipleChoiceItem());
  if (items.length !== questions.length + 1) {
    throw new Error("Generated an incorrect number of multiple-choice items.");
  }
  if (items[0].getPoints() !== 0) {
    throw new Error("The Bootcoding interest question must be ungraded.");
  }
  const totalPoints = items.slice(1).reduce(
    (total, item) => total + item.getPoints(),
    0,
  );
  if (totalPoints !== config.totalPoints) {
    throw new Error("The form has an incorrect total score.");
  }
}

function pointsForQuestion(index, config) {
  return index < config.onePointQuestionCount
    ? config.onePointValue
    : config.twoPointValue;
}

function calculateTotalPoints(questionCount, config) {
  const twoPointQuestionCount = questionCount - config.onePointQuestionCount;
  return (
    config.onePointQuestionCount * config.onePointValue +
    twoPointQuestionCount * config.twoPointValue
  );
}

function shuffle(values) {
  for (let index = values.length - 1; index > 0; index -= 1) {
    const randomIndex = Math.floor(Math.random() * (index + 1));
    [values[index], values[randomIndex]] = [
      values[randomIndex],
      values[index],
    ];
  }
}

