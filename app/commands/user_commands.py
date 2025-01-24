from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from app import db, create_app
from app.auth import has_permission
from app.models.user import User, UserRole

console = Console()
app = create_app()

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