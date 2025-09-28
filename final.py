import uuid
from datetime import datetime, timedelta

class Client:
    def __init__(self, name, email):
        self.client_id = str(uuid.uuid4())[:6]
        self.name = name
        self.email = email

    def __str__(self):
        return f"ID: {self.client_id} | Name: {self.name}"

class Invoice:
    def __init__(self, client_id, project_title, items, due_days=30):
        self.invoice_id = str(uuid.uuid4())[:8]
        self.client_id = client_id
        self.project_title = project_title
        self.items = items
        self.issue_date = datetime.now()
        self.due_date = self.issue_date + timedelta(days=due_days)
        self.total_due = round(sum(item['qty']*item['price'] for item in items), 2)
        self.amount_paid = 0.0
        self.status = "PENDING"

    def record_payment(self, amount):
        self.amount_paid += amount
        if self.amount_paid >= self.total_due:
            self.status = "PAID"
        elif self.amount_paid > 0:
            self.status = "PARTIAL"

    def get_balance(self):
        return round(self.total_due - self.amount_paid, 2)

    def update_status(self):
        if self.status != "PAID" and datetime.now() > self.due_date:
            self.status = "OVERDUE"

    def get_summary(self):
        self.update_status()
        balance = self.get_balance()
        status_text = f"{self.status} (DUE: ${balance:.2f})" if balance >= 0 else f"PAID (CREDIT: ${abs(balance):.2f})"
        return f"INV-{self.invoice_id} | {self.project_title} | Total: ${self.total_due:.2f} | Status: {status_text}"

class FinanceApp:
    def __init__(self):
        self.clients = {}
        self.invoices = []

    def add_client(self):
        name = input("Client Name: ")
        email = input("Client Email: ")
        client = Client(name, email)
        self.clients[client.client_id] = client
        print(f"Client '{name}' added with ID: {client.client_id}")

    def generate_invoice(self):
        if not self.clients:
            print("Add a client first!")
            return
        print("\nClients:")
        for client in self.clients.values():
            print(f"- {client.name}")
        client_name = input("Client Name to bill: ")
        matches = [c for c in self.clients.values() if c.name.lower()==client_name.lower()]
        if not matches:
            print("Client not found.")
            return
        client_id = matches[0].client_id
        project_title = input("Project/Service Name: ")
        items=[]
        while True:
            desc = input("Item Description (or 'done' to stop): ")
            if desc.lower() == "done": break
            qty = int(input("Quantity: "))
            price = float(input("Price per unit: "))
            items.append({'desc': desc, 'qty': qty, 'price': price})
        if items:
            inv = Invoice(client_id, project_title, items)
            self.invoices.append(inv)
            print(f"Invoice created! ID: {inv.invoice_id}, Total: ${inv.total_due:.2f}")
        else:
            print("No items added.")

    def record_payment(self):
        if not self.invoices:
            print("No invoices yet.")
            return
        proj_name = input("Enter Project Name to pay: ")
        matches = [i for i in self.invoices if i.project_title.lower()==proj_name.lower()]
        if not matches:
            print("Invoice not found.")
            return
        inv = matches[0]
        print(f"Balance: ${inv.get_balance():.2f}")
        amt = float(input("Payment Amount: "))
        inv.record_payment(amt)
        print(f"Payment recorded! Status: {inv.status}, Remaining Balance: ${inv.get_balance():.2f}")

    def check_client_balance(self):
        client_name = input("Enter Client Name: ")
        matches = [c for c in self.clients.values() if c.name.lower()==client_name.lower()]
        if not matches:
            print("Client not found.")
            return
        client_id = matches[0].client_id
        total_due = sum(inv.get_balance() for inv in self.invoices if inv.client_id==client_id)
        print(f"Total Outstanding: ${total_due:.2f}")
        for inv in self.invoices:
            if inv.client_id==client_id:
                print(f"- {inv.get_summary()}")

    def run(self):
        while True:
            print("\n1. Add Client\n2. Generate Invoice\n3. Record Payment\n4. Check Client Balance\n5. Exit")
            choice = input("Option: ")
            if choice=='1': self.add_client()
            elif choice=='2': self.generate_invoice()
            elif choice=='3': self.record_payment()
            elif choice=='4': self.check_client_balance()
            elif choice=='5':
                print("Goodbye!")
                break
            else:
                print("Invalid option.")

if __name__=="__main__":
    app = FinanceApp()
    app.run()
