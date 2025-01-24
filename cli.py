from rich.console import Console
from rich.prompt import Prompt

console = Console()

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

    console.print("\n[bold green]Manage users")
    console.print("1 - Create user")
    console.print("2 - main")
    choice = Prompt.ask("[bold green]Enter your choice", choices=["1", "2"])

    if choice == "1":
        console.print("[bold yellow]Cette fonctionnalité sera implémentée dans l'étape 2.[/bold yellow]")
    elif choice == "2":
        main_menu()


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