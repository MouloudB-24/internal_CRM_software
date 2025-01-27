from app import create_app, db
from app.models.user import User, UserRole
from app.utils.validators import validate_email
from rich.console import Console
from rich.prompt import Prompt

app = create_app()
console = Console()

with app.app_context():
    console.print("[bold green]Create an administrator account[/bold green]\n")

    # Collect user input with validation
    while True:
        email = Prompt.ask("[bold magenta]Enter the administrator's email[/bold magenta]")
        if validate_email(email):
            break
        console.print("[bold red]Invalid email format. Please try again.[/bold red]")
    password = Prompt.ask("[bold magenta]Enter the administrator's password[/bold magenta]", password=True)

    # Check fields and uniqueness
    if not all([email, password]):
        console.print("[bold red]All fields are required![/bold red]")
    elif User.query.filter_by(email=email).first():
        console.print("[bold red]An account with this email already exists.[/bold red]")
    else:
        # Create the admin user
        admin = User(
            username="admin",
            email=email,
            phone="0123456789",
            role="Management"
        )
        admin.set_password(password)

        db.session.add(admin)
        db.session.commit()
        console.print("[bold green]Superuser created successfully![/bold green]")
