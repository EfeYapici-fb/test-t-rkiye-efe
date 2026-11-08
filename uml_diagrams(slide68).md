# UML exercise: reference diagrams (Mermaid, rendered by GitHub)

## Exo 1: Hospital Management System

### Class diagram (Tasks 1, 2, 3)
```mermaid
classDiagram
    class User {
        <<abstract>>
        #id: int
        #name: str
        #password: str
        +login()
        +logout()
    }
    class Patient {
        +submitProblem()
        +pay()
    }
    class Doctor {
        -specialty: str
        +writePrescription()
    }
    class Organizer {
        +registerMember()
        +readProblem()
        +consult()
        +sendPrescription()
        +forwardPayment()
    }
    class HealthProblem {
        -id: int
        -description: str
        -createdAt: datetime
        -status: ProblemStatus
    }
    class Prescription {
        -text: str
        -createdAt: datetime
    }
    class Payment {
        <<abstract>>
        -amount: float
        -date: datetime
        +process()
    }
    class CheckPayment {
        -checkNumber: str
        +process()
    }
    class CashPayment {
        +process()
    }
    class CreditCardPayment {
        -cardNumber: str
        +process()
    }
    class ProblemStatus {
        <<enumeration>>
        PENDING
        IN_REVIEW
        RESOLVED
    }
    User <|-- Patient
    User <|-- Doctor
    User <|-- Organizer
    Payment <|-- CheckPayment
    Payment <|-- CashPayment
    Payment <|-- CreditCardPayment
    Patient "1" --> "0..*" HealthProblem : submits
    Organizer "1" --> "0..*" HealthProblem : reads
    HealthProblem "0..*" --> "0..1" Doctor : consulted by
    HealthProblem "1" --> "0..1" Prescription : has
    Patient "1" --> "0..*" Payment : makes
    Payment "0..1" --> "1" HealthProblem : settles
    Organizer "1" --> "0..*" Payment : forwards to doctor
```

### Sequence diagram 1: submit a problem, receive a prescription, pay (Task 2)
```mermaid
sequenceDiagram
    actor Patient
    participant Organizer
    participant Doctor
    participant Database
    Patient->>Organizer: Submit health problem
    Organizer->>Database: Save problem (status: PENDING)
    Database-->>Organizer: Saved
    Organizer->>Organizer: Read problem (status: IN_REVIEW)
    Organizer->>Doctor: Consult doctor
    Doctor->>Doctor: Write prescription
    Doctor-->>Organizer: Prescription
    Organizer->>Database: Save prescription (status: RESOLVED)
    Database-->>Organizer: Saved
    Organizer-->>Patient: Send prescription
    Patient->>Organizer: Pay (check, cash or credit card)
    Organizer->>Database: Save payment
    Database-->>Organizer: Saved
    Organizer-->>Patient: Payment confirmation
```

### Sequence diagram 2: patient registration (Task 3)
```mermaid
sequenceDiagram
    actor Patient
    participant Organizer
    participant Database
    Patient->>Organizer: Request registration
    Organizer->>Organizer: Verify request
    Organizer->>Organizer: Generate member ID and password
    Organizer->>Database: Save new member
    Database-->>Organizer: Saved
    Organizer-->>Patient: Send ID and password
```

### Sequence diagram 3: consultation flow (Task 3)
```mermaid
sequenceDiagram
    actor Patient
    participant Organizer
    participant Doctor
    participant Database
    Patient->>Organizer: Post health problem
    Organizer->>Database: Save problem (status: PENDING)
    Database-->>Organizer: Saved
    Organizer->>Organizer: Read problem details
    Organizer->>Database: Update status to IN_REVIEW
    Database-->>Organizer: Updated
    Organizer->>Doctor: Send problem
    Doctor->>Doctor: Examine problem
    Doctor-->>Organizer: Prescription
    Organizer->>Database: Save prescription, status RESOLVED
    Database-->>Organizer: Saved
    Organizer-->>Patient: Deliver prescription
```

### Sequence diagram 4: payment processing (Task 3)
```mermaid
sequenceDiagram
    actor Patient
    participant Organizer
    participant Doctor
    participant Database
    Patient->>Organizer: Pay (check, cash or credit card)
    Organizer->>Organizer: Process payment
    Organizer->>Database: Save payment
    Database-->>Organizer: Saved
    Organizer-->>Patient: Payment receipt
    Organizer->>Doctor: Forward payment
    Doctor-->>Organizer: Payment received
```

Questions to consider (short answers):
- **Several doctors per patient:** a patient has many problems, each problem is consulted by one doctor, so a patient can meet many doctors (Patient 1 to 0..* HealthProblem, HealthProblem 0..* to 0..1 Doctor).
- **Reusable prescriptions:** keep Prescription as its own class linked to the patient history, so a past prescription can be referenced by a new problem.
- **Design pattern for payments:** Strategy (Payment with Check, Cash and CreditCard subclasses sharing `process()`).
- **Data integrity:** save the payment and the status change in one database transaction (all or nothing), and only forward the payment to the doctor after it is saved.

---

## Exo 2: ABCD Records

### Use case diagram (Level 1 and 2)
```mermaid
flowchart LR
    NM(["Non-Member"])
    M(["Member"])
    OPC(["Order Processing Clerk"])
    CDC(["Collection Department Clerk"])
    subgraph SYS["ABCD Records System"]
        PO([Place Order])
        VM([Verify Membership])
        PRO([Process Order])
        VA([Verify Item Availability])
        AD([Apply Discount])
        SAVE([Save Order in Daily Records])
        SMA([Send Membership Application])
        OU([Order Unavailable Items])
        MP([Make Payment])
        PI([Print Invoice])
        PSL([Print Shipping List])
    end
    M --- PO
    NM --- PO
    OPC --- PRO
    CDC --- MP
    PO -. "include" .-> VM
    PRO -. "include" .-> VA
    PRO -. "include" .-> SAVE
    PRO -. "include" .-> PI
    PRO -. "include" .-> PSL
    SMA -. "extend [not a member]" .-> VM
    AD -. "extend [Royal member]" .-> PRO
    OU -. "extend [item unavailable, Royal member]" .-> VA
    MP -. "include" .-> PI
```

### Class diagram (Level 1 and 2)
```mermaid
classDiagram
    class Member {
        <<abstract>>
        #id: int
        #name: str
        #address: str
        +placeOrder()
        +makePayment()
    }
    class RoyalMember {
        -discountRate: float
        +orderUnavailableItem()
    }
    class RegularMember
    class NonMember {
        -name: str
        +requestMembership()
    }
    class MembershipApplication {
        -date: date
    }
    class Order {
        -id: int
        -date: date
        -status: str
    }
    class OrderLine {
        -quantity: int
    }
    class Item {
        <<abstract>>
        -id: int
        -title: str
        -price: float
        -stock: int
    }
    class CD
    class Tape
    class Invoice {
        -amount: float
        -paid: bool
    }
    class ShippingList {
        -date: date
    }
    class Payment {
        <<abstract>>
        -amount: float
        -date: date
        +process()
    }
    class CashPayment
    class CheckPayment {
        -checkNumber: str
    }
    class BankDraftPayment {
        -bank: str
    }
    class OrderProcessingClerk {
        -id: int
        -name: str
        +verifyMembership()
        +processOrder()
        +printInvoice()
    }
    class CollectionDepartmentClerk {
        -id: int
        -name: str
        +handlePayment()
    }
    Member <|-- RoyalMember
    Member <|-- RegularMember
    Item <|-- CD
    Item <|-- Tape
    Payment <|-- CashPayment
    Payment <|-- CheckPayment
    Payment <|-- BankDraftPayment
    Member "1" --> "0..*" Order : places
    Order "1" *-- "1..*" OrderLine : contains
    OrderLine "0..*" --> "1" Item : refers to
    Order "1" --> "0..1" Invoice : generates
    Order "1" --> "0..1" ShippingList : generates
    Invoice "1" --> "0..*" Payment : paid by
    OrderProcessingClerk "1" --> "0..*" Order : processes
    CollectionDepartmentClerk "1" --> "0..*" Payment : handles
    NonMember "1" --> "0..*" MembershipApplication : receives
```
Scenario (Royal member orders 2 CDs, one unavailable, pays by check): a `RoyalMember` has one `Order` with two `OrderLine` objects pointing to two `CD` objects; the unavailable CD is re-ordered (royal privilege); one `Invoice` is generated (with the royal discount) and paid with one `CheckPayment`.

### Sequence diagram 1: complete order processing flow (Level 3)
```mermaid
sequenceDiagram
    actor Member
    participant Clerk as Order Processing Clerk
    participant Collector as Collection Dept Clerk
    participant Database
    Member->>Clerk: Place order (2 CDs)
    Clerk->>Database: Check membership
    Database-->>Clerk: Valid member
    Clerk->>Database: Check item availability
    Database-->>Clerk: CD1 available, CD2 unavailable
    Clerk->>Clerk: Apply royal discount
    Clerk->>Database: Order unavailable item (CD2)
    Database-->>Clerk: Ordered
    Clerk->>Database: Save order in daily records
    Database-->>Clerk: Saved
    Clerk->>Clerk: Print invoice and shipping list
    Clerk-->>Member: Send invoice
    Member->>Collector: Pay by check
    Collector->>Database: Save payment
    Database-->>Collector: Saved
    Collector-->>Member: Payment confirmation
```

### Sequence diagram 2: membership verification (success and failure)
```mermaid
sequenceDiagram
    actor Customer
    participant Clerk as Order Processing Clerk
    participant Database
    Customer->>Clerk: Place order
    Clerk->>Database: Verify membership
    Database-->>Clerk: Result
    alt member found (success)
        Clerk->>Database: Save order in daily records
        Database-->>Clerk: Saved
        Clerk-->>Customer: Order accepted
    else not a member (failure)
        Clerk-->>Customer: Send membership application form
    end
```

### Sequence diagram 3: payment processing (all types)
```mermaid
sequenceDiagram
    actor Member
    participant Collector as Collection Dept Clerk
    participant Database
    Member->>Collector: Pay invoice (cash, check or bank draft)
    alt cash
        Collector->>Collector: Receive cash
    else check
        Collector->>Collector: Verify and deposit check
    else bank draft
        Collector->>Collector: Verify bank draft
    end
    Collector->>Database: Save payment, invoice paid
    Database-->>Collector: Saved
    Collector-->>Member: Payment receipt
```

### Sequence diagram 4: item reordering for Royal members
```mermaid
sequenceDiagram
    actor Member
    participant Clerk as Order Processing Clerk
    participant Database
    Member->>Clerk: Order item
    Clerk->>Database: Check item availability
    Database-->>Clerk: Unavailable
    opt Royal member
        Clerk->>Database: Order item from supplier
        Database-->>Clerk: Reorder saved
        Clerk-->>Member: Item will be shipped when available
    end
    opt Regular member
        Clerk-->>Member: Item cannot be ordered
    end
```
