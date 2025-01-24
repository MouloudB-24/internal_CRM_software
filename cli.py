from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from app import create_app, db
from app.models.customer import Customer
from app.models.user import User, UserRole

console = Console()
app = create_app()

def main_menu():
    """Application main menu"""

    while True:
        console.print("\n[bold green]Main menu")
        console.print("1 - Mange users")
        console.print("2 - Manage costumers")
        console.print("3 - Exit")

        choice = Prompt.ask("[bold purple]Enter your choice", choices=["1", "2", "3"])

        if choice == "1":
            user_menu()
        elif choice == "2":
            costumer_menu()
        elif choice == "3":
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



if __name__ == '__main__':
    main_menu()