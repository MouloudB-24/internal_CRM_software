from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from werkzeug.security import check_password_hash

from app import create_app, db
from app.models.contract import Contract, ContractStatus
from app.models.customer import Customer
from app.models.event import Event
from app.models.user import User, UserRole

console = Console()
app = create_app()


# -------------------------------------- LOGIN and PERMISSIONS ---------------------------------------------
# Variable for logged-in user
current_user = None

def login_user():
    """User login"""

    global current_user
    console.print("\n[bold cyan]User login")

    email = Prompt.ask("[bold yellow]Email")
    password = Prompt.ask("[bold yellow]Password", password=True)

    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            current_user = user
            console.print(f"[bold green]Successfully connection! Welcome, {user.username}.[/bold green]")
        else:
            console.print("[bold red]Invalid credentials. Please again!")
            login_user()

def has_permission(required_role):
    """Check whether the logged-in user has the required role."""

    if current_user.role == UserRole.MANAGEMENT:
        return True
    return current_user.role == required_role



# -------------------------------------- Main MENU ----------------------------------------------
def main_menu():
    """Application main menu"""

    while True:
        console.print("\n[bold green]Main menu")
        console.print("1 - Mange users")
        console.print("2 - Manage costumers")
        console.print("3 - Manage contracts")
        console.print("4 - Manage events")
        console.print("q - Exit")

        choice = Prompt.ask("[bold purple]Enter your choice", choices=["1", "2", "3", "4", "q"])

        if choice == "1":
            user_menu()
        elif choice == "2":
            costumer_menu()
        elif choice == "3":
            contract_menu()
        elif choice == "4":
            event_menu()
        elif choice == "q":
            console.print("[bold red]Good-bye!")
            break



# -------------------------------------- Manager USERS ----------------------------------------------
def user_menu():
    """User management menu"""

    while True:
        console.print("\n[bold green]Manage users")
        console.print("1 - Create user")
        console.print("2 - Show users")
        console.print("q - Back to main menu")

        choice = Prompt.ask("[bold green]Enter your choice", choices=["1", "2", "q"])

        if choice == "1":
            create_user()
        elif choice == "2":
            list_users()
        elif choice == "q":
            break

def create_user():
    """Create a new user"""

    if not has_permission(UserRole.MANAGEMENT):
        console.print("[bold red]Permission denied : Only managers can create users.")
        return

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



# -------------------------------------- Manager COSTUMERS ----------------------------------------------
def costumer_menu():
    """Costumers management menu"""

    while True:
        console.print("\n[bold green]Manage costumers[/bold green]")
        console.print("[bold yellow]1 - Create costumer")
        console.print("[bold yellow]2 - Show all costumers")
        console.print("[bold yellow]3 - Update costumer")
        console.print("[bold yellow]4 - Delete costumer")
        console.print("[bold yellow]q - Back to main menu")

        choice = Prompt.ask("[bold green]Enter your choice[/bold green]", choices=["1", "2", "3", "4", "q"])

        if choice == "1":
            create_costumer()
        elif choice == "2":
            list_costumers()
        elif choice == "3":
            update_costumer()
        elif choice == "4":
            delete_customer()
        elif choice == "q":
            break


def create_costumer():
    """Create a new costumer"""

    if not has_permission(UserRole.SALES):
        console.print("[bold red]Permission denied : only sales and managers can create costumers.")
        return

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

def update_costumer():
    """Update customer"""

    if not has_permission(UserRole.SALES):
        console.print("[bold red]Permission denied : only sales and managers can create costumers.")
        return

    console.print("\n[bold yellow]Costumer update")

    customer_id = Prompt.ask("[bold yellow]Customer ID to be updated")

    with app.app_context():
        customer = db.session.get(Customer, customer_id)
        if not customer:
            console.print("[bold red]Costumer not found!")
            return

        # Request new values
        full_name = Prompt.ask("[bold yellow]Full name[/bold yellow]", default=customer.full_name)
        email = Prompt.ask("[bold yellow]Email", default=customer.email)
        phone = Prompt.ask("[bold yellow]Phone", default=customer.phone)
        company_name = Prompt.ask("[bold yellow]Company name", default=customer.company_name)

        try:
            customer.full_name = full_name
            customer.email = email
            customer.phone = phone
            customer.company_name = company_name
            db.session.commit()
            console.print("[bold green]Customer successfully updated!")
        except Exception as e:
            console.print(f"[bold red]Updated error: {str(e)}[/bold red]")


def delete_customer():
    """Delete costumer"""

    if not has_permission(UserRole.MANAGEMENT):
        console.print("[bold red]Permission denied : Only managers can create users.")
        return

    console.print("\n[bold yellow]Deleting a constumer")

    customer_id = Prompt.ask("[bold yellow]Costumer ID to be deleted")

    with app.app_context():
        customer = db.session.get(Customer, customer_id)
        if not customer:
            console.print("[bold red]Costumer not found!")
            return

        try:
            db.session.delete(customer)
            db.session.commit()
            console.print("[bold green]Costumer successfully deleted")
        except Exception as e:
            console.print(f"[bold red]Deleted error: {str(e)}[/bold red]")



# -------------------------------------- Manager CONTRACTS ----------------------------------------------
def contract_menu():
    """Manage contracts"""
    while True:
        console.print("\n[bold cyan]Manage contracts")
        console.print("1 - Create contract")
        console.print("2 - Show contracts")
        console.print("3 - Update contract")
        console.print("4 - Delete contract")
        console.print("q. back to main menu")

        choice = Prompt.ask("[bold green]Enter your choice", choices=["1", "2", "3", "4", "q"])

        if choice == "1":
            create_contract()
        elif choice == "2":
            list_contracts()
        elif choice == "3":
            update_contract()
        elif choice == "4":
            delete_contract()
        elif choice == "q":
            break

def create_contract():
    """Create a new contract"""

    if not has_permission(UserRole.SALES):
        console.print("[bold red]Permission denied : only sales and managers can create contracts.")
        return


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

def update_contract():
    """Update contract"""

    if not has_permission(UserRole.SALES):
        console.print("[bold red]Permission denied : only sales and managers can update contracts.")
        return

    console.print("\n[bold yellow]Updating a contract")

    contract_id = Prompt.ask("[bold yellow]ID of the contract to update")

    with app.app_context():
        contract = db.session.get(Contract, contract_id)
        if not contract:
            console.print("[bold red]Contract not found!")
            return

        # Prompt for new values (leave blank to keep current values)
        customer_id = Prompt.ask("[bold yellow]Customer ID", default=str(contract.customer_id))
        sales_contact_id = Prompt.ask("[bold yellow]Sales contact ID", default=str(contract.sales_contact_id))
        total_amount = Prompt.ask("[bold yellow]Total amount", default=str(contract.total_amount))
        remaining_amount = Prompt.ask("[bold yellow]Remaining amount", default=str(contract.remaining_amount))
        status = Prompt.ask("[bold yellow]Status (Draft, Pending, Signed, Completed)", default=contract.status)

        try:
            # Update the contract
            contract.customer_id = int(customer_id)
            contract.sales_contact_id = int(sales_contact_id)
            contract.total_amount = float(total_amount)
            contract.remaining_amount = float(remaining_amount)
            contract.status = status
            db.session.commit()
            console.print("[bold green]Contract updated successfully!")
        except Exception as e:
            console.print(f"[bold red]Error updating the contract: {str(e)}[/bold red]")


def delete_contract():
    """Delete contract"""

    if not has_permission(UserRole.MANAGEMENT):
        console.print("[bold red]Permission denied : only managers can delete contracts.")
        return

    console.print("\n[bold yellow]Deleting a contract")

    contract_id = Prompt.ask("[bold yellow]ID of the contract to delete")

    with app.app_context():
        contract = db.session.get(Contract, contract_id)
        if not contract:
            console.print("[bold red]Contract not found!")
            return

        try:
            # Delete the contract
            db.session.delete(contract)
            db.session.commit()
            console.print("[bold green]Contract deleted successfully!")
        except Exception as e:
            console.print(f"[bold red]Error deleting the contract: {str(e)}[/bold red]")



# -------------------------------------- Manager EVENTS ----------------------------------------------
def event_menu():
    """Event management menu"""
    while True:
        console.print("\n[bold cyan]Manage events")
        console.print("1 - Create event")
        console.print("2 - Show events")
        console.print("3 - Update event")
        console.print("4 - Delete event")
        console.print("q - Back to main menu")

        choice = Prompt.ask("[bold green]Enter your choice", choices=["1", "2", "3", "4", "q"])

        if choice == "1":
            create_event()
        elif choice == "2":
            list_events()
        elif choice == "3":
            update_event()
        elif choice == "4":
            delete_event()
        elif choice == "q":
            break


def create_event():
    """Create a new event"""

    if not has_permission(UserRole.SUPPORT):
        console.print("[bold red]Permission denied : only supports and managers can create events.")
        return

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

def update_event():
    """Update event"""

    if not has_permission(UserRole.SUPPORT):
        console.print("[bold red]Permission denied : only supports and managers can update events.")
        return

    console.print("\n[bold yellow]Updating an event")

    event_id = Prompt.ask("[bold yellow]ID of the event to update")

    with app.app_context():
        event = db.session.get(Event, event_id)
        if not event:
            console.print("[bold red]Event not found!")
            return

        # Prompt for new values
        contract_id = Prompt.ask("[bold yellow]Contract ID", default=str(event.contract_id))
        support_contact_id = Prompt.ask("[bold yellow]Support Contact ID", default=str(event.support_contact_id) if event.support_contact_id else "None")
        name = Prompt.ask("[bold yellow]Event Name", default=event.name)
        status = Prompt.ask("[bold yellow]Status (Planned, In_progress, Completed)", default=event.status)
        start_date = Prompt.ask("[bold yellow]Start Date (YYYY-MM-DD)", default=event.start_date.strftime("%Y-%m-%d"))
        end_date = Prompt.ask("[bold yellow]End Date (YYYY-MM-DD)", default=event.end_date.strftime("%Y-%m-%d"))
        location = Prompt.ask("[bold yellow]Location", default=event.location)
        attendees = Prompt.ask("[bold yellow]Number of Attendees", default=str(event.attendees))
        notes = Prompt.ask("[bold yellow]Notes", default=event.notes if event.notes else "")

        try:
            # Update the event
            event.contract_id = int(contract_id)
            event.support_contact_id = int(support_contact_id) if support_contact_id.lower() != "none" else None
            event.name = name
            event.status = status
            event.start_date = start_date
            event.end_date = end_date
            event.location = location
            event.attendees = int(attendees)
            event.notes = notes
            db.session.commit()
            console.print("[bold green]Event updated successfully!")
        except Exception as e:
            console.print(f"[bold red]Error updating the event: {str(e)}[/bold red]")


def delete_event():
    """Delete event"""

    if not has_permission(UserRole.MANAGEMENT):
        console.print("[bold red]Permission denied : only managers can delete events.")
        return

    console.print("\n[bold yellow]Deleting an event")

    event_id = Prompt.ask("[bold yellow]ID of the event to delete")

    with app.app_context():
        event = db.session.get(Event, event_id)
        if not event:
            console.print("[bold red]Event not found!")
            return

        try:
            # Delete the event
            db.session.delete(event)
            db.session.commit()
            console.print("[bold green]Event deleted successfully!")
        except Exception as e:
            console.print(f"[bold red]Error deleting the event: {str(e)}[/bold red]")


if __name__ == '__main__':
    login_user()
    main_menu()