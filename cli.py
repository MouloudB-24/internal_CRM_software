from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from app import create_app, db
from app.models.user import User, UserRole

console = Console()
app = create_app()

def main_menu():
    """Application main menu"""

    while True:
        console.print("\n[bold green]Main menu")
        console.print("1 - Mange users")
        console.print("2 - Mange costumers")
        console.print("3 - Exit")

        choice = Prompt.ask("[bold purple]Enter your choice", choices=["1", "2", "3"])

        if choice == "1":
            user_menu()
        elif choice == "2":
            client_menu()
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




def client_menu():
    """Costumers management menu"""

    console.print("\n[bold green]Manage [/bold green]")
    console.print("[bold yellow]1 - Create costumer")
    console.print("[bold yellow]2 - Back to main menu")

    choice = Prompt.ask("[bold green]Enter your choice[/bold green]", choices=["1", "2"])

    if choice == "1":
        console.print("[bold yellow]Cette fonctionnalité sera implémentée dans l'étape 3.[/bold yellow]")
    elif choice == "2":
        main_menu()


if __name__ == '__main__':
    main_menu()