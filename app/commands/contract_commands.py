from rich.prompt import Prompt
from rich.table import Table
from rich.console import Console

from app import db, create_app
from app.models.contract import Contract
from app.models.user import UserRole
from app.auth import has_permission

console = Console()
app = create_app()

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

