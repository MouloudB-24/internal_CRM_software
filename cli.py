from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from app import create_app, db
from app.models.customer import Customer
from app.models.contract import Contract
from app.models.user import User, UserRole

console = Console()
app = create_app()

def main_menu():
    """Application main menu"""

    while True:
        console.print("\n[bold green]Main menu")
        console.print("1 - Mange users")
        console.print("2 - Manage costumers")
        console.print("3 - Manage contracts")
        console.print("4 - Manage events")
        console.print("5 - Exit")

        choice = Prompt.ask("[bold purple]Enter your choice", choices=["1", "2", "3", "4", "5"])

        if choice == "1":
            user_menu()
        elif choice == "2":
            costumer_menu()
        elif choice == "3":
            contract_menu()
        elif choice == "4":
            event_menu()
        elif choice == "5":
            console.print("[bold red]Good-bye!")
            break

def user_menu():
    """User management menu"""

    while True:
        console.print("\n[bold green]Manage users")
        console.print("1 - Create user")
        console.print("2 - Show users")
        console.print("3 - Back to main menu")

        choice = Prompt.ask("[bold green]Enter your choice", choices=["1", "2", "3"])

        if choice == "1":
            create_user()
        elif choice == "2":
            list_users()
        elif choice == "3":
            break

def create_user():
    """Create a new user"""

    console.print("\n[bold yellow]Create a new user[/bold yellow]")

    username = Prompt.ask("[bold yellow]Name[/bold yellow]")
    email = Prompt.ask("[bold yellow]Email")
    phone = Prompt.ask("[bold yellow]Phone")
    password = Prompt.ask("[bold yellow]Password")
    role = Prompt.ask("[bold yellow]Role", choices=["Sales", "Support", "Management"])

    with app.app_context():
        # Data verification and user creation
        try:
            user = User(username=username, email=email, phone=phone, role=UserRole(role))
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            console.print("[bold green]User successfully created![/bold green]")
        except Exception as e:
            console.print(f"[bold red]User creation error : {str(e)}[/bold red]")

def list_users():
    """Show all users"""

    console.print("\n[bold yellow]Users list")

    with app.app_context():
        users = User.query.all()
        if not users:
            console.print("[bold red]No user found!")
            return

        table = Table(title="Registered users")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Name", style="magenta")
        table.add_column("Email", style="magenta")
        table.add_column("Phone", style="magenta")
        table.add_column("Role", style="magenta")

        for user in users:
            table.add_row(
                str(user.id),
                user.username,
                user.email,
                user.phone,
                user.role.value
            )

        console.print(table)




def costumer_menu():
    """Costumers management menu"""

    while True:
        console.print("\n[bold green]Manage costumers[/bold green]")
        console.print("[bold yellow]1 - Create costumer")
        console.print("[bold yellow]2 - Show all costumers")
        console.print("[bold yellow]3 - Back to main menu")

        choice = Prompt.ask("[bold green]Enter your choice[/bold green]", choices=["1", "2", "3"])

        if choice == "1":
            create_costumer()
        elif choice == "2":
            list_costumers()
        elif choice == "3":
            break


def create_costumer():
    """Create a new costumer"""

    console.print("\n[bold yellow]Create a new costumer")

    full_name = Prompt.ask("[bold yellow]Full name")
    email = Prompt.ask("[bold yellow]Email")
    phone = Prompt.ask("[bold yellow]Phone")
    company_name = Prompt.ask("[bold yellow]Company name", default="N/A")
    sales_contact_id = Prompt.ask("[bold yellow]Associated sales contact ID")

    with app.app_context():
        try:
            # Create a new costumer
            costumer = Customer(
                full_name=full_name,
                email=email,
                phone=phone,
                company_name=company_name,
                sales_contact_id=int(sales_contact_id) if sales_contact_id.isdigit() else None
            )
            db.session.add(costumer)
            db.session.commit()

            console.print("[bold green]Costumer successfully created!")
        except Exception as e:
            console.print(f"[bold red]Costumer creation error: {str(e)}[/bold red]")


def list_costumers():
    """Show all costumers"""
    console.print("\n[bold yellow]Costumers list")

    with app.app_context():
        clients = Customer.query.all()

        if not clients:
            console.print("[bold red]No costumer found!")
            return

        # Create a Rich table to display customers
        table = Table(title="Registered costumers")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Full name", style="magenta")
        table.add_column("Email", style="magenta")
        table.add_column("Phone", style="magenta")
        table.add_column("Company", style="magenta")
        table.add_column("Sales contact", style="magenta")

        for client in clients:
            table.add_row(
                str(client.id),
                client.full_name,
                client.email,
                client.phone,
                client.company_name if client.company_name else "N/A",
                str(client.sales_contact_id) if client.sales_contact_id else "None"
            )

        console.print(table)


def contract_menu():
    """Manage contracts"""
    while True:
        console.print("\n[bold cyan]Manage contracts")
        console.print("1 - Create contract")
        console.print("2 - Show contracts")
        console.print("3. back to main menu")

        choice = Prompt.ask("[bold green]Enter your choice", choices=["1", "2", "3"])

        if choice == "1":
            create_contract()
        elif choice == "2":
            list_contracts()
        elif choice == "3":
            break

def create_contract():
    """Create a new contract"""

    console.print("\n[bold yellow]Create a new contract")

    customer_id = Prompt.ask("[bold yellow]Associated costumer ID")
    sales_contact_id = Prompt.ask("[bold yellow]Associated contact sales ID")
    total_amount = Prompt.ask("[bold yellow]Total contract amount")
    remaining_amount = Prompt.ask("[bold yellow]Remaining amount")
    status = Prompt.ask("[bold yellow]Contract status", choices=["Draft", "Pending", "Signed", "Completed"])

    with app.app_context():
        try:
            contract = Contract(
                customer_id=int(customer_id),
                sales_contact_id=int(sales_contact_id),
                total_amount=float(total_amount),
                remaining_amount=float(remaining_amount),
                status=status
            )
            db.session.add(contract)
            db.session.commit()
            console.print("[bold green]Contract successfully created![/bold green]")
        except Exception as e:
            console.print(f"[bold red]Creation contract error: {str(e)}[/bold red]")


def list_contracts():
    """Show contracts"""
    console.print("\n[bold yellow]Contracts list")

    with app.app_context():
        contracts = Contract.query.all()

        if not contracts:
            console.print("[bold red]No contract found!")
            return

        table = Table(title="Registered contracts")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Costumer", style="magenta")
        table.add_column("Sales contact", style="magenta")
        table.add_column("Total amount", style="magenta")
        table.add_column("Remaining amount", style="magenta")
        table.add_column("Status", style="magenta")

        for contract in contracts:
            table.add_row(
                str(contract.id),
                str(contract.customer_id),
                str(contract.sales_contact_id),
                f"{contract.total_amount:.2f}",
                f"{contract.remaining_amount:.2f}",
                str(contract.status.value)
            )

        console.print(table)


def event_menu():
    """Event management menu"""
    while True:
        console.print("\n[bold cyan]Manage events")
        console.print("1 - Create event")
        console.print("2 - Show events")
        console.print("3 - Back to main menu")

        choice = Prompt.ask("[bold green]Enter your choice", choices=["1", "2", "3"])

        if choice == "1":
            create_event()
        elif choice == "2":
            list_events()
        elif choice == "3":
            break


from app.models.event import Event

def create_event():
    """Create a new event"""

    console.print("\n[bold yellow]Create a new event")

    contract_id = Prompt.ask("[bold yellow]Associated contrast ID")
    support_contact_id = Prompt.ask("[bold yellow]Support contact ID", default="None")
    name = Prompt.ask("[bold yellow]Event name")
    status = Prompt.ask("[bold yellow]Event status", choices=["Planned", "In_progress", "Completed"])
    start_date = Prompt.ask("[bold yellow]Start date (YYYY-MM-DD)")
    end_date = Prompt.ask("[bold yellow]End date (YYYY-MM-DD)")
    location = Prompt.ask("[bold yellow]Event location")
    attendees = Prompt.ask("[bold yellow]Number of attendees", default="0")
    notes = Prompt.ask("[bold yellow]Notes (optional)", default="")

    with app.app_context():
        try:
            event = Event(
                contract_id=int(contract_id),
                support_contact_id=int(support_contact_id) if support_contact_id != "None" else None,
                name=name,
                status=status,
                start_date=start_date,
                end_date=end_date,
                location=location,
                attendees=int(attendees),
                notes=notes
            )
            db.session.add(event)
            db.session.commit()
            console.print("[bold green]Event successfully created!")
        except Exception as e:
            console.print(f"[bold red]Event creation error: {str(e)}[/bold red]")


def list_events():
    """Show events"""

    console.print("\n[bold yellow]Event list")

    with app.app_context():
        events = Event.query.all()

        if not events:
            console.print("[bold red]No event found!")
            return

        table = Table(title="Registered events")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Contract", style="magenta")
        table.add_column("Contact support", style="magenta")
        table.add_column("Name", style="magenta")
        table.add_column("Status", style="magenta")
        table.add_column("Start", style="magenta")
        table.add_column("End", style="magenta")
        table.add_column("Location", style="magenta")
        table.add_column("Attendees", style="magenta")

        for event in events:
            table.add_row(
                str(event.id),
                str(event.contract_id),
                str(event.support_contact_id) if event.support_contact_id else "None",
                event.name,
                str(event.status.value),
                event.start_date.strftime("%Y-%m-%d"),
                event.end_date.strftime("%Y-%m-%d"),
                event.location,
                str(event.attendees)
            )

        console.print(table)



if __name__ == '__main__':
    main_menu()