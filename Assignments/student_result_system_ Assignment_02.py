"""
Student Performance and Result Management System
Author : Muhammad Moneem

This program collects a student's name and marks, processes the marks,
stores the records in Python data structures and prints a performance report.

How to run
    python student_result_system.py          -> interactive run (sections a-g), then the test cases
    python student_result_system.py --test   -> only the built-in test cases (no typing needed)

Written explanations are placed in the "EXPLANATION" comment blocks of each section.
"""

import keyword
import math
import sys


# Constants used by the whole program

SUBJECTS = ["Mathematics", "Physics", "Chemistry", "English", "Computer Science"]
MAX_MARKS = 100              # maximum marks in one subject
PASS_PERCENTAGE = 50         # below this percentage the student fails
DISTINCTION_PERCENTAGE = 75  # distinction rule chosen for this program (75% or more)


def section(title):
    """Print a clear heading for each part of the program."""
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


# Input and validation helpers (used by the whole program)
def parse_mark(text):
    """Convert the text typed by the user into a valid mark (float).

    Raises ValueError with a clear message if the text is not a valid mark.
    """
    text = text.strip()                     # remove spaces around the input
    if text == "":
        raise ValueError("The marks cannot be empty.")
    mark = float(text)                      # type casting: str -> float (ValueError if not a number)
    if not math.isfinite(mark):             # rejects 'nan' and 'inf', which float() accepts
        raise ValueError("The marks must be a real number.")
    if mark < 0 or mark > MAX_MARKS:
        raise ValueError(f"The marks must be between 0 and {MAX_MARKS}.")
    return mark


def read_mark(subject, source=input):
    """Keep asking for the marks of one subject until the user enters a valid value
    or chooses to stop by typing 'q'.

    Returns a tuple (raw_text, mark), or None if the user stopped.
    `source` is the function used to read the text (input by default). It is a
    parameter so the same loop can be tested without typing.
    """
    while True:                                              # while loop: repeat until valid or quit
        raw = source(f"Enter marks for {subject} (0-{MAX_MARKS}, or 'q' to stop): ")
        if raw.strip().lower() == "q":
            return None                                      # user chose to stop
        try:
            return raw.strip(), parse_mark(raw)              # valid value: leave the loop
        except ValueError as error:
            print(f"  Invalid input ({error}) Please try again.")


def get_student_name(source=input):
    """Ask for the student's name until a sensible name is entered."""
    while True:
        raw = source("Enter the student's name: ")
        name = raw.strip()
        if name == "":
            print("  Invalid input (the name cannot be empty). Please try again.")
        elif any(character.isdigit() for character in name):
            print("  Invalid input (the name cannot contain digits). Please try again.")
        else:
            return raw                                       # return it exactly as typed


def collect_marks(subjects, source=input):
    """Collect one valid mark for every subject. Returns (raw_texts, marks) or None."""
    raw_texts, marks = [], []
    for subject in subjects:
        result = read_mark(subject, source)
        if result is None:
            return None                                      # the user chose to stop
        raw_texts.append(result[0])
        marks.append(result[1])
    return raw_texts, marks


def make_fake_input(values):
    """Return a function that behaves like input() but reads from a list.
    Used to test the invalid-input handling without typing anything."""
    iterator = iter(values)

    def fake_input(prompt=""):
        value = next(iterator)
        print(f"{prompt}{value}")
        return value

    return fake_input


# Calculation helpers
def calculate_results(marks):
    """Return (total, average, percentage) for a list of marks."""
    total = sum(marks)                                       # addition
    average = total / len(marks)                             # division
    percentage = total / (len(marks) * MAX_MARKS) * 100      # division and multiplication
    return total, average, percentage


def get_grade(percentage):
    """Grade rules from the question (see section d)."""
    if percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "Fail"


# a. VALUES, EXPRESSIONS, VARIABLES AND OPERATORS
def section_a(name, marks, subjects):
    section("a. Values, Expressions, Variables and Operators")

    # Variables that store the student's information (each one has a different data type)
    student_name = name.strip()
    age = 20
    total_marks, average_marks, percentage = calculate_results(marks)   # float, float, float
    is_enrolled = True
    # `subjects` (a list of str) is passed in and stores the subject names

    print("Variable        Type   Value")
    for label, value in [("student_name", student_name), ("age", age),
                         ("total_marks", total_marks), ("average_marks", average_marks),
                         ("percentage", percentage), ("is_enrolled", is_enrolled),
                         ("subjects", subjects)]:
        print(f"{label:<15} {type(value).__name__:<6} {value}")

    # Arithmetic operators
    print("\nArithmetic operators")
    print(f"Total marks   = sum of all marks             = {total_marks}")
    print(f"Average marks = total / number of subjects   = {total_marks} / {len(marks)} = {average_marks:.2f}")
    print(f"Percentage    = total / (subjects * 100) * 100 = {percentage:.2f}%")
    print(f"Extra examples: 17 // 5 = {17 // 5}, 17 % 5 = {17 % 5}, 2 ** 3 = {2 ** 3}")

    # Comparison and logical operators decide whether the student has passed
    passed = percentage >= PASS_PERCENTAGE and is_enrolled
    print("\nComparison and logical operators")
    print(f"percentage >= {PASS_PERCENTAGE}                 -> {percentage >= PASS_PERCENTAGE}   (comparison)")
    print(f"percentage >= {PASS_PERCENTAGE} and is_enrolled -> {passed}   (logical and)")
    print(f"not passed                      -> {not passed}   (logical not)")
    print(f"Result: {'PASSED' if passed else 'FAILED'}")

    # Keywords are reserved words; `keyword.iskeyword` checks a word
    print(f"\nkeyword.iskeyword('if') = {keyword.iskeyword('if')}, "
          f"keyword.iskeyword('total_marks') = {keyword.iskeyword('total_marks')}")
    print(f"Python has {len(keyword.kwlist)} keywords, for example: {keyword.kwlist[:8]}")

    # EXPLANATION - value, expression, statement, variable and keyword
    #   value      : a single piece of data, e.g. 85, 'Ali', True, 3.5.
    #   variable   : a name that refers to a value stored in memory, e.g. in
    #                `marks_obtained = 85` the name marks_obtained refers to the value 85.
    #   expression : a combination of values, variables and operators that Python
    #                evaluates to produce a value, e.g. `85 + 10` gives 95 and
    #                `percentage >= 50` gives True or False.
    #   statement  : a complete instruction that Python executes, e.g. the assignment
    #                `total = 85 + 90`, `print(total)`, an `if` block or a `for` loop.
    #                A statement can contain expressions, but an expression alone is not
    #                always a statement.
    #   keyword    : a reserved word with a fixed meaning in the language, such as
    #                if, else, for, while, def, True, None, and, or, not. Keywords cannot
    #                be used as variable names (for = 5 is a SyntaxError).
    #   Example putting them together:   passed = marks >= 50
    #       `passed`     is a variable,  `50` is a value,  `marks >= 50` is an expression,
    #       the whole line is an assignment statement,  and `>=` is an operator.
    return percentage


# b. STRINGS, INPUT, TYPE CASTING AND COMMENTS
def section_b(raw_name, raw_marks, marks, percentage, grade):
    section("b. Strings, Input, Type Casting and Comments")

    name = raw_name.strip()                                  # strip() removes extra spaces at both ends
    print(f"Name as typed       : {raw_name!r}")
    print(f"After strip()       : {name!r}")
    print(f"Uppercase           : {name.upper()}")
    print(f"Lowercase           : {name.lower()}")
    print(f"Title case          : {name.title()}")
    print(f"Spaces inside name  : {' '.join(name.split())!r}  (split/join also removes repeated inner spaces)")

    # Type casting: input() always gives a string, so it was converted with float()
    print("\nType casting of the marks entered by the user")
    for text, number in zip(raw_marks, marks):
        print(f"  input text {text!r:<8} ({type(text).__name__}) -> float {number} ({type(number).__name__})")
    print(f"  Without casting: '85' + '90' = {'85' + '90'!r}   With casting: 85 + 90 = {float('85') + float('90')}")

    # Formatted result using an f-string
    clean_name = ' '.join(name.split()).title()
    print("\nFormatted result (f-string)")
    print(f"Student : {clean_name}")
    print(f"Marks   : {marks}")
    print(f"Result  : {percentage:.2f}%  |  Grade {grade}" if grade != "Fail"
          else f"Result  : {percentage:.2f}%  |  Fail")

    # EXPLANATION - why type casting is necessary when using input()
    #   input() always returns a str, even when the user types digits. A string such as
    #   '85' cannot be used for arithmetic: '85' + '90' joins the text into '8590',
    #   '85' + 5 raises TypeError, and '85' > 50 raises TypeError. Converting the text
    #   with int() or float() creates a real number, so total, average, percentage and
    #   comparisons are calculated correctly. If the text is not a number, the cast
    #   raises ValueError, which the program catches to ask for the value again.


# c. PYTHON DATA STRUCTURES
def section_c(name, marks, subjects):
    section("c. Python Data Structures")

    # The five data structures asked for
    subject_list = subjects.copy()                           # list of five subject names (a copy is edited below)
    roll_info = (101, 2024)                                  # tuple: (roll number, admission year)
    student = {"name": name.strip(), "age": 20, "marks": marks}   # dictionary
    selected = ["Mathematics", "Physics", "Mathematics", "Chemistry",
                "Physics", "English", "Chemistry"]           # subjects chosen by students (has repeats)
    unique_subjects = set(selected)                          # set: duplicates are removed

    print(f"List       : {subject_list}")
    print(f"Tuple      : {roll_info}  -> roll number {roll_info[0]}, admission year {roll_info[1]}")
    print(f"Dictionary : {student}")
    print(f"Set        : {sorted(unique_subjects)}")

    # List operations: add, update and remove
    print("\nList operations")
    subject_list.append("Statistics")                        # add a new subject
    print(f"After add    (append 'Statistics')            : {subject_list}")
    subject_list[1] = "Applied Physics"                      # update an existing subject
    print(f"After update (index 1 -> 'Applied Physics')   : {subject_list}")
    subject_list.remove("Chemistry")                         # remove one subject
    print(f"After remove ('Chemistry')                    : {subject_list}")

    # Tuple cannot be changed
    print("\nTuple is immutable")
    try:
        roll_info[0] = 202                                   # not allowed
    except TypeError as error:
        print(f"Trying roll_info[0] = 202 -> TypeError: {error}")

    # Dictionary operations
    print("\nDictionary operations")
    student["section"] = "A"                                 # add a new key-value pair
    print(f"After adding 'section': {student}")
    print(f"Marks retrieved with student['marks']      : {student['marks']}")
    print(f"Marks retrieved with student.get('marks')  : {student.get('marks')}")

    # Set removes duplicates
    print("\nSet removes duplicate values")
    print(f"Original list ({len(selected)} items)   : {selected}")
    print(f"As a set ({len(unique_subjects)} unique items) : {sorted(unique_subjects)}")

    # Comparison table of the four structures
    print("\nList vs Tuple vs Dictionary vs Set")
    rows = [("Structure", "Ordered", "Mutable", "Duplicates", "Example"),
            ("list", "Yes", "Yes", "Allowed", "[1, 2, 2]"),
            ("tuple", "Yes", "No", "Allowed", "(1, 2, 2)"),
            ("dict", "Yes (3.7+)", "Yes", "Keys unique", "{'a': 1}"),
            ("set", "No", "Yes", "Not allowed", "{1, 2}")]
    for row in rows:
        print(f"{row[0]:<10}{row[1]:<13}{row[2]:<9}{row[3]:<13}{row[4]}")

    # EXPLANATION - why a tuple is suitable for data that must not change
    #   A tuple is immutable: after it is created its items cannot be added, changed or
    #   removed. A roll number and an admission year should never be changed by accident,
    #   so storing them in a tuple protects them (Python raises TypeError on any change),
    #   makes the intent clear to other programmers, and tuples are slightly faster and
    #   can be used as dictionary keys.
    #
    # EXPLANATION - differences between list, tuple, dictionary and set
    #   list       : ordered, mutable, allows duplicates, items accessed by index.
    #   tuple      : ordered, immutable, allows duplicates, items accessed by index.
    #   dictionary : stores key-value pairs. Keys must be unique (a repeated key replaces
    #                the old value), values may repeat. It keeps insertion order (Python 3.7+)
    #                and is mutable. Items are accessed by key.
    #   set        : unordered (no index), mutable (items can be added or removed), and
    #                does not allow duplicates, so it is ideal for unique values.


# d. CONDITIONAL EXECUTION
def section_d(percentage):
    section("d. Conditional Execution")

    # if / elif / else to assign the grade
    grade = get_grade(percentage)
    print(f"Percentage {percentage:.2f}% -> {'Grade ' + grade if grade != 'Fail' else 'Fail'}")

    print("\nGrade boundaries")
    for value in [95, 80, 79.9, 70, 69.9, 60, 59.9, 50, 49.9]:
        label = get_grade(value)
        print(f"  {value:>5}%  ->  {'Grade ' + label if label != 'Fail' else 'Fail'}")

    # Nested conditional: passed? and then distinction?
    print("\nNested conditional")
    if percentage >= PASS_PERCENTAGE:                        # outer check: has the student passed?
        if percentage >= DISTINCTION_PERCENTAGE:             # inner check: distinction?
            result = "Passed with Distinction"
        else:
            result = "Passed (no distinction)"
    else:
        result = "Failed"
    print(f"Result: {result}")

    # Ternary (conditional) expression
    eligibility = "Eligible to pass" if percentage >= PASS_PERCENTAGE else "Not eligible to pass"
    print(f"\nTernary expression: {eligibility}")

    # Why the order of the conditions matters
    def grade_wrong_order(value):
        if value >= 50:                                      # this catches everything from 50 upward
            return "D"
        elif value >= 60:                                    # never reached for 60 or more
            return "C"
        elif value >= 70:
            return "B"
        elif value >= 80:
            return "A"
        else:
            return "Fail"

    print("\nWhy the order matters")
    print(f"  85% with the correct order     -> Grade {get_grade(85)}")
    print(f"  85% with the conditions reversed -> Grade {grade_wrong_order(85)}  (wrong!)")

    # EXPLANATION - if, elif and else
    #   if   : starts the decision and runs its block when its condition is True.
    #   elif : "else if" - checked only when all earlier conditions were False. You can
    #          use many elif blocks to test further conditions one after another.
    #   else : the final block that runs when none of the conditions above was True. It has
    #          no condition of its own and is optional.
    #   Only the first block whose condition is True runs; the rest are skipped.
    #
    # EXPLANATION - why the order of conditions matters in a grading system
    #   Python checks the conditions from top to bottom and stops at the first True one.
    #   Because a mark of 85 is also >= 70, >= 60 and >= 50, the highest grade must be tested
    #   first (>= 80, then >= 70, ...). If `>= 50` were tested first, every passing student
    #   would get Grade D, as the demonstration above shows.
    return grade, result


# e. LOOPS AND CONTROL STATEMENTS
def send_result_sms(student_name):
    """Placeholder function: the SMS feature will be written later."""
    pass                                                     # pass does nothing; it keeps the function valid


def section_e(name, subjects, marks):
    section("e. Loops and Control Statements")

    # for loop over the subject list
    print("for loop - each subject")
    for subject in subjects:
        print(f"  {subject}")

    # enumerate() with serial numbers starting from 1
    print("\nenumerate() - serial number starting from 1")
    for number, (subject, mark) in enumerate(zip(subjects, marks), start=1):
        print(f"  {number}. {subject:<18} {mark}")

    # while loop: repeat until a valid value is entered or the user stops.
    # (The same loop collected the real marks at the start of the program. Here it is shown
    #  again with simulated typing so the behaviour is visible.)
    print("\nwhile loop - repeat until valid input, or the user chooses to stop")
    fake = make_fake_input(["abc", "105", "", "72.5"])
    result = read_mark("Demo subject", source=fake)
    print(f"  Accepted value: {result[1]}")
    fake = make_fake_input(["x", "q"])
    result = read_mark("Demo subject", source=fake)
    print(f"  User typed 'q' -> returned {result} (stopped)")

    # Nested loops: table of students and their subjects
    print("\nNested loops - students and their subjects")
    students = {"Ali": ["Mathematics", "Physics"],
                "Sara": ["Chemistry", "English", "Computer Science"],
                name.strip().title(): subjects}
    print(f"  {'Student':<18}| Subject")
    print("  " + "-" * 40)
    for student_name, student_subjects in students.items():  # outer loop: students
        for subject in student_subjects:                     # inner loop: that student's subjects
            print(f"  {student_name:<18}| {subject}")

    print("\nNested loops - 5 x 5 multiplication table")
    for row in range(1, 6):
        print("  " + "".join(f"{row * column:>4}" for column in range(1, 6)))

    # break: stop the loop as soon as a subject mark is below 33 (a failing subject)
    print("\nbreak - stop when a subject below 33 is found")
    for subject, mark in zip(subjects, marks):
        if mark < 33:
            print(f"  Failing subject found: {subject} ({mark}). Loop stopped with break.")
            break
        print(f"  Checked {subject}: {mark} is fine")
    else:                                                    # runs only if the loop was not stopped by break
        print("  No subject below 33 was found.")

    # continue: skip invalid marks and keep the valid ones
    print("\ncontinue - skip invalid marks")
    raw_entries = ["78", "abc", "105", "64", "-5", "90"]
    valid_marks = []
    for entry in raw_entries:
        try:
            mark = parse_mark(entry)
        except ValueError:
            print(f"  Skipping invalid mark {entry!r}")
            continue                                         # jump to the next entry
        valid_marks.append(mark)
    print(f"  Valid marks kept: {valid_marks}")

    # pass: placeholder
    print("\npass - placeholder")
    send_result_sms(name)                                    # runs without doing anything yet
    print("  send_result_sms() was called; its body is only `pass`, so nothing happens yet.")

    # EXPLANATION - purpose of pass
    #   pass is a statement that does nothing. Python needs at least one statement inside a
    #   function, class, loop or if block, so pass is used as a placeholder for code that
    #   will be written later, e.g.
    #       def send_result_sms(student_name):
    #           pass            # TODO: write the SMS code later
    #   Without it, an empty block would cause an IndentationError.
    #
    # EXPLANATION - break and continue
    #   break    : ends the loop completely and continues with the code after the loop.
    #   continue : skips the rest of the current round and goes to the next round of the loop.


# f. LIST COMPREHENSION, ITERABLES AND ITERATORS
def section_f(subjects):
    section("f. List Comprehension, Iterables and Iterators")

    marks = [35, 78, 45, 90, 62, 28, 85]
    passing = [mark for mark in marks if mark >= 50]
    print(f"marks                       = {marks}")
    print(f"Marks >= 50                 = {passing}")

    even_squares = [number ** 2 for number in range(1, 21) if number % 2 == 0]
    print(f"Squares of even numbers 1-20 = {even_squares}")

    # iter() and next()
    print("\niter() and next()")
    iterator = iter(subjects)
    print(f"type(subjects) = {type(subjects).__name__}, type(iterator) = {type(iterator).__name__}")
    for _ in range(len(subjects)):
        print(f"  next(iterator) -> {next(iterator)}")

    # What happens when no items are left
    print("\nCalling next() after the iterator is exhausted")
    try:
        next(iterator)
    except StopIteration:
        print("  StopIteration was raised because there are no elements left.")
    print(f"  next(iterator, 'no more items') -> {next(iterator, 'no more items')}  (default value avoids the error)")

    # EXPLANATION - iterable vs iterator
    #   iterable : any object that can give its items one at a time, i.e. it can be used in a
    #              for loop: list, tuple, str, dict, set, range. It has an __iter__() method.
    #              An iterable can be looped over many times.
    #   iterator : an object that produces the items one by one and remembers its position.
    #              It has __next__() (and __iter__()). It is created from an iterable with
    #              iter(), and next() returns the next item. An iterator can be used only once;
    #              when it is finished it stays finished.
    #   Every iterator is an iterable, but a list is an iterable that is not an iterator.
    #
    # EXPLANATION - next() on an exhausted iterator
    #   When no elements remain, next() raises the StopIteration exception. A for loop catches
    #   this automatically to end the loop. With a manual next() call, catch StopIteration
    #   with try/except or give next() a default value: next(iterator, default).


# g. CODE ANALYSIS AND DEBUGGING
def section_g():
    section("g. Code Analysis and Debugging")

    # The code given in the question, run exactly as written
    print("Given code output:")
    marks = [45, 80, 32, 90, 65]

    passed = []

    for mark in marks:
        if mark < 50:
            continue
        passed.append(mark)

    print(passed)
    print(len(passed))
    print(sum(passed) / len(passed))

    # What happens if continue is replaced with break
    print("\nWith break instead of continue:")
    passed_break = []
    for mark in marks:
        if mark < 50:
            break                                            # stops at the first mark below 50 (45)
        passed_break.append(mark)
    print(passed_break)
    print(len(passed_break))
    try:
        print(sum(passed_break) / len(passed_break))
    except ZeroDivisionError as error:
        print(f"ZeroDivisionError: {error}")

    # What happens if all marks are below 50, and the fix
    print("\nIf all marks are below 50:")
    low_marks = [45, 32, 40]
    passed_low = []
    for mark in low_marks:
        if mark < 50:
            continue
        passed_low.append(mark)
    print(f"passed = {passed_low}, len(passed) = {len(passed_low)}")
    try:
        print(sum(passed_low) / len(passed_low))             # this is the buggy line
    except ZeroDivisionError as error:
        print(f"ZeroDivisionError: {error}   <- the problem")
    if passed_low:                                           # the solution: check before dividing
        print(sum(passed_low) / len(passed_low))
    else:
        print("Fixed: no marks of 50 or above, so the average is not calculated.")

    # Rewrite with list comprehension
    print("\nRewritten with list comprehension:")
    passed_lc = [mark for mark in marks if mark >= 50]
    print(passed_lc)
    print(len(passed_lc))
    print(sum(passed_lc) / len(passed_lc) if passed_lc else "No passing marks")
    print(f"Same result as the loop version: {passed_lc == passed}")

    # ANSWERS
    # 1. Output of the program:
    #        [80, 90, 65]
    #        3
    #        78.33333333333333        (80 + 90 + 65 = 235, and 235 / 3)
    # 2. Why continue is used: when a mark is below 50 (45 and 32), continue skips the rest of
    #    that round, so append() is not executed and the failing mark is not added to the list.
    #    The loop then carries on with the next mark.
    # 3. If continue were replaced with break: the loop would end completely at the first mark
    #    below 50. The first mark is 45, so the loop stops immediately and passed stays empty.
    #    The program prints [] and 0, and then crashes with ZeroDivisionError at
    #    sum(passed) / len(passed) because len(passed) is 0. Marks 80, 90 and 65 would never be checked.
    # 4. If all marks were below 50: passed stays empty, len(passed) is 0 and the last line raises
    #    ZeroDivisionError (division by zero). Solution: check the list before dividing, e.g.
    #        if passed:
    #            print(sum(passed) / len(passed))
    #        else:
    #            print("No passing marks")
    # 5. List comprehension version:
    #        passed = [mark for mark in marks if mark >= 50]


# TESTING: at least three different sets of marks, and invalid input
def generate_report(name, marks):
    """Print a short result report for one student and return the key results."""
    total, average, percentage = calculate_results(marks)
    grade = get_grade(percentage)
    if percentage >= PASS_PERCENTAGE:
        status = "Passed with Distinction" if percentage >= DISTINCTION_PERCENTAGE else "Passed"
    else:
        status = "Failed"
    best_index = marks.index(max(marks))
    record = {"name": name, "marks": marks, "total": total, "average": average,
              "percentage": percentage, "grade": grade, "status": status}
    print(f"  Student     : {name}")
    for number, (subject, mark) in enumerate(zip(SUBJECTS, marks), start=1):
        print(f"    {number}. {subject:<18}{mark:>6.1f}")
    print(f"  Total       : {total:.1f} / {len(marks) * MAX_MARKS}")
    print(f"  Average     : {average:.2f}")
    print(f"  Percentage  : {percentage:.2f}%")
    print(f"  Grade       : {'Grade ' + grade if grade != 'Fail' else 'Fail'}")
    print(f"  Status      : {status}")
    print(f"  Best subject: {SUBJECTS[best_index]} ({marks[best_index]})")
    return record


def run_test_cases():
    section("TESTS: four different sets of marks")
    test_cases = [
        ("Test 1 - high scorer", "Ayesha Khan", [92, 88, 79, 85, 90], "A"),
        ("Test 2 - average student", "Bilal Ahmed", [65, 58, 72, 61, 55], "C"),
        ("Test 3 - failing student", "Usman Ali", [35, 42, 28, 45, 39], "Fail"),
        ("Test 4 - boundary case (exactly 50%)", "Hina Raza", [50, 50, 50, 50, 50], "D"),
    ]
    records = []                                             # all test records stored in a list of dictionaries
    all_ok = True
    for title, student_name, marks, expected_grade in test_cases:
        print(f"\n{title}")
        record = generate_report(student_name, marks)
        records.append(record)
        ok = record["grade"] == expected_grade
        all_ok = all_ok and ok
        print(f"  Expected grade: {expected_grade} | Actual grade: {record['grade']} | {'OK' if ok else 'MISMATCH'}")

    print("\nSummary of all test records")
    print(f"  {'Name':<14}{'Percentage':>11}{'Grade':>7}  Status")
    for record in records:
        print(f"  {record['name']:<14}{record['percentage']:>10.2f}%{record['grade']:>7}  {record['status']}")
    print(f"\nAll grade checks passed: {all_ok}")

    # Invalid input handling
    print("\nInvalid input test: the program keeps asking until a valid mark is entered")
    fake = make_fake_input(["abc", "-5", "101", "", "nan", "75"])
    result = read_mark("Mathematics", source=fake)
    print(f"  Final accepted mark: {result[1]}")
    print("\nInvalid name test")
    fake = make_fake_input(["", "   ", "Ali123", "  Zain Malik  "])
    print(f"  Final accepted name: {get_student_name(fake).strip()!r}")


# Main program
def main():
    if "--test" in sys.argv:                                 # only run the tests
        run_test_cases()
        return

    print("STUDENT PERFORMANCE AND RESULT MANAGEMENT SYSTEM")
    print("Enter the student's details. Type 'q' instead of marks to stop.\n")

    raw_name = get_student_name()
    collected = collect_marks(SUBJECTS)
    if collected is None:
        print("\nEntry stopped by the user. No report was generated.")
        return
    raw_marks, marks = collected

    percentage = section_a(raw_name, marks, SUBJECTS)
    grade = get_grade(percentage)
    section_b(raw_name, raw_marks, marks, percentage, grade)
    section_c(raw_name, marks, SUBJECTS)
    section_d(percentage)
    section_e(raw_name, SUBJECTS, marks)
    section_f(SUBJECTS)
    section_g()

    section("FINAL REPORT")
    generate_report(raw_name.strip().title(), marks)
    run_test_cases()


if __name__ == "__main__":
    main()
