from pathlib import Path
import csv
import html

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    PageBreak,
    KeepTogether,
    Spacer,
)


BASE = Path(__file__).resolve().parent
CSV_PATH = BASE / "python_fundamentals_200_mcqs.csv"
PDF_PATH = BASE / "python_fundamentals_200_mcqs_answers.pdf"


SOLUTIONS = {
    "q1": "The / operator performs true division: 10 / 4 = 2.5.",
    "q2": "// performs floor division. 10 / 4 is 2.5, and flooring gives 2.",
    "q3": "Flooring moves toward negative infinity, so -7 / 2 = -3.5 becomes -4.",
    "q4": "% returns the remainder after division. 10 = 3 × 3 + 1.",
    "q5": "** is exponentiation, so 2 ** 3 means 2 × 2 × 2 = 8.",
    "q6": "Exponentiation binds more tightly than the unary minus: -3 ** 2 is -(3 ** 2) = -9.",
    "q7": "not performs a truth-value test and always produces a Boolean, True or False.",
    "q8": "The + operator concatenates strings, so 'Py' + 'thon' produces 'Python'.",
    "q9": "Multiplying a string repeats it: 'ha' * 3 produces 'hahaha'.",
    "q10": "Multiplication has precedence over addition, so 2 + (3 × 4) = 14.",
    "q11": "Parentheses are evaluated first: (2 + 3) × 4 = 20.",
    "q12": "Comparison expressions evaluate to Boolean values: True or False.",
    "q13": "Chained comparisons mean 18 <= 25 and 25 < 60; both are true.",
    "q14": "is tests whether two references point to the same object (identity).",
    "q15": "== compares the values of two objects for equality.",
    "q16": "and stops at the first falsy operand and returns that operand itself.",
    "q17": "An empty string is falsy, so the or expression returns its fallback operand.",
    "q18": "Membership in a dictionary tests its keys; values require an explicit values() check.",
    "q19": "The walrus operator := assigns a value while also returning that value in an expression.",
    "q20": "Bitwise AND compares bits: 5 (101) & 3 (011) = 1 (001).",
    "q21": "A def statement creates a function object and binds its name to it.",
    "q22": "def creates the function; its body runs later when the function is called.",
    "q23": "A parameter is the name in the function definition that receives an argument.",
    "q24": "return immediately ends the current function and sends a value to its caller.",
    "q25": "If execution reaches the end without return, Python returns None implicitly.",
    "q26": "Multiple comma-separated return values are packed into a tuple.",
    "q27": "Positional arguments are matched to parameters from left to right.",
    "q28": "Keyword arguments identify their target parameters by name.",
    "q29": "If the caller omits a parameter with a default, that default value is used.",
    "q30": "Required parameters must precede default parameters in a function signature.",
    "q31": "Default expressions are evaluated once, when the def statement executes.",
    "q32": "A mutable default is one object reused by later calls, so changes can accumulate.",
    "q33": "Using None as the default and creating a list inside the function gives each call a fresh list.",
    "q34": "In a signature, / marks all parameters before it as positional-only.",
    "q35": "A bare * ends positional parameters; parameters after it must be supplied by keyword.",
    "q36": "Extra positional arguments are collected into the tuple named by *args.",
    "q37": "Extra keyword arguments are collected into the dictionary named by **kwargs.",
    "q38": "A single * in a call unpacks an iterable into positional arguments.",
    "q39": "A ** in a call unpacks a mapping into keyword arguments.",
    "q40": "The parameter refers to the same mutable list, so in-place mutation is visible to the caller.",
    "q41": "Rebinding changes only the local parameter name; it does not rebind the caller's name.",
    "q42": "Python resolves names in Local, Enclosing, Global, then Built-in scopes: LEGB.",
    "q43": "global declares that assignments to count target the module-level name.",
    "q44": "nonlocal targets the nearest binding in an enclosing function, not the module scope.",
    "q45": "An assignment makes the name local throughout the function; reading it first raises UnboundLocalError.",
    "q46": "A variable name is a label or reference bound to an object, not a fixed storage box.",
    "q47": "Dynamic typing lets the same name be rebound to objects of different types at runtime.",
    "q48": "Identifiers may contain letters, digits, and underscores, subject to starting-character rules.",
    "q49": "Identifiers cannot start with a digit, so 2nd_place is invalid syntax.",
    "q50": "Reserved Python keywords have syntactic meaning and cannot be used as identifiers.",
    "q51": "Python is case-sensitive, so name and Name refer to potentially different names.",
    "q52": "PEP 8 recommends lowercase words separated by underscores for ordinary variables.",
    "q53": "Assignment copies the reference, so both names point to the same list object.",
    "q54": "Rebinding makes a name refer to a different object; it does not mutate the old object.",
    "q55": "Mutation changes the state of an existing object, such as adding an item to a list.",
    "q56": "Integers are immutable, so incrementing binds the name to a new integer object.",
    "q57": "Multiple assignment binds several names in one statement, often by unpacking values.",
    "q58": "Chained assignment binds each name to the same right-hand object reference.",
    "q59": "The starred unpacking target gathers remaining items into a new list.",
    "q60": "An annotation records an expected type for tools and readers; ordinary Python does not enforce it.",
    "q61": "Every Python object has a type and an identity; its state is represented by its value or contents.",
    "q62": "int represents whole-number values, such as 0, 7, or -12.",
    "q63": "float represents binary floating-point values, such as 3.14.",
    "q64": "Python uses j (or J) to mark the imaginary component of a complex literal.",
    "q65": "bool is implemented as a subclass of int, with True behaving numerically like 1 and False like 0.",
    "q66": "None is Python's singleton meaning absence of a value or result; it is not the same as zero.",
    "q67": "is None tests identity with the singleton None and is the recommended check.",
    "q68": "A string is an immutable Unicode sequence, so its characters cannot be changed in place.",
    "q69": "A list preserves order and supports in-place changes, making it an ordered mutable sequence.",
    "q70": "A tuple preserves order but cannot be changed after creation, so it is immutable.",
    "q71": "The comma creates the tuple; parentheses alone do not. Thus (10,) has one item.",
    "q72": "range stops before its stop argument, so range(2, 8, 2) yields 2, 4, and 6.",
    "q73": "A dictionary maps unique hashable keys to values.",
    "q74": "Modern Python dictionaries preserve insertion order when iterated.",
    "q75": "The in operator on a dictionary checks keys by default.",
    "q76": "A set stores unique hashable values and automatically removes duplicate insertions.",
    "q77": "A frozenset has set semantics but is immutable, so it can itself be hashed when its elements are hashable.",
    "q78": "bytes is immutable and represents integer byte values from 0 through 255.",
    "q79": "bytearray has the same byte-value range as bytes but supports in-place modification.",
    "q80": "Lists are designed for in-place operations such as append, item assignment, and removal.",
    "q81": "An empty list is falsy in a Boolean context; non-empty lists are truthy.",
    "q82": "Python tests if/elif conditions in order and executes only the first branch whose condition is true.",
    "q83": "A conditional expression has the form x if condition else y and selects exactly one of two values.",
    "q84": "Chained comparison is equivalent to 18 <= 25 and 25 < 60, so it is True.",
    "q85": "Boolean precedence is not first, then and, then or; parentheses can make intent explicit.",
    "q86": "and stops as soon as it finds a falsy operand, avoiding evaluation of later operands.",
    "q87": "for obtains values from an iterable, such as a list, string, range, or generator.",
    "q88": "The stop value in range is exclusive, so it is never produced.",
    "q89": "enumerate pairs each item with its index, for example (0, first_item).",
    "q90": "zip cannot produce a pair after any input ends, so it stops at the shortest iterable.",
    "q91": "A while loop repeats while its condition remains truthy; the loop must eventually make it false to finish.",
    "q92": "break exits the nearest enclosing loop, not all loops or the surrounding function.",
    "q93": "continue skips the remaining body of the current iteration and starts the next iteration.",
    "q94": "pass is a no-operation placeholder used where a statement is syntactically required.",
    "q95": "A loop's else block runs only when the loop ends normally, not when break exits it.",
    "q96": "In nested loops, break applies to the nearest loop containing that break statement.",
    "q97": "match checks cases in source order and selects the first case whose pattern and guard match.",
    "q98": "The underscore pattern _ is commonly a catch-all fallback in a match statement.",
    "q99": "any([]) is False because no element in the empty iterable is truthy.",
    "q100": "all([]) is True by vacuous truth: there is no element that violates the condition.",
    "q101": "An iterable can provide an iterator, usually through __iter__, so it can be traversed.",
    "q102": "An iterator maintains traversal state and supplies its next value when asked.",
    "q103": "iter(list) returns a list_iterator object that traverses the list.",
    "q104": "An iterator's __iter__ method normally returns itself, so iter(iterator) is iterator is True.",
    "q105": "next(iterator) requests and returns the next item in the iterator's sequence.",
    "q106": "Once no items remain, next raises StopIteration to signal normal exhaustion.",
    "q107": "Most iterators are one-pass: after exhaustion they do not restart automatically.",
    "q108": "A for loop obtains an iterator with iter() and repeatedly calls next() until StopIteration.",
    "q109": "A custom iterator implements __iter__() and __next__().",
    "q110": "For an iterator object, __iter__() should return self so it can be used by for and iter().",
    "q111": "list(iterator) repeatedly consumes next(), advancing the iterator through all remaining values.",
    "q112": "After exhaustion there are no remaining values, so a second list(iterator) is empty.",
    "q113": "Create a fresh iterator from the original reusable iterable, such as iter(numbers).",
    "q114": "The iterator stores its current position so the next call continues where the last one stopped.",
    "q115": "A generator is usually simpler when the traversal state can be expressed with local variables and yield.",
    "q116": "Calling a function containing yield creates a generator iterator; its body has not run yet.",
    "q117": "Generator execution is lazy and starts on next() or when iteration begins.",
    "q118": "yield produces a value and suspends execution while preserving locals and the execution position.",
    "q119": "Resuming with next continues until another yield, a return, or an exception.",
    "q120": "Normal completion of a generator is reported to the iterator protocol as StopIteration.",
    "q121": "A generator's return expression becomes the value attribute of the final StopIteration.",
    "q122": "yield from forwards iteration to another iterable and handles its values for the caller.",
    "q123": "A generator expression computes values lazily as iteration requests them.",
    "q124": "A list comprehension builds and stores the complete list immediately.",
    "q125": "A lazy pipeline connects stages that produce each value only when downstream code requests it.",
    "q126": "The context-manager protocol uses __enter__() on entry and __exit__() on leaving the with block.",
    "q127": "After successful entry, __exit__() runs when the with body finishes, including during cleanup.",
    "q128": "Returning False from __exit__ does not suppress an exception, so it propagates normally.",
    "q129": "Returning True from __exit__ tells the with statement that the exception was handled.",
    "q130": "contextlib.contextmanager turns a generator function with setup/yield/cleanup into a context manager.",
    "q131": "Code before yield runs on entering the context and is used for setup.",
    "q132": "A finally block runs whether the body succeeds or raises, making it suitable for deterministic cleanup.",
    "q133": "Nested context managers exit in reverse order: B is entered after A and exits first.",
    "q134": "A list or tuple retains values for reuse, unlike a one-pass iterator that may be exhausted.",
    "q135": "A context manager deterministically acquires and releases resources around a with block.",
    "q136": "A namespace maps names to the objects those names currently reference.",
    "q137": "An object is usefully described by its type, state, and identity.",
    "q138": "Separate lists may contain equal values while being different objects: == is True and is is False.",
    "q139": "id returns an identity value unique among live objects for that object's lifetime.",
    "q140": "Aliasing means multiple references point to the same object, especially important for mutable objects.",
    "q141": "Mutating through one alias changes the shared object, so other aliases observe the change.",
    "q142": "Rebinding changes one name's reference; it does not automatically alter the object previously referenced.",
    "q143": "Mutation changes contents in place, preserving the mutable object's identity.",
    "q144": "Strings are immutable, so concatenation creates a new string instead of changing the old one.",
    "q145": "An object remains reachable while at least one live reference can still reach it.",
    "q146": "Garbage collection can reclaim objects that are no longer reachable from live roots.",
    "q147": "Reference counting alone can leave a closed cycle with nonzero counts, so cyclic GC is needed.",
    "q148": "Resource lifetime should be explicit; use deterministic cleanup such as a with statement rather than GC timing.",
    "q149": "Ordinary assignment creates another reference to the same object; it does not recursively copy it.",
    "q150": "A shallow copy duplicates the outer container but retains references to its nested objects.",
    "q151": "A deep copy recursively copies nested objects, separating the copied object graph.",
    "q152": "The * 3 repeats the same inner-list reference, so changing one row can change all repeated rows.",
    "q153": "The comprehension creates a new inner list on each iteration, giving rows independent storage.",
    "q154": "Calling a function binds its local parameter to the same object reference; it does not automatically deep-copy it.",
    "q155": "Use == for normal value comparison; identity behavior of interned objects is an implementation detail.",
    "q156": "A simplified CPython path is source → tokens/AST → code object/bytecode → execution frame.",
    "q157": "exec compiles and executes supplied code in the namespace(s) given to it.",
    "q158": "Untrusted text passed to exec can execute arbitrary Python code, so it is unsafe without strong isolation.",
    "q159": "At module level, Python executes statements sequentially from top to bottom.",
    "q160": "A def statement creates the function; its body runs only when the function is called.",
    "q161": "Each active function call has an execution frame containing its locals and execution state.",
    "q162": "Nested lookup follows LEGB: Local, Enclosing, Global, then Built-in.",
    "q163": "Any assignment marks the name local throughout that function, so an earlier read raises UnboundLocalError.",
    "q164": "Python evaluates the callable and argument expressions before entering the function body.",
    "q165": "Arguments are matched and parameters are bound before the first body statement executes.",
    "q166": "A finally clause runs during unwinding, even after a return value has been prepared.",
    "q167": "An unhandled exception unwinds call frames until a matching exception handler is found or the program terminates.",
    "q168": "with invokes __enter__ before the body and __exit__ afterward, including during exception handling.",
    "q169": "for repeatedly calls next on an iterator and stops when StopIteration is raised.",
    "q170": "A suspended generator keeps its frame, instruction position, and local variables.",
    "q171": "Decorator expressions and application normally occur when the decorated definition executes.",
    "q172": "The class body executes immediately in a temporary namespace while the class statement runs.",
    "q173": "sys.modules caches imported module objects so normal repeated imports can reuse them.",
    "q174": "The main-module guard tests whether __name__ == '__main__'.",
    "q175": "Separate processes normally have separate address spaces; threads within a process share its memory.",
    "q176": "Python has no enforced const keyword; UPPER_SNAKE_CASE communicates a constant-by-convention name.",
    "q177": "Final is primarily for static type checkers; it does not make a value immutable at runtime.",
    "q178": "type(value) returns the value's exact runtime class.",
    "q179": "isinstance accepts instances of the requested type and its subclasses.",
    "q180": "bool is a subclass of int, and True is an instance of int, so the result is True.",
    "q181": "The decimal text '25' is parsed as an integer, producing 25.",
    "q182": "'2.5' is valid float text but not valid integer text, so int raises ValueError.",
    "q183": "With base 2, 1010 represents 1×8 + 0×4 + 1×2 + 0×1 = 10.",
    "q184": "With base 16, ff is 15×16 + 15 = 255.",
    "q185": "int converts a float by truncating toward zero; int(3.9) is 3.",
    "q186": "float converts the integer 7 to the floating-point value 7.0.",
    "q187": "str(100) creates the text '100', not another numeric object.",
    "q188": "Zero is a falsy numeric value, so bool(0) is False.",
    "q189": "A non-empty string is truthy regardless of its characters; bool('False') is True.",
    "q190": "list(string) iterates over characters, producing ['a', 'b', 'a'].",
    "q191": "tuple(string) iterates over characters and packs them into ('a', 'b', 'a').",
    "q192": "Set construction keeps only unique values, so duplicate elements are removed.",
    "q193": "dict accepts an iterable of pairs, using each pair's first item as a key and second as its value.",
    "q194": "Encoding translates text characters into a bytes representation using a character encoding.",
    "q195": "Decoding interprets bytes with an encoding and produces text (a str).",
    "q196": "Mixed numeric addition promotes the integer to floating point, so 2 + 3.5 is a float.",
    "q197": "The Unicode code point for uppercase A is 65, so ord('A') returns 65.",
    "q198": "chr maps code point 65 back to its character, uppercase A.",
    "q199": "Converting 3.75 to int removes the fractional part, producing 3.",
    "q200": "Validation inspects whether data meets requirements; conversion transforms it into another representation or type.",
}


def esc(value: str) -> str:
    return html.escape(str(value), quote=False)


class NumberedDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="normal",
        )
        self.addPageTemplates([PageTemplate(id="main", frames=frame, onPage=self._header_footer)])

    def _header_footer(self, canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#D7DEE8"))
        canvas.line(doc.leftMargin, A4[1] - 17 * mm, A4[0] - doc.rightMargin, A4[1] - 17 * mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#667085"))
        canvas.drawString(doc.leftMargin, A4[1] - 13 * mm, "Python Fundamentals — Answered MCQs")
        canvas.drawRightString(A4[0] - doc.rightMargin, 10 * mm, f"Page {doc.page}")
        canvas.restoreState()


def build_pdf():
    with CSV_PATH.open(newline="", encoding="utf-8-sig") as source:
        rows = list(csv.DictReader(source))

    if len(rows) != 200:
        raise ValueError(f"Expected 200 rows, found {len(rows)}")

    expected_ids = {f"q{i}" for i in range(1, 201)}
    actual_ids = {row["Question ID"] for row in rows}
    if actual_ids != expected_ids or set(SOLUTIONS) != expected_ids:
        raise ValueError("Question IDs or solution coverage is incomplete")

    for row in rows:
        options = [row[f"Option {letter}"] for letter in "ABCD"]
        if row["Correct Answer"] not in options:
            raise ValueError(f"Answer is not one of the choices for {row['Question ID']}")

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "TitleCustom", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=23, leading=29, alignment=TA_CENTER, textColor=colors.HexColor("#17324D"),
        spaceAfter=8 * mm,
    )
    subtitle = ParagraphStyle(
        "Subtitle", parent=styles["Normal"], fontSize=11, leading=16,
        alignment=TA_CENTER, textColor=colors.HexColor("#475467"), spaceAfter=4 * mm,
    )
    section = ParagraphStyle(
        "Section", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=9, leading=12, textColor=colors.HexColor("#16715A"),
        spaceBefore=3 * mm, spaceAfter=1.5 * mm,
    )
    question = ParagraphStyle(
        "Question", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=10.5, leading=14, textColor=colors.HexColor("#172B4D"), spaceAfter=1.5 * mm,
    )
    options = ParagraphStyle(
        "Options", parent=styles["Normal"], fontSize=8.7, leading=11.5,
        leftIndent=4 * mm, textColor=colors.HexColor("#475467"), spaceAfter=1.5 * mm,
    )
    answer = ParagraphStyle(
        "Answer", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=9.5, leading=13, textColor=colors.HexColor("#0B6E4F"), spaceAfter=1 * mm,
    )
    solution = ParagraphStyle(
        "Solution", parent=styles["Normal"], fontSize=9.2, leading=13,
        textColor=colors.HexColor("#344054"), spaceAfter=3 * mm,
    )
    note = ParagraphStyle(
        "Note", parent=styles["Normal"], fontSize=9.5, leading=14,
        alignment=TA_CENTER, textColor=colors.HexColor("#475467"),
    )

    doc = NumberedDocTemplate(
        str(PDF_PATH), pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=24 * mm, bottomMargin=16 * mm,
        title="Python Fundamentals 200 MCQs — Answers and Solutions",
        author="OpenAI",
    )
    story = [
        Spacer(1, 28 * mm),
        Paragraph("Python Fundamentals", title),
        Paragraph("200 Multiple-Choice Questions — Answers and Solutions", subtitle),
        Spacer(1, 8 * mm),
        Paragraph(
            "This answer guide follows the order and answer choices in the supplied CSV. "
            "Each item includes the question, all choices for reference, the correct answer, and a concise explanation.",
            note,
        ),
        Spacer(1, 8 * mm),
        Paragraph("Source: python_fundamentals_200_mcqs.csv", note),
        PageBreak(),
    ]

    current_section = None
    for row in rows:
        qid = row["Question ID"]
        if row["Section"] != current_section:
            current_section = row["Section"]
            story.append(Paragraph(esc(current_section), section))

        choice_text = "<br/>".join(
            f"{letter}. {esc(row[f'Option {letter}'])}" for letter in "ABCD"
        )
        block = [
            Paragraph(f"{esc(qid.upper())}. {esc(row['Question Text'])}", question),
            Paragraph(choice_text, options),
            Paragraph(f"Answer: {esc(row['Correct Answer'])}", answer),
            Paragraph(f"Solution: {esc(SOLUTIONS[qid])}", solution),
        ]
        story.append(KeepTogether(block))

    doc.build(story)
    print(f"Created {PDF_PATH}")


if __name__ == "__main__":
    build_pdf()
