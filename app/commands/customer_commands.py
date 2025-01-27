from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from app import db, create_app
from app.auth import has_permission
from app.models.customer import Customer
from app.models.user import UserRole
from app.utils.validators import validate_phone

console = Console()
app = create_app()


def create_costumer():
    """Create a new costumer"""

    if not has_permission(UserRole.SALES):
        console.print("[bold red]Permission denied : only sales and managers can create costumers.")
        return

    console.print("\n[bold yellow]Create a new costumer")

    full_name = Prompt.ask("[bold yellow]Full name")
    email = Prompt.ask("[bold yellow]Email")

    while True:
        phone = Prompt.ask("[bold yellow]Phone")
        if validate_phone(phone):
            break
        console.print("[red]Invalid phone number. It must contain only digits and be 10 to 15 characters long.[/red]")

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
        console.print("[bold red]Permission denied : Only managers can delete users.")
        return

    console.print("\n[bold yellow]Deleting a customer")

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

