#!/usr/bin/env python
# coding: utf-8

# # Student Management System in Python
# **Functions, File Handling and Object-Oriented Programming (50 Marks)**
# Name: Muhammad Moneem
# 
# In this notebook I build a small Student Management System step by step. Each part (A to H) of the question has its own section with the code, the output and a short explanation of what I did and why.
# 
# How the parts connect:
# * **A and B** use plain functions, lists and dictionaries, and save the data to a text file.
# * **C to G** move the same idea into classes (`Student`, `Person`, `Teacher`, and so on).
# * **H** puts everything together in one small application.
# 
# Please run the cells from top to bottom, because later cells use the classes and functions from the earlier ones. The notebook creates a few small text files (like `students.txt`) in the same folder, which is the "supporting file" for the file handling part.
# 
# **A few design decisions I made**
# * Marks are out of 100, and a student passes with an average of 50 or more.
# * In part A students are simple dictionaries, because I wanted to show functions on their own before introducing classes.
# * A class is rebuilt when a new idea needs it (for example `Student` is rebuilt to inherit from `Person` in part D). I say so each time it happens.
# * All the contact details used in the examples are made-up values.

# ---
# # A. Functions, Scope and Functional Programming (8 Marks)
# 
# ## A.1 and A.2 Functions, and the three kinds of arguments
# I wrote four functions: `add_student`, `calculate_average`, `get_grade` and `display_student`. A student is stored as a dictionary, and all the students are kept in a list.
# 
# `add_student` has a default parameter (`department="General"`), so the same function can be called in three ways:
# * **positional arguments** - the values go in the order the function expects;
# * **keyword arguments** - I write the parameter names, so the order doesn't matter;
# * **default values** - if I leave the argument out, Python uses the default.

# In[1]:


# ---------- global variables (used again in A.3) ----------
school_name = "Green Valley School"
passing_marks = 50
student_count = 0


def add_student(student_list, name, roll_no, marks, department="General"):
    """Add one student (as a dictionary) to the list and return it."""
    global student_count                 # we want to change the global counter
    record = {"name": name, "roll_no": roll_no, "marks": marks, "department": department}
    student_list.append(record)
    student_count += 1
    return record


def calculate_average(marks):
    """Average of a list of marks (0 if the list is empty)."""
    if len(marks) == 0:
        return 0
    return sum(marks) / len(marks)


def get_grade(average):
    """Turn an average into a grade letter."""
    if average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    return "F"


def display_student(record, show_grade=True):
    """Print one student. show_grade has a default value of True."""
    average = calculate_average(record["marks"])
    line = (f"{record['roll_no']} | {record['name']:<7} | {record['department']:<8} | "
            f"marks {record['marks']} | average {average:.1f}")
    if show_grade:
        line += f" | grade {get_grade(average)}"
    print(line)


students = []

# 1) positional arguments: the order matters
add_student(students, "Ali", 101, [78, 85, 90])

# 2) keyword arguments: the order does not matter
add_student(students, name="Sara", marks=[45, 52, 38], roll_no=102, department="Science")

# 3) default value: no department given, so "General" is used
add_student(students, "Hamza", 103, [60, 55, 70])

# positional arguments, including the department
add_student(students, "Ayesha", 104, [92, 88, 95], "Maths")
add_student(students, "Bilal", 105, [30, 42, 35])

for s in students:
    display_student(s)

print("\nUsing the default of show_grade=True, then overriding it:")
display_student(students[0])
display_student(students[0], show_grade=False)


# ## A.3 Local and global variables
# A **local** variable is created inside a function and only exists while that function runs. A **global** variable is created outside every function, so any function can read it.
# 
# In the code below, `remark` is local to `check_result`, and `passing_marks` is global. If a function wants to *change* a global variable it has to say `global` first (that is what `add_student` did with `student_count`). Without it, Python quietly creates a new local variable with the same name instead.

# In[2]:


def check_result(average):
    remark = "Pass"                     # local variable: only exists inside this function
    if average < passing_marks:         # global variable: read from outside the function
        remark = "Fail"
    return remark


print("Average 72 ->", check_result(72))
print("Average 41 ->", check_result(41))

# The local variable cannot be used outside the function
try:
    print(remark)
except NameError as error:
    print("NameError:", error)

# Global counter changed with the 'global' keyword inside add_student
print("\nStudents added so far (global counter):", student_count)


def wrong_reset():
    student_count = 0                   # this makes a NEW local variable, the global is untouched
    return student_count


wrong_reset()
print("After wrong_reset(), the global counter is still:", student_count)


# ## A.4 Lambda expression
# A lambda is a small function written in one line, without a name. Mine squares a number.

# In[3]:


square = lambda x: x ** 2

print("square(7) =", square(7))
print("square(2.5) =", square(2.5))


# ## A.5 `map()`: marks out of 100 to marks out of 10
# `map()` applies a function to every item of a list. I pass a lambda that divides each mark by 10.

# In[4]:


marks_100 = [78, 85, 90, 45, 52, 38]
marks_10 = list(map(lambda mark: mark / 10, marks_100))

print("Out of 100:", marks_100)
print("Out of 10 :", marks_10)


# ## A.6 `filter()`: students with marks of at least 50
# `filter()` keeps only the items for which the function returns `True`. I use each student's average mark as the "marks" to compare.

# In[5]:


passed = list(filter(lambda s: calculate_average(s["marks"]) >= 50, students))

print("Students with average marks of 50 or more:")
for s in passed:
    print(f"  {s['name']} ({calculate_average(s['marks']):.1f})")

failed = [s["name"] for s in students if s not in passed]
print("Filtered out:", failed)


# ## A.7 Nested functions
# A nested function is a function defined inside another function. I used two examples:
# 1. `make_report` has a small helper `format_line` inside it, because only `make_report` needs it.
# 2. `make_pass_checker` returns the inner function. The inner function remembers the `pass_mark` it was created with (this is called a closure).
# 
# Nested functions are useful because they keep helper code private (it doesn't clutter the rest of the program), and a closure can remember a value without using a global variable.

# In[6]:


def make_report(name, marks):
    def format_line(label, value):          # nested helper, only visible inside make_report
        return f"{label:<8}: {value}"

    average = calculate_average(marks)
    lines = [format_line("Name", name),
             format_line("Average", f"{average:.1f}"),
             format_line("Grade", get_grade(average))]
    return "\n".join(lines)


print(make_report("Ayesha", [92, 88, 95]))


def make_pass_checker(pass_mark):
    def check(average):                      # remembers pass_mark from the outer function
        return average >= pass_mark
    return check


is_pass_50 = make_pass_checker(50)
is_pass_70 = make_pass_checker(70)
print("\n65 passes at 50?", is_pass_50(65))
print("65 passes at 70?", is_pass_70(65))


# ---
# # B. File Handling and Exception Handling (6 Marks)
# 
# ## B.1 and B.2 Save the records to `students.txt` and read them back
# Each student is written as one line: `roll_no|name|department|mark1,mark2,...`. I used the `|` sign as separator because names can contain spaces.
# 
# Both functions use a `with` statement (B.4), and the reading function handles a missing file (B.5).

# In[7]:


FILE_NAME = "students.txt"


def to_number(text):
    """'78' -> 78 and '78.5' -> 78.5 (keeps whole numbers as int)."""
    value = float(text)
    return int(value) if value.is_integer() else value


def save_students(student_list, filename=FILE_NAME):
    """Write all student records to a text file (mode 'w' replaces the old content)."""
    with open(filename, "w") as file:
        for s in student_list:
            marks_text = ",".join(str(m) for m in s["marks"])
            file.write(f"{s['roll_no']}|{s['name']}|{s['department']}|{marks_text}\n")
    print(f"Saved {len(student_list)} records to {filename}")


def read_students(filename=FILE_NAME):
    """Read the records back. Returns an empty list if the file does not exist."""
    records = []
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                roll_no, name, department, marks_text = line.split("|")
                marks = [to_number(m) for m in marks_text.split(",")]
                records.append({"name": name, "roll_no": int(roll_no),
                                "marks": marks, "department": department})
    except FileNotFoundError:
        print(f"File '{filename}' was not found, so there is nothing to read.")
    return records


save_students(students)

print("\nRaw content of students.txt:")
with open(FILE_NAME) as file:
    print(file.read())

print("Records read back from the file:")
loaded = read_students()
for s in loaded:
    display_student(s)


# ## B.3 File modes: `r`, `w`, `a` and `x`
# | Mode | Meaning | If the file does not exist | If the file exists |
# |---|---|---|---|
# | `r` | read only (the default) | `FileNotFoundError` | opens it, starts at the beginning |
# | `w` | write | creates it | **erases** the old content and starts fresh |
# | `a` | append | creates it | keeps the content and adds new text at the end |
# | `x` | exclusive create | creates it | `FileExistsError` (it never overwrites) |
# 
# Below I try `a` and `x` on the real file.

# In[8]:


# 'a' keeps the old records and adds a new line at the end
with open(FILE_NAME, "a") as file:
    file.write("106|Zainab|General|88,91,79\n")
print("After appending with mode 'a':", len(read_students()), "records in the file")

# 'x' refuses to overwrite a file that already exists
try:
    with open(FILE_NAME, "x") as file:
        file.write("this will never be written")
except FileExistsError as error:
    print("Mode 'x' on an existing file -> FileExistsError:", error)

# 'x' works when the file is new (I remove the old backup first so this can be re-run)
import os
if os.path.exists("students_backup.txt"):
    os.remove("students_backup.txt")
with open("students_backup.txt", "x") as file:
    file.write("backup created\n")
print("Mode 'x' on a new file worked: students_backup.txt was created")


# ## B.4 The `with` statement
# `with open(...) as file:` closes the file automatically when the block ends, even if an error happens inside the block. Without it I would have to remember to call `file.close()` myself. The cell below shows the file really is closed after the block.

# In[9]:


with open(FILE_NAME) as file:
    first_line = file.readline().strip()
    print("Inside the with block, file.closed =", file.closed)

print("First line:", first_line)
print("After the with block,  file.closed =", file.closed)


# ## B.5 Handling `FileNotFoundError`
# If the file is missing, `open()` raises `FileNotFoundError`. `read_students` catches it, prints a message and returns an empty list, so the program carries on instead of crashing.

# In[10]:


missing = read_students("this_file_does_not_exist.txt")
print("Records returned:", missing)

# the same error, caught directly
try:
    open("this_file_does_not_exist.txt")
except FileNotFoundError as error:
    print("Caught directly ->", error)


# ## B.6 Invalid marks with `ValueError`, and `try` / `except` / `else` / `finally`
# `float("abc")` raises a `ValueError`. I also raise one myself when a number is outside 0-100.
# 
# * **`try`** - the code that might fail.
# * **`except`** - runs only if an error happened in the `try` block.
# * **`else`** - runs only if the `try` block finished with *no* error.
# * **`finally`** - runs **always**, whether there was an error or not (good for cleanup).

# In[11]:


def read_mark(text):
    try:
        mark = float(text)                          # may raise ValueError
        if mark < 0 or mark > 100:
            raise ValueError("marks must be between 0 and 100")
    except ValueError as error:
        print(f"  '{text}' rejected -> {error}")
        return None
    else:
        print(f"  '{text}' accepted -> {mark}")
        return mark
    finally:
        print("  (finally: this check is finished)")


for typed in ["85", "abc", "105", "-4", "72.5", ""]:
    read_mark(typed)


# ---
# # C. Classes, Objects and Variables (7 Marks)
# 
# Now I move the same idea into a class. The `Student` class below has:
# * instance variables: `name` (public), `_roll_no` (protected by convention) and `__marks` (private);
# * a **class variable** `school_name` that is shared by every student;
# * instance methods `calculate_average()` and `display_details()`;
# * a **class method** `update_school_name()` and a **static method** `is_valid_marks()`;
# * a constructor `__init__()` and a destructor `__del__()`.

# In[12]:


class Student:
    school_name = "Green Valley School"          # class variable: one copy shared by all students

    def __init__(self, name, roll_no, marks):
        """Constructor: runs automatically when a Student object is created."""
        if not Student.is_valid_marks(marks):
            raise ValueError("Marks must be a list of numbers between 0 and 100")
        self.name = name                         # public attribute
        self._roll_no = roll_no                  # protected attribute (convention: one underscore)
        self.__marks = list(marks)               # private attribute (two underscores -> name mangling)
        print(f"[init] Student object created for {name}")

    def calculate_average(self):
        return sum(self.__marks) / len(self.__marks)

    def display_details(self):
        print(f"Name: {self.name} | Roll no: {self._roll_no} | Marks: {self.__marks} | "
              f"Average: {self.calculate_average():.1f} | School: {Student.school_name}")

    @classmethod
    def update_school_name(cls, new_name):
        """Class method: works on the class itself, so it changes the shared variable."""
        cls.school_name = new_name

    @staticmethod
    def is_valid_marks(marks):
        """Static method: needs neither self nor cls, it is just a helper check."""
        return len(marks) > 0 and all(isinstance(m, (int, float)) and 0 <= m <= 100 for m in marks)

    def __del__(self):
        """Destructor: called when the object is about to be destroyed."""
        print(f"[del] Student object for {getattr(self, 'name', 'unknown')} is being destroyed")


s1 = Student("Ali", 101, [78, 85, 90])
s2 = Student("Sara", 102, [45, 52, 38])

s1.display_details()
s2.display_details()


# ## C.3 and C.4 Class variable, class method and static method
# `school_name` belongs to the class, so all objects see the same value. The class method `update_school_name` changes it once for everybody. The static method only checks marks, so I can call it without creating any object.

# In[13]:


print("Before:", s1.school_name, "|", s2.school_name, "|", Student.school_name)

Student.update_school_name("City Model School")          # class method
print("After :", s1.school_name, "|", s2.school_name, "|", Student.school_name)

# If I assign through an object, I only create a separate instance variable
s1.school_name = "Private Copy"
print("\nAfter s1.school_name = 'Private Copy':")
print("s1 sees:", s1.school_name, "| s2 sees:", s2.school_name, "| class has:", Student.school_name)
del s1.school_name                                       # remove it, s1 uses the class value again
print("After deleting it, s1 sees:", s1.school_name)

# Static method: no object needed
print("\nStudent.is_valid_marks([50, 90]) ->", Student.is_valid_marks([50, 90]))
print("Student.is_valid_marks([50, 120]) ->", Student.is_valid_marks([50, 120]))

try:
    Student("Bad Data", 999, [50, 120])
except ValueError as error:
    print("\nCreating a student with invalid marks -> ValueError:", error)


# ## C.5 The constructor `__init__()`
# `__init__()` is the constructor. An object is initialised at the moment it is created: when I write `Student("Ali", 101, [...])`, Python first makes an empty object and then immediately calls `__init__` on it to set up its attributes. That is why the `[init]` message was printed as soon as `s1` and `s2` were created. My `__init__` also checks the marks, so a student with invalid marks is never created.
# 
# One small thing I noticed in the next cell: after the failed attempt with invalid marks, a `[del] ... unknown` line is printed. Python still throws away the half-built object, and `__del__` runs on it. The `name` was never set at that point, which is why I wrote `getattr(self, 'name', 'unknown')` in `__del__`.
# 
# ## C.7 Public, protected and private attributes, and name mangling

# In[14]:


print("Public    s1.name      ->", s1.name)
print("Protected s1._roll_no  ->", s1._roll_no, " (works, but the underscore says 'please do not touch')")

try:
    print(s1.__marks)
except AttributeError as error:
    print("Private   s1.__marks   -> AttributeError:", error)

print("Mangled   s1._Student__marks ->", s1._Student__marks)
print("\nAttributes stored in the object:", list(s1.__dict__.keys()))


# **Name mangling:** when an attribute starts with two underscores (and does not end with two), Python renames it inside the class to `_ClassName__name`. So `__marks` really becomes `_Student__marks`. This is why `s1.__marks` fails from outside but the code inside the class still works.
# 
# **Why Python is different from Java or C++:** in those languages `private` is enforced by the compiler, and outside code simply cannot access it. Python follows the idea "we are all consenting adults". A single underscore is only a convention, and the double underscore only prevents accidents (for example a subclass accidentally overwriting a parent's attribute). Anyone who really wants to can still reach it, as I did with `_Student__marks`.
# 
# ## C.6 The destructor `__del__()`
# `__del__` is called when an object is about to be destroyed (for example when no variable refers to it any more). I use `del s2` to remove the last reference:

# In[15]:


del s2
print("s2 has been deleted")


# **Why it should not be used for important cleanup:** Python does not promise *when* (or even *if*) `__del__` runs. It can be delayed by the garbage collector, it may not run at all when the program exits or when objects refer to each other in a cycle, and an error raised inside it is only printed and ignored. Other Python implementations also behave differently. For important work, like closing a file or a connection, it is safer to use a `with` statement or `try`/`finally`.

# ---
# # D. Inheritance and Method Resolution Order (7 Marks)
# 
# From here on the `Student` class is **rebuilt on top of a `Person` base class**. It has the same features as in part C (class variable, class method, static method, protected and private attributes), but it now reuses `Person` through `super()`. I also added `display_info()` and two small methods, `to_line()` and `from_line()`, that part H uses for the file.
# 
# ## D.1 and D.2 `Person` and `Student(Person)`

# In[16]:


class Person:
    """Base class: every person has a name."""
    def __init__(self, name):
        self.name = name

    def display_name(self):
        print(f"Name: {self.name}")

    def display_info(self):                  # will be overridden in the subclasses (part F)
        print(f"Person: {self.name}")


class Student(Person):
    school_name = "Green Valley School"

    def __init__(self, name, roll_no, marks):
        super().__init__(name)               # let Person set up the name
        if not Student.is_valid_marks(marks):
            raise ValueError("Marks must be a list of numbers between 0 and 100")
        self._roll_no = roll_no
        self.__marks = list(marks)

    def get_marks(self):
        return list(self.__marks)

    def get_roll_no(self):
        return self._roll_no

    def calculate_average(self):
        return sum(self.__marks) / len(self.__marks)

    def get_grade(self):
        return get_grade(self.calculate_average())          # the function from part A

    def display_details(self):
        print(f"Name: {self.name} | Roll no: {self._roll_no} | Marks: {self.__marks} | "
              f"Average: {self.calculate_average():.1f} | Grade: {self.get_grade()} | "
              f"School: {Student.school_name}")

    def display_info(self):                  # overrides Person.display_info
        print(f"Student -> {self.name} (roll no {self._roll_no}), average {self.calculate_average():.1f}")

    @classmethod
    def update_school_name(cls, new_name):
        cls.school_name = new_name

    @staticmethod
    def is_valid_marks(marks):
        return len(marks) > 0 and all(isinstance(m, (int, float)) and 0 <= m <= 100 for m in marks)

    def to_line(self):
        """One line of text for the file: roll_no|name|mark1,mark2,..."""
        return f"{self._roll_no}|{self.name}|{','.join(str(m) for m in self.__marks)}"

    @classmethod
    def from_line(cls, line):
        """Build a Student from a line written by to_line(). Raises ValueError for a bad line."""
        parts = line.strip().split("|")
        if len(parts) != 3:
            raise ValueError(f"bad record (expected 3 fields): {line.strip()!r}")
        roll_text, name, marks_text = parts
        return cls(name, int(roll_text), [float(m) for m in marks_text.split(",")])


p = Person("Imran")
p.display_name()

stu = Student("Ali", 101, [78, 85, 90])
stu.display_name()                           # inherited from Person
stu.display_details()
print("Is Student a Person?", isinstance(stu, Person))


# ## D.3 Multilevel inheritance: Person → Student → GraduateStudent
# In multilevel inheritance a class inherits from a class that already inherits from another one. `GraduateStudent` gets everything from `Student` and, through it, from `Person`. It adds a thesis title, and its `display_details()` calls the parent version with `super()` first and then prints its own extra line.

# In[17]:


class GraduateStudent(Student):
    def __init__(self, name, roll_no, marks, thesis_title):
        super().__init__(name, roll_no, marks)
        self.thesis_title = thesis_title

    def display_details(self):
        super().display_details()            # reuse the Student version
        print(f"   Thesis: {self.thesis_title}")


grad = GraduateStudent("Hira", 201, [85, 90, 88], "Machine Learning for Crop Prediction")
grad.display_details()
grad.display_name()                          # comes all the way from Person


# ## D.4 Hierarchical inheritance: several subclasses of one parent
# Here more than one class inherits from the same parent. `Student`, `Teacher` and `OfficeStaff` are all subclasses of `Person` (I made two new ones, `Teacher` and `OfficeStaff`).

# In[18]:


class Teacher(Person):
    def __init__(self, name, subject):
        super().__init__(name)
        self.subject = subject

    def display_info(self):
        print(f"Teacher -> {self.name}, teaches {self.subject}")


class OfficeStaff(Person):
    def __init__(self, name, office):
        super().__init__(name)
        self.office = office

    def display_info(self):
        print(f"Office staff -> {self.name}, works in {self.office}")


print("Direct subclasses of Person:", [cls.__name__ for cls in Person.__subclasses__()])
Teacher("Mr. Usman", "Computer Science").display_info()
OfficeStaff("Mrs. Farah", "Admissions").display_info()


# ## D.5 Multiple inheritance: one child, two parents
# `StudentAthlete` inherits from two parents, `Student` and a separate class `Athlete`. It has the features of both.

# In[19]:


class Athlete:
    def __init__(self, sport):
        self.sport = sport

    def train(self):
        print(f"Training for {self.sport}")


class StudentAthlete(Student, Athlete):
    def __init__(self, name, roll_no, marks, sport):
        Student.__init__(self, name, roll_no, marks)     # set up the first parent
        Athlete.__init__(self, sport)                    # set up the second parent


sa = StudentAthlete("Hamza", 103, [60, 55, 70], "Cricket")
sa.display_details()          # from Student
sa.train()                    # from Athlete


# ## D.6 Method Resolution Order (MRO)
# The MRO is the order in which Python looks through the classes when it searches for a method or attribute. Python takes the first class in this order that has the name. The rules (called C3 linearisation) are: a child always comes before its parents, and the parents are kept in the left-to-right order I wrote them in. `mro()` shows the order.

# In[20]:


print("StudentAthlete :", [c.__name__ for c in StudentAthlete.mro()])
print("GraduateStudent:", [c.__name__ for c in GraduateStudent.mro()])


# A diamond shape, where the order really matters
class A:
    def hello(self): return "hello from A"

class B(A):
    def hello(self): return "hello from B"

class C(A):
    def hello(self): return "hello from C"

class D(B, C):
    pass


print("\nDiamond D(B, C):", [c.__name__ for c in D.mro()])
print("D().hello() ->", D().hello(), " (B comes before C in the MRO)")


# ## D.7 How `super()` helps
# `super()` gives access to the next class in the MRO, so a subclass can reuse the parent's code instead of copying it. In this notebook:
# * `Student.__init__` calls `super().__init__(name)`, so the name is set up in only one place (`Person`);
# * `GraduateStudent.display_details` calls `super().display_details()` and then only adds the thesis line.
# 
# If the parent changes later, the child gets the change automatically.

# ---
# # E. Relationships Between Classes (5 Marks)
# 
# First I extend the `Student` class once more. The new class has the same name, so it replaces the old one. It adds a `teacher` link (for the association) and the nested class `ContactInfo` (E.5).

# In[21]:


class Student(Student):
    """The same Student as before, plus a teacher link and a nested ContactInfo class."""

    class ContactInfo:                       # nested class: it lives inside Student
        def __init__(self, phone, email):
            self.phone = phone
            self.email = email

        def show(self):
            print(f"Phone: {self.phone} | Email: {self.email}")

    def __init__(self, name, roll_no, marks):
        super().__init__(name, roll_no, marks)
        self.teacher = None
        self.contact = None

    def assign_teacher(self, teacher):
        self.teacher = teacher

    def set_contact(self, phone, email):
        self.contact = Student.ContactInfo(phone, email)


# ## E.1 Association: student and teacher
# Association is the loosest relationship: one object just *knows about* or *uses* another. A student has a teacher, but both exist on their own. Neither one owns the other.

# In[22]:


teacher_a = Teacher("Mr. Usman", "Computer Science")
student_a = Student("Ali", 101, [78, 85, 90])

student_a.assign_teacher(teacher_a)
print(f"{student_a.name}'s teacher is {student_a.teacher.name} ({student_a.teacher.subject})")

# Both objects are independent: deleting the student does not delete the teacher
del student_a
print("After deleting the student, the teacher still exists:", teacher_a.name)


# ## E.2 Aggregation: department and students
# In aggregation the whole holds references to its parts, but the parts can live without it. A `Department` keeps a list of students. If the department is deleted, the students are still there.

# In[23]:


class Department:
    def __init__(self, name):
        self.name = name
        self.students = []                   # students are created outside and only added here

    def add_student(self, student):
        self.students.append(student)

    def show_students(self):
        print(f"Department of {self.name}:")
        for s in self.students:
            print("  -", s.name)


ali = Student("Ali", 101, [78, 85, 90])
sara = Student("Sara", 102, [45, 52, 38])

cs_department = Department("Computer Science")
cs_department.add_student(ali)
cs_department.add_student(sara)
cs_department.show_students()

del cs_department                            # the department is gone...
print("\nDepartment deleted, but the students still exist:", ali.name, "and", sara.name)


# ## E.3 Composition: a student record owns its result card
# In composition the whole *creates and owns* its part, so the part cannot live without it. A `StudentRecord` creates its own `ResultCard` inside `__init__`. Nobody else gets the card, and when the record is deleted the card is destroyed with it. (I use `__del__` here only to make that visible.)

# In[24]:


class ResultCard:
    def __init__(self, owner, marks):
        self.owner = owner
        self.marks = marks

    def __del__(self):
        print(f"   ResultCard of {self.owner} destroyed")


class StudentRecord:
    def __init__(self, name, marks):
        self.name = name
        self.result_card = ResultCard(name, marks)    # created and owned inside the record


record = StudentRecord("Hira", [85, 90, 88])
print("Record created for", record.name, "with a card holding", record.result_card.marks)

print("Deleting the record...")
del record
print("Done: the result card was destroyed together with its record.")


# ## E.4 Association vs aggregation vs composition
# | | Association | Aggregation | Composition |
# |---|---|---|---|
# | Idea | one object *uses* or *knows* another | a whole *has* parts | a whole *owns* its parts |
# | Strength | weakest | medium | strongest |
# | Can the part live alone? | yes | yes | **no** |
# | Who creates the part? | anyone | usually created outside and passed in | created inside the whole |
# | My example | Student and Teacher | Department and Students | StudentRecord and ResultCard |
# 
# ## E.5 The nested class `ContactInfo`
# `ContactInfo` is written inside the `Student` class, so it is reached as `Student.ContactInfo`. I can create an object of it directly, or let a student create one with `set_contact()`. (The phone number and email are made-up examples.)

# In[25]:


# Creating a ContactInfo object directly
info = Student.ContactInfo("0300-0000000", "example@example.com")
info.show()

# A student keeps a ContactInfo object and I read it through the student
ali.set_contact("0311-1111111", "ali@example.com")
print("\nali.contact.phone :", ali.contact.phone)
print("ali.contact.email :", ali.contact.email)
ali.contact.show()


# ---
# # F. Polymorphism and Operator Overloading (6 Marks)
# 
# ## F.1 and F.2 `display_info()` in `Person`, overridden in `Student` and `Teacher`
# `Person` has a `display_info()` method (from part D). `Student` and `Teacher` each override it, which means they write their own version with the same name. The check below shows the three versions are different functions.

# In[26]:


print("Person.display_info  is Student.display_info ?", Person.display_info is Student.display_info)
print("Person.display_info  is Teacher.display_info ?", Person.display_info is Teacher.display_info)


# ## F.3 Dynamic polymorphism
# The function `show_info(person)` just calls `person.display_info()`. It never checks whether the object is a student or a teacher. Python decides which version to run **at run time**, from the real type of the object. This is dynamic polymorphism: one call, different behaviour. I can even add a new kind of person later and the function will still work without any change.

# In[27]:


def show_info(person):
    person.display_info()                    # no if/else on the type


people = [Student("Ali", 101, [78, 85, 90]),
          Teacher("Mr. Usman", "Computer Science"),
          OfficeStaff("Mrs. Farah", "Admissions"),
          Person("Imran")]

for person in people:
    show_info(person)


# ## F.4 and F.5 Operator overloading and dunder methods
# Dunder methods (double underscore) let my own classes work with Python's built-in syntax. In the `Marks` class:
# * `__add__` makes the `+` operator combine the marks of two `Marks` objects;
# * `__len__` makes `len(marks_object)` work;
# * `__str__` controls what `print()` shows, and `__repr__` is the developer view.

# In[28]:


class Marks:
    def __init__(self, values):
        self.values = list(values)

    def __add__(self, other):                # called for  marks1 + marks2
        return Marks(self.values + other.values)

    def __len__(self):                       # called for  len(marks)
        return len(self.values)

    def __str__(self):                       # called by print()
        return "Marks(" + ", ".join(str(v) for v in self.values) + ")"

    def __repr__(self):
        return f"Marks({self.values})"

    def average(self):
        return sum(self.values) / len(self.values)


term1 = Marks([78, 85, 90])
term2 = Marks([60, 72])

total = term1 + term2                        # uses __add__
print("term1       :", term1)
print("term2       :", term2)
print("term1+term2 :", total)
print("len(total)  :", len(total))
print("average     :", round(total.average(), 2))
print("repr(total) :", repr(total))


# ## F.6 Overriding vs operator overloading vs method overloading
# * **Method overriding:** a subclass writes its own version of a method that the parent already has (`Student.display_info` replacing `Person.display_info`).
# * **Operator overloading:** a class defines a dunder method such as `__add__` so an operator like `+` works for its objects.
# * **Method overloading:** several methods with the same name but different parameter lists. Python does **not** support the traditional kind. If I define the same name twice, the second one simply replaces the first. In Python I get the same result with default arguments or `*args`.

# In[29]:


class Shape:
    def area(self, a):                       # first version
        return a * a

    def area(self, a, b):                    # this REPLACES the first one
        return a * b


shape = Shape()
print("area(4, 5) ->", shape.area(4, 5))
try:
    shape.area(4)
except TypeError as error:
    print("area(4)    -> TypeError:", error)


class FlexibleShape:
    def area(self, a, b=None):               # one method with a default argument does both jobs
        return a * a if b is None else a * b


flexible = FlexibleShape()
print("\nWith a default argument: area(4) =", flexible.area(4), "and area(4, 5) =", flexible.area(4, 5))


# ---
# # G. Abstract Classes, Data Classes and Empty Classes (6 Marks)
# 
# ## G.1 and G.2 Abstract class `Record`
# `Record` uses `ABC` and has an abstract method `display()`. An abstract class is a template. It says "every record must have a `display()`" but does not say how. A class with an unimplemented abstract method is incomplete, so Python refuses to create an object of it (`TypeError`). A subclass must implement every abstract method before it can be instantiated.

# In[30]:


from abc import ABC, abstractmethod


class Record(ABC):
    @abstractmethod
    def display(self):
        """Every kind of record must show itself."""


class ResultSummary(Record):                 # concrete subclass: implements display()
    def __init__(self, student_name, average):
        self.student_name = student_name
        self.average = average

    def display(self):
        print(f"Result summary -> {self.student_name}: average {self.average}")


try:
    record = Record()                        # not allowed
except TypeError as error:
    print("Record() -> TypeError:", error)

summary = ResultSummary("Ali", 84.3)
summary.display()


# ## G.3 Empty class `TemporaryRecord`
# An empty class has only `pass` in its body. It is useful as a placeholder while a design is still in progress, as a simple container where I can attach attributes on the fly, or as a marker type (a custom exception is often just an empty class too).

# In[31]:


class TemporaryRecord:
    pass


temp = TemporaryRecord()
temp.student = "Ali"                         # attributes can be added later
temp.note = "waiting for the final marks"
print(temp.student, "-", temp.note)
print("Attributes:", temp.__dict__)


# ## G.4 and G.5 The `@dataclass` named `Course`
# A data class is meant for classes that mostly just hold data. The `@dataclass` decorator writes `__init__`, `__repr__` and `__eq__` for me. To compare, I also wrote the same `Course` by hand as `CourseManual`.

# In[32]:


from dataclasses import dataclass, fields


@dataclass
class Course:
    name: str
    code: str
    credit_hours: int


class CourseManual:                          # the same thing written by hand
    def __init__(self, name, code, credit_hours):
        self.name = name
        self.code = code
        self.credit_hours = credit_hours

    def __repr__(self):
        return f"CourseManual(name={self.name!r}, code={self.code!r}, credit_hours={self.credit_hours!r})"

    def __eq__(self, other):
        return (self.name, self.code, self.credit_hours) == (other.name, other.code, other.credit_hours)


c1 = Course("Python Programming", "CS101", 3)
c2 = Course("Data Structures", "CS201", 4)
c3 = Course("Python Programming", "CS101", 3)

print(c1)                                    # __repr__ was written automatically
print(c2)
print("c1 == c3 ?", c1 == c3, "(equal because all the fields match)")
print("c1 == c2 ?", c1 == c2)
print("Fields:", [f.name for f in fields(Course)])
print("\nCourse needs 5 lines, CourseManual needs about 12 lines for the same behaviour.")


# ## G.6 Regular class vs abstract class vs data class
# | | Regular class | Abstract class | Data class |
# |---|---|---|---|
# | Purpose | general use, data and behaviour | a template that other classes must complete | mostly holds data |
# | Can I create objects? | yes | **no**, not while abstract methods are unimplemented | yes |
# | Methods | I write everything myself | has abstract methods that subclasses must implement | `__init__`, `__repr__`, `__eq__` are generated |
# | How it is written | `class Student:` | `class Record(ABC)` with `@abstractmethod` | `@dataclass class Course:` |
# | Example here | `Student` | `Record` | `Course` |

# ---
# # H. Integration and Code Quality (5 Marks)
# 
# Now I combine everything into one small application. It:
# 1. creates **two student objects and one teacher object** (more are used in the tests);
# 2. uses **functions and class methods** to manage the data (`save_students_to_file`, `load_students_from_file`, `Student.from_line`, `Student.update_school_name`);
# 3. shows different kinds of people through **inheritance and polymorphism**;
# 4. **saves and reads** the students from a file;
# 5. **handles invalid input and missing files** without crashing.

# In[33]:


APP_FILE = "students_app.txt"


def create_student_safely(name, roll_text, marks_text):
    """Build a Student from typed text. Returns None (and explains why) if the input is invalid."""
    try:
        name = name.strip()
        if name == "":
            raise ValueError("the name cannot be empty")
        roll_no = int(roll_text)                                   # ValueError if not a whole number
        marks = [float(m) for m in marks_text.split(",")]          # ValueError if a mark is not a number
        return Student(name, roll_no, marks)                       # ValueError if marks are out of range
    except ValueError as error:
        print(f"  Could not create student {name!r}: {error}")
        return None


def save_students_to_file(student_list, filename=APP_FILE):
    with open(filename, "w") as file:
        for student in student_list:
            file.write(student.to_line() + "\n")
    print(f"Saved {len(student_list)} students to {filename}")


def load_students_from_file(filename=APP_FILE):
    """Read students from a file. A missing file gives an empty list, bad lines are skipped."""
    loaded, skipped = [], 0
    try:
        with open(filename) as file:
            for line in file:
                if line.strip() == "":
                    continue
                try:
                    loaded.append(Student.from_line(line))
                except ValueError as error:
                    skipped += 1
                    print(f"  Skipping a bad line: {error}")
    except FileNotFoundError:
        print(f"File '{filename}' not found. Starting with an empty list.")
    print(f"Loaded {len(loaded)} students from {filename}" + (f" ({skipped} bad line(s) skipped)" if skipped else ""))
    return loaded


def show_everyone(people):
    """Polymorphism: each object prints itself in its own way."""
    for person in people:
        person.display_info()


print("Helper functions are ready.")


# ## H.1 to H.4 Running the application

# In[34]:


print("--- Step 1: create two students and one teacher ---")
Student.update_school_name("Green Valley School")        # class method
student_1 = create_student_safely("Ali Khan", "101", "78, 85, 90")
student_2 = create_student_safely("Sara Ahmed", "102", "45, 52, 38")
teacher = Teacher("Mr. Usman", "Computer Science")
student_1.assign_teacher(teacher)
student_2.assign_teacher(teacher)

print("\n--- Step 2: show them (inheritance + polymorphism) ---")
show_everyone([student_1, student_2, teacher])
print()
student_1.display_details()
student_2.display_details()
print(f"{student_1.name}'s teacher: {student_1.teacher.name}")

print("\n--- Step 3: save to a file ---")
save_students_to_file([student_1, student_2])
with open(APP_FILE) as file:
    print("File content:\n" + file.read())

print("--- Step 4: read the students back from the file ---")
students_from_file = load_students_from_file()
for student in students_from_file:
    student.display_details()


# ## H.5 Testing with valid and invalid data
# Here I test the program with good data and with bad data. The program should never crash: it should explain the problem and carry on.

# In[35]:


print("=== Valid data ===")
valid = create_student_safely("Zara Noor", "103", "80, 91, 77")
print("Created:", valid.name if valid else None)

print("\n=== Invalid data (each one should be rejected with a message) ===")
bad_inputs = [
    ("Marks with letters",   ("Test", "104", "80, abc, 77")),
    ("Mark above 100",       ("Test", "105", "80, 120, 77")),
    ("Negative mark",        ("Test", "106", "-5, 60")),
    ("Roll number not int",  ("Test", "x1", "50, 60")),
    ("Empty name",           ("   ", "107", "50, 60")),
    ("Empty marks",          ("Test", "108", "")),
]
results = []
for label, (name, roll, marks_text) in bad_inputs:
    print(f"{label}:")
    results.append(create_student_safely(name, roll, marks_text) is None)

print("\n=== Missing file ===")
nothing = load_students_from_file("no_such_file.txt")
print("Returned list:", nothing)

print("\n=== File that contains a damaged line ===")
with open("students_damaged.txt", "w") as file:
    file.write(student_1.to_line() + "\n")
    file.write("this line is damaged\n")
    file.write("999|Only Two Fields\n")
    file.write(student_2.to_line() + "\n")
recovered = load_students_from_file("students_damaged.txt")
print("Students recovered:", [s.name for s in recovered])

print("\n=== Test summary ===")
print("All 6 invalid inputs were rejected :", all(results))
print("Missing file handled (empty list)  :", nothing == [])
print("Damaged file: 2 good lines loaded  :", len(recovered) == 2)


# ---
# ## Summary of what I demonstrated
# | Part | Concepts shown in code |
# |---|---|
# | A | functions, positional/keyword/default arguments, local and global scope, lambda, `map`, `filter`, nested functions and closures |
# | B | writing, reading and appending files, modes `r`/`w`/`a`/`x`, `with`, `FileNotFoundError`, `ValueError`, `try`/`except`/`else`/`finally` |
# | C | instance and class variables, `__init__`, `__del__`, class method, static method, public/protected/private, name mangling |
# | D | single, multilevel, hierarchical and multiple inheritance, MRO, `super()` |
# | E | association, aggregation, composition, nested class `ContactInfo` |
# | F | overriding, dynamic polymorphism, `__add__`, `__len__`, `__str__`, `__repr__`, why Python has no real method overloading |
# | G | abstract class with `ABC`, empty class, `@dataclass` |
# | H | one application that uses all of the above with valid and invalid data |
