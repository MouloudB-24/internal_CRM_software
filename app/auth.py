from rich.console import Console
from rich.prompt import Prompt
from werkzeug.security import check_password_hash

from app import create_app
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

