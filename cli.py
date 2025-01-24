from rich.console import Console
from rich.prompt import Prompt

from app.auth import login_user
from app.commands.contract_commands import create_contract, list_contracts, update_contract, delete_contract
from app.commands.customer_commands import create_costumer, list_costumers, update_costumer, delete_customer
from app.commands.event_commands import create_event, list_events, update_event, delete_event
from app.commands.user_commands import create_user, list_users

console = Console()

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


if __name__ == '__main__':
    login_user()
    main_menu()