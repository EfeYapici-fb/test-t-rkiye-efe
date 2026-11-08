"""Exo 1 - Hospital Management System (implementation of the UML class diagram)."""
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum


class ProblemStatus(Enum):
    PENDING = "pending"
    IN_REVIEW = "in-review"
    RESOLVED = "resolved"


# ---------------- Users (abstract superclass) ----------------
class User(ABC):
    def __init__(self, user_id, name, password):
        self._id = user_id
        self._name = name
        self._password = password
        self._logged_in = False

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def login(self, password):
        self._logged_in = password == self._password
        return self._logged_in

    def logout(self):
        self._logged_in = False

    @abstractmethod
    def role(self):
        ...


class Patient(User):
    def __init__(self, user_id, name, password):
        super().__init__(user_id, name, password)
        self.problems = []          # 1 patient -> 0..* HealthProblem

    def role(self):
        return "patient"

    def submit_problem(self, description):
        problem = HealthProblem(len(self.problems) + 1, description, self)
        self.problems.append(problem)
        return problem

    def pay(self, problem, payment):
        payment.process()
        problem.payment = payment
        return payment


class Doctor(User):
    def __init__(self, user_id, name, password, specialty):
        super().__init__(user_id, name, password)
        self.specialty = specialty

    def role(self):
        return "doctor"

    def write_prescription(self, problem, text):
        prescription = Prescription(text, problem)
        problem.prescription = prescription
        problem.status = ProblemStatus.RESOLVED
        return prescription


class Organizer(User):
    """Coordinator and administrator of the platform."""

    def __init__(self, user_id, name, password):
        super().__init__(user_id, name, password)
        self.members = {}           # database of members (id -> user)
        self.payments_forwarded = []

    def role(self):
        return "organizer"

    # ---- administrator part ----
    def register_member(self, member_class, name, *extra):
        new_id = f"M{len(self.members) + 1:03d}"
        password = f"pw-{new_id}"           # issued by the organizer
        member = member_class(new_id, name, password, *extra)
        self.members[new_id] = member
        return member

    # ---- workflow part ----
    def read_problem(self, problem):
        problem.status = ProblemStatus.IN_REVIEW
        return problem

    def consult(self, doctor, problem):
        problem.doctor = doctor
        return doctor.write_prescription(problem, f"Treatment for: {problem.description}")

    def send_prescription(self, patient, prescription):
        return f"Prescription sent to {patient.name}: {prescription.text}"

    def forward_payment(self, doctor, payment):
        self.payments_forwarded.append((doctor.name, payment.amount))
        return True


# ---------------- Core classes ----------------
class HealthProblem:
    def __init__(self, problem_id, description, patient):
        self.id = problem_id
        self.description = description
        self.patient = patient
        self.status = ProblemStatus.PENDING
        self.created_at = datetime.now()
        self.doctor = None
        self.prescription = None     # 0..1
        self.payment = None


class Prescription:
    def __init__(self, text, problem):
        self.text = text
        self.problem = problem
        self.created_at = datetime.now()   # timestamp; kept in history


# ---------------- Payment (strategy via polymorphism) ----------------
class Payment(ABC):
    def __init__(self, amount):
        self.amount = amount
        self.paid = False
        self.date = datetime.now()

    @abstractmethod
    def process(self):
        ...


class CheckPayment(Payment):
    def __init__(self, amount, check_number):
        super().__init__(amount)
        self.check_number = check_number

    def process(self):
        self.paid = True
        return f"Check {self.check_number} cashed: {self.amount}"


class CashPayment(Payment):
    def process(self):
        self.paid = True
        return f"Cash received: {self.amount}"


class CreditCardPayment(Payment):
    def __init__(self, amount, card_number):
        super().__init__(amount)
        self.card_number = card_number

    def process(self):
        self.paid = True
        return f"Card ****{self.card_number[-4:]} charged: {self.amount}"


if __name__ == "__main__":
    # Scenario: patient submits a problem, receives a prescription, pays.
    org = Organizer("A001", "Admin", "root")
    patient = org.register_member(Patient, "Efe")
    doctor = org.register_member(Doctor, "Dr. House", "diagnostics")

    problem = patient.submit_problem("Headache for three days")
    assert problem.status is ProblemStatus.PENDING

    org.read_problem(problem)
    assert problem.status is ProblemStatus.IN_REVIEW

    prescription = org.consult(doctor, problem)
    assert problem.status is ProblemStatus.RESOLVED
    print(org.send_prescription(patient, prescription))

    payment = CreditCardPayment(50, "1234567812345678")
    patient.pay(problem, payment)
    assert payment.paid
    org.forward_payment(doctor, payment)
    assert org.payments_forwarded == [("Dr. House", 50)]

    # past prescriptions of a patient
    history = [p.prescription for p in patient.problems if p.prescription]
    assert len(history) == 1
    print("Hospital: all checks passed.")
