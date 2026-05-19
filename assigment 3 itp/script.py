# Имя: [MATZHAN ARLAN]
# Группа: [SE 2505]

import math
import csv
import os
from abc import ABC, abstractmethod

# TASK 1: Function Arguments (Required, Keyword, Default)
def create_profile(name, age, city="Astana", **kwargs):
    print(f"Name: {name}")
    print(f"Age: {age}")
    print(f"City: {city}")
    for key, value in kwargs.items():
        print(f"{key.capitalize()}: {value}")

print("--- Task 1 ---")
create_profile("Alice", 25)
create_profile("Bob", 30, city="Almaty")

u_name = input("Enter name: ")
u_age = input("Enter age: ")
u_hobby = input("Enter a hobby: ")
create_profile(u_name, u_age, hobby=u_hobby)


# TASK 2: Lambda, Map, and Filter
print("\n--- Task 2 ---")
nums_str = input("Enter a list of numbers (separated by spaces): ")
nums = list(map(int, nums_str.split()))
threshold = int(input("Enter threshold X: "))

squared = list(map(lambda x: x**2, nums))
evens = list(filter(lambda x: x % 2 == 0, nums))
greater_than_x = list(filter(lambda x: x > threshold, nums))

print(f"Original list: {nums}")
print(f"Squared numbers: {squared}")
print(f"Even numbers: {evens}")
print(f"Numbers greater than {threshold}: {greater_than_x}")


# TASK 3: Basic Class and Object
class Book:
    def __init__(self, title="", author="", pages=0):
        self.title = title
        self.author = author
        self.pages = pages

    def describe(self):
        print(f"The book '{self.title}' by {self.author} has {self.pages} pages.")

print("\n--- Task 3 ---")
book1 = Book("To Kill a Mockingbird", "Harper Lee", 281)
book2 = Book("The Great Gatsby", "F. Scott Fitzgerald", 180)

print("Enter a new book details:")
u_title = input("Title: ")
u_author = input("Author: ")
u_pages = int(input("Number of pages: "))
book3 = Book(u_title, u_author, u_pages)

book1.describe()
book2.describe()
book3.describe()


# TASK 4: Class with __init__ and __str__
class Rectangle:
    def __init__(self, width, height):
        self.width = float(width)
        self.height = float(height)

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def __str__(self):
        return f"Rectangle(width={self.width}, height={self.height})"

print("\n--- Task 4 ---")
r_w = input("Enter rectangle width: ")
r_h = input("Enter rectangle height: ")
rect = Rectangle(r_w, r_h)
print(rect)
print(f"Area: {rect.area()}")
print(f"Perimeter: {rect.perimeter()}")


# TASK 5: Single Inheritance
class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def display_info(self):
        print(f"Vehicle: {self.make} {self.model} ({self.year})")

class Car(Vehicle):
    def __init__(self, make, model, year, num_doors):
        super().__init__(make, model, year)
        self.num_doors = num_doors

    def honk(self):
        print("Beep beep!")

print("\n--- Task 5 ---")
c_make = input("Car Make: ")
c_model = input("Car Model: ")
c_year = input("Year: ")
c_doors = input("Number of doors: ")

my_car = Car(c_make, c_model, c_year, c_doors)
my_car.display_info()
print(f"Doors: {my_car.num_doors}")
my_car.honk()


# TASK 6: Method Overriding and Polymorphism
class Shape:
    def area(self):
        return 0
    def describe(self):
        print("This is a shape.")

class Circle(Shape):
    def __init__(self, radius):
        self.radius = float(radius)
    def area(self):
        return round(math.pi * (self.radius ** 2), 2)
    def describe(self):
        print(f"This is a circle with radius {self.radius}.")

class Square(Shape):
    def __init__(self, side):
        self.side = float(side)
    def area(self):
        return self.side * self.side
    def describe(self):
        print(f"This is a square with side {self.side}.")

print("\n--- Task 6 ---")
c_rad = input("Enter radius for the circle: ")
s_side = input("Enter side length for the square: ")

shapes = [Circle(c_rad), Square(s_side)]
for s in shapes:
    s.describe()
    print(f"Area: {s.area()}")


# TASK 7: Association
class Author:
    def __init__(self, name, nationality):
        self.name = name
        self.nationality = nationality
    def get_info(self):
        return f"{self.name} ({self.nationality})"

class LibraryBook: # Renamed to avoid conflict with Task 3
    def __init__(self, title, year, author_obj):
        self.title = title
        self.year = year
        self.author = author_obj
    def get_book_info(self):
        print(f"Book: \"{self.title}\" ({self.year})")
        print(f"Author: {self.author.get_info()}")

print("\n--- Task 7 ---")
auth_n = input("Author Name: ")
auth_nat = input("Author Nationality: ")
b_title = input("Book Title: ")
b_year = input("Publication Year: ")

author = Author(auth_n, auth_nat)
lib_book = LibraryBook(b_title, b_year, author)
lib_book.get_book_info()


# TASK 8: File I/O with Class Serialization
class Student:
    def __init__(self, name, id, grades):
        self.name = name
        self.id = id
        self.grades = grades

    def average_grade(self):
        return round(sum(self.grades) / len(self.grades), 1)

    def to_file_string(self):
        grades_str = ",".join(map(str, self.grades))
        return f"{self.name}|{self.id}|{grades_str}"

    @classmethod
    def from_file_string(cls, line):
        parts = line.strip().split("|")
        name = parts[0]
        st_id = parts[1]
        grades = list(map(int, parts[2].split(",")))
        return cls(name, st_id, grades)

print("\n--- Task 8 ---")
students = [Student("Alice", "001", [85, 90, 92]), Student("Bob", "002", [70, 80, 75])]
s_name = input("Enter new student name: ")
s_id = input("Enter student ID: ")
s_grades = list(map(int, input("Enter three grades (spaces): ").split()))
students.append(Student(s_name, s_id, s_grades))

with open("students.txt", "w") as f:
    for s in students:
        f.write(s.to_file_string() + "\n")
print("Data written to students.txt.")

loaded_students = []
with open("students.txt", "r") as f:
    for line in f:
        loaded_students.append(Student.from_file_string(line))

print("--- Loaded Students ---")
for s in loaded_students:
    print(f"{s.name} (ID: {s.id}) - Average: {s.average_grade()}")


# TASK 9: CSV Processing with Classes
class Employee:
    def __init__(self, name, age, department, salary):
        self.name = name
        self.age = age
        self.department = department
        self.salary = float(salary)

    def give_raise(self, percent):
        self.salary += self.salary * (percent / 100)

    def to_dict(self):
        return {"name": self.name, "age": self.age, "department": self.department, "salary": self.salary}

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['age'], data['department'], data['salary'])

print("\n--- Task 9 ---")
employees = [Employee("Alice", 25, "HR", 50000), Employee("Bob", 30, "Dev", 60000)]
e_name = input("New Employee Name: ")
e_age = input("Age: ")
e_dept = input("Department: ")
e_sal = input("Salary: ")
employees.append(Employee(e_name, e_age, e_dept, e_sal))

with open("employees.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age", "department", "salary"])
    writer.writeheader()
    for e in employees:
        writer.writerow(e.to_dict())
print(f"Written {len(employees)} employees to employees.csv")

new_emps = []
with open("employees.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        new_emps.append(Employee.from_dict(row))

for e in new_emps:
    e.give_raise(5)
print("Applied 5% raise to all employees.")

with open("employees_updated.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age", "department", "salary"])
    writer.writeheader()
    for e in new_emps:
        writer.writerow(e.to_dict())
print("Updated data written to employees_updated.csv")


# TASK 10: Employee Management System
class BaseEmployee(ABC):
    def __init__(self, name, emp_id):
        self.name = name
        self.emp_id = emp_id
    @abstractmethod
    def calculate_pay(self): pass
    @abstractmethod
    def to_csv_row(self): pass

class HourlyEmployee(BaseEmployee):
    def __init__(self, name, emp_id, hours, rate):
        super().__init__(name, emp_id)
        self.hours, self.rate = float(hours), float(rate)
    def calculate_pay(self): return self.hours * self.rate
    def to_csv_row(self): return ["Hourly", self.name, self.emp_id, self.hours, self.rate]

class SalariedEmployee(BaseEmployee):
    def __init__(self, name, emp_id, salary):
        super().__init__(name, emp_id)
        self.salary = float(salary)
    def calculate_pay(self): return self.salary / 12
    def to_csv_row(self): return ["Salaried", self.name, self.emp_id, self.salary]

class CommissionEmployee(BaseEmployee):
    def __init__(self, name, emp_id, sales, rate):
        super().__init__(name, emp_id)
        self.sales, self.rate = float(sales), float(rate)
    def calculate_pay(self): return self.sales * (self.rate / 100)
    def to_csv_row(self): return ["Commission", self.name, self.emp_id, self.sales, self.rate]

print("\n--- Task 10 ---")
ems_list = []
while True:
    print("\n1. Add Employee\n2. Save to File\n3. Load from File\n4. Payroll Report\n5. Exit")
    opt = input("Choose option: ")
    if opt == '1':
        t = input("Type (1:Hourly, 2:Salaried, 3:Commission): ")
        n = input("Name: ")
        i = input("ID: ")
        if t == '1': ems_list.append(HourlyEmployee(n, i, input("Hours: "), input("Rate: ")))
        elif t == '2': ems_list.append(SalariedEmployee(n, i, input("Annual Salary: ")))
        elif t == '3': ems_list.append(CommissionEmployee(n, i, input("Sales: "), input("Rate %: ")))
    elif opt == '2':
        with open("ems.csv", "w", newline="") as f:
            csv.writer(f).writerows([e.to_csv_row() for e in ems_list])
        print("Saved.")
    elif opt == '3':
        ems_list = []
        with open("ems.csv", "r") as f:
            for r in csv.reader(f):
                if r[0] == "Hourly": ems_list.append(HourlyEmployee(r[1], r[2], r[3], r[4]))
                elif r[0] == "Salaried": ems_list.append(SalariedEmployee(r[1], r[2], r[3]))
                elif r[0] == "Commission": ems_list.append(CommissionEmployee(r[1], r[2], r[3], r[4]))
        print("Loaded.")
    elif opt == '4':
        print("\nPayroll Report:")
        for e in ems_list:
            print(f"{e.name} ({type(e).__name__}) - Monthly Pay: ${e.calculate_pay():.2f}")
    elif opt == '5': break