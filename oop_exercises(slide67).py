"""OOP exercises: operator overloading and inheritance."""
import math


# =====================================================================
# PART 1: OPERATOR OVERLOADING
# =====================================================================

# ---- Problem 1: Complex number ---------------------------------------
class Complex:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        return Complex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return Complex(self.real - other.real, self.imag - other.imag)

    def __eq__(self, other):
        return self.real == other.real and self.imag == other.imag

    def __repr__(self):
        sign = "+" if self.imag >= 0 else "-"
        return f"({self.real} {sign} {abs(self.imag)}i)"


# ---- Problem 2: Person compared by age -------------------------------
class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __gt__(self, other):
        return self.age > other.age


# ---- Problem 4: Vector dot product -----------------------------------
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, other):
        # dot product: x1*x2 + y1*y2 + z1*z2
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"


# ---- Problem 5: Circle, all comparison operators ---------------------
class Circle:
    def __init__(self, radius):
        self.radius = radius

    def __lt__(self, other):
        return self.radius < other.radius

    def __gt__(self, other):
        return self.radius > other.radius

    def __eq__(self, other):
        return self.radius == other.radius

    def __ne__(self, other):
        return self.radius != other.radius

    def __ge__(self, other):
        return self.radius >= other.radius

    def __le__(self, other):
        return self.radius <= other.radius


# ---- Problem 6: 2D point compared by distance from the origin --------
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self):
        # Euclidean distance from the origin: sqrt(x^2 + y^2)
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __lt__(self, other):
        return self.distance() < other.distance()

    def __gt__(self, other):
        return self.distance() > other.distance()

    def __eq__(self, other):
        return math.isclose(self.distance(), other.distance())

    def __ne__(self, other):
        return not self == other

    def __ge__(self, other):
        return self > other or self == other

    def __le__(self, other):
        return self < other or self == other


# ---- Problem 7: Matrix multiplication --------------------------------
class Matrix:
    def __init__(self, rows):
        self.rows = rows  # list of lists

    def __mul__(self, other):
        # (m x n) * (n x p) -> (m x p)
        if len(self.rows[0]) != len(other.rows):
            raise ValueError("Incompatible dimensions for multiplication")
        result = []
        for i in range(len(self.rows)):
            new_row = []
            for j in range(len(other.rows[0])):
                total = 0
                for k in range(len(other.rows)):
                    total += self.rows[i][k] * other.rows[k][j]
                new_row.append(total)
            result.append(new_row)
        return Matrix(result)

    def __eq__(self, other):
        return self.rows == other.rows

    def __repr__(self):
        return f"Matrix({self.rows})"


# =====================================================================
# PART 2: INHERITANCE
# =====================================================================

# ---- Problem 1: Vehicle, Car, Bicycle --------------------------------
class Vehicle:
    def drive(self):
        return "Driving a vehicle"


class Car(Vehicle):
    def drive(self):
        return "Driving a car"


class Bicycle(Vehicle):
    def drive(self):
        return "Riding a bicycle"


# ---- Problem 2: Person, Student, Employee ----------------------------
class PersonInfo:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def introduce(self):
        return f"Hi, I am {self.name}, {self.age} years old, I live at {self.address}."


class Student(PersonInfo):
    def __init__(self, name, age, address, field_of_study):
        super().__init__(name, age, address)
        self.field_of_study = field_of_study

    def introduce(self):
        return f"{super().introduce()} I study {self.field_of_study}."


class Employee(PersonInfo):
    def __init__(self, name, age, address, company):
        super().__init__(name, age, address)
        self.company = company

    def introduce(self):
        return f"{super().introduce()} I work at {self.company}."


# ---- Problem 3: BankAccount, SavingsAccount --------------------------
class BankAccount:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def transfer(self, destination, amount):
        # False if insufficient balance, True otherwise
        if not self.withdraw(amount):
            return False
        destination.deposit(amount)
        return True


class SavingsAccount(BankAccount):
    def __init__(self, account_number, balance=0, interest_rate=0.0):
        super().__init__(account_number, balance)
        self.interest_rate = interest_rate  # e.g. 0.05 for 5 %

    def add_interest(self):
        self.balance += self.balance * self.interest_rate

    def check_balance(self):
        return self.balance


# =====================================================================
# TESTS (run: python3 oop_exercises.py)
# =====================================================================
if __name__ == "__main__":
    # Operator overloading
    assert Complex(1, 2) + Complex(3, 4) == Complex(4, 6)
    assert Complex(5, 5) - Complex(2, 7) == Complex(3, -2)
    print(Complex(1, 2) + Complex(3, 4), Complex(5, 5) - Complex(2, 7))

    p1, p2 = Person("Ali", 30, "M"), Person("Ayse", 25, "F")
    assert (p1 > p2) is True and (p2 > p1) is False

    assert Vector(1, 2, 3) * Vector(4, 5, 6) == 32

    c1, c2 = Circle(3), Circle(5)
    assert c1 < c2 and c2 > c1 and c1 != c2 and c1 <= c2 and c2 >= c1
    assert Circle(3) == Circle(3) and Circle(3) >= Circle(3) and Circle(3) <= Circle(3)

    a, b = Point2D(3, 4), Point2D(1, 1)  # distances 5 and sqrt(2)
    assert b < a and a > b and a != b and b <= a and a >= b
    assert Point2D(3, 4) == Point2D(5, 0)  # same distance from the origin

    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[5, 6], [7, 8]])
    assert m1 * m2 == Matrix([[19, 22], [43, 50]])
    assert Matrix([[1, 2, 3]]) * Matrix([[1], [2], [3]]) == Matrix([[14]])
    try:
        m1 * Matrix([[1, 2, 3]])
        raise AssertionError("should have raised ValueError")
    except ValueError:
        pass

    # Inheritance
    assert Vehicle().drive() == "Driving a vehicle"
    assert Car().drive() == "Driving a car"
    assert Bicycle().drive() == "Riding a bicycle"

    s = Student("Efe", 20, "Paris", "AI and Data")
    e = Employee("Deniz", 35, "Istanbul", "Acme")
    print(s.introduce())
    print(e.introduce())
    assert isinstance(s, PersonInfo) and isinstance(e, PersonInfo)

    acc1 = BankAccount("A1", 100)
    acc2 = SavingsAccount("S1", 50, 0.1)
    assert acc1.transfer(acc2, 40) is True
    assert acc1.balance == 60 and acc2.balance == 90
    assert acc1.transfer(acc2, 1000) is False
    assert acc1.balance == 60 and acc2.balance == 90
    acc2.add_interest()
    assert math.isclose(acc2.check_balance(), 99.0)

    print("All tests passed.")
