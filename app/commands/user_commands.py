import sentry_sdk
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from sentry_sdk import capture_message

from app import db, create_app
from app.auth import has_permission
from app.models.user import User, UserRole
from app.utils.validators import validate_email, validate_phone

console = Console()
app = create_app()

def create_user():
    """Create a new user"""

    if not has_permission(UserRole.MANAGEMENT):
        console.print("[bold red]Permission denied : Only managers can create users.")
        return

    console.print("\n[bold yellow]Create a new user[/bold yellow]")

    username = Prompt.ask("[bold yellow]Name[/bold yellow]")

    while True:
        email = Prompt.ask("[bold yellow]Email[bold yellow]")
        if validate_email(email):
            break
        console.print("[red]Invalid email format[/red]")

    while True:
        phone = Prompt.ask("[bold yellow]Phone")
        if validate_phone(phone):
            break
        console.print("[red]Invalid phone number. It must contain only digits and be 10 to 15 characters long.[/red]")

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

            # Log to Sentry
            capture_message(f"User '{username}' created successfully.", level="info")

        except Exception as e:
            console.print(f"[bold red]User creation error : {str(e)}[/bold red]")
            sentry_sdk.capture_exception(e)

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

def delete_user():
    """Delete User"""

    if not has_permission(UserRole.MANAGEMENT):
        console.print("[bold red]Permission denied : Only managers can create users.")
        return

    console.print("\n[bold yellow]Deleting a user")

    user_id = Prompt.ask("[bold yellow]User ID to be deleted")

    with app.app_context():
        user = db.session.get(User, user_id)
        if not user:
            console.print("[bold red]User not found!")
            return

        try:
            db.session.delete(user)
            db.session.commit()
            console.print("[bold green]User successfully deleted")
        except Exception as e:
            console.print(f"[bold red]Deleted error: {str(e)}[/bold red]")
