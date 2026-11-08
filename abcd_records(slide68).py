"""Exo 2 - ABCD Records (implementation of the UML class diagram)."""
from abc import ABC, abstractmethod
from datetime import date


# ---------------- Items ----------------
class Item(ABC):
    def __init__(self, item_id, title, price, stock):
        self.id = item_id
        self.title = title
        self.price = price
        self.stock = stock

    def is_available(self, quantity=1):
        return self.stock >= quantity


class CD(Item):
    pass


class Tape(Item):
    pass


# ---------------- Members ----------------
class Member(ABC):
    def __init__(self, member_id, name):
        self.id = member_id
        self.name = name
        self.orders = []

    @abstractmethod
    def discount(self):
        ...

    @abstractmethod
    def can_order_unavailable(self):
        ...

    def place_order(self, lines):
        order = Order(self, lines)
        self.orders.append(order)
        return order


class RoyalMember(Member):
    def discount(self):
        return 0.10            # discounts + priority

    def can_order_unavailable(self):
        return True


class RegularMember(Member):
    def discount(self):
        return 0.0

    def can_order_unavailable(self):
        return False


class NonMember:
    def __init__(self, name):
        self.name = name


class MembershipApplication:
    def __init__(self, applicant):
        self.applicant = applicant


# ---------------- Orders ----------------
class OrderLine:
    def __init__(self, item, quantity):
        self.item = item
        self.quantity = quantity
        self.unavailable = False

    def total(self):
        return self.item.price * self.quantity


class Order:
    def __init__(self, member, lines):
        self.member = member
        self.lines = lines       # Order 1 ◆— 1..* OrderLine
        self.date = date.today()
        self.status = "NEW"
        self.invoice = None
        self.shipping_list = None


class Invoice:
    def __init__(self, order, amount):
        self.order = order
        self.amount = amount
        self.paid = False


class ShippingList:
    def __init__(self, order, lines):
        self.order = order
        self.lines = lines


# ---------------- Payments ----------------
class Payment(ABC):
    def __init__(self, invoice):
        self.invoice = invoice

    @abstractmethod
    def process(self):
        ...


class CashPayment(Payment):
    def process(self):
        self.invoice.paid = True
        return "cash"


class CheckPayment(Payment):
    def __init__(self, invoice, check_number):
        super().__init__(invoice)
        self.check_number = check_number

    def process(self):
        self.invoice.paid = True
        return f"check {self.check_number}"


class BankDraftPayment(Payment):
    def __init__(self, invoice, bank):
        super().__init__(invoice)
        self.bank = bank

    def process(self):
        self.invoice.paid = True
        return f"bank draft {self.bank}"


# ---------------- Employees ----------------
class OrderProcessingClerk:
    def __init__(self):
        self.daily_records = []          # all orders saved to the daily records file

    def handle(self, customer, lines=None):
        """Only members can order. Non-members receive an application form."""
        if isinstance(customer, NonMember):
            return MembershipApplication(customer)
        return self.process_order(customer.place_order(lines))

    def process_order(self, order):
        member = order.member
        ready = []
        for line in order.lines:
            if line.item.is_available(line.quantity):
                ready.append(line)
            elif member.can_order_unavailable():     # Royal only
                line.unavailable = True               # re-ordered from the supplier
            else:
                order.status = "REJECTED"
                self.daily_records.append(order)
                return order
        total = sum(l.total() for l in order.lines)
        order.invoice = Invoice(order, round(total * (1 - member.discount()), 2))
        order.shipping_list = ShippingList(order, ready)
        for line in ready:
            line.item.stock -= line.quantity
        order.status = "PROCESSED"
        self.daily_records.append(order)
        return order


class CollectionDepartmentClerk:
    def handle_payment(self, payment):
        return payment.process()


if __name__ == "__main__":
    # Scenario: Royal member orders 2 CDs (one unavailable) and pays by check.
    cd1 = CD(1, "Abbey Road", 20.0, stock=5)
    cd2 = CD(2, "Thriller", 15.0, stock=0)          # unavailable
    royal = RoyalMember("R1", "Efe")
    clerk = OrderProcessingClerk()
    collector = CollectionDepartmentClerk()

    order = clerk.handle(royal, [OrderLine(cd1, 1), OrderLine(cd2, 1)])
    assert order.status == "PROCESSED"
    assert order.lines[1].unavailable and not order.lines[0].unavailable
    assert order.invoice.amount == 31.5                      # (20 + 15) * 0.9
    assert len(order.shipping_list.lines) == 1               # only the available CD ships
    collector.handle_payment(CheckPayment(order.invoice, "CHK-42"))
    assert order.invoice.paid

    # Regular member cannot order unavailable items
    regular = RegularMember("G1", "Ali")
    refused = clerk.handle(regular, [OrderLine(cd2, 1)])
    assert refused.status == "REJECTED"

    # Non-member receives a membership application
    assert isinstance(clerk.handle(NonMember("Zoe")), MembershipApplication)
    assert len(clerk.daily_records) == 2
    print("ABCD: all checks passed.")
