from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from app import db, create_app
from app.models.event import Event
from app.models.user import UserRole
from app.auth import has_permission
from app.utils.validators import validate_date

console = Console()
app = create_app()


def create_event():
    """Create a new event"""

    if not has_permission(UserRole.SUPPORT):
        console.print("[bold red]Permission denied : only supports and managers can create events.")
        return

    console.print("\n[bold yellow]Create a new event")

    contract_id = Prompt.ask("[bold yellow]Associated contrast ID")
    support_contact_id = Prompt.ask("[bold yellow]Support contact ID", default="None")
    name = Prompt.ask("[bold yellow]Event name")
    status = Prompt.ask("[bold yellow]Event status", choices=["Planned", "In_progress", "Completed"])

    while True:
        start_date = Prompt.ask("[bold yellow]Start date (YYYY-MM-DD)")
        if validate_date(start_date):
            break
        console.print("[red]Invalid date format. Please use YYYY-MM-DD.[/red]")

    while True:
        end_date = Prompt.ask("[bold yellow]End date (YYYY-MM-DD)")
        if validate_date(end_date):
            break
        console.print("[red]Invalid date format. Please use YYYY-MM-DD.[/red]")

    location = Prompt.ask("[bold yellow]Event location")
    attendees = Prompt.ask("[bold yellow]Number of attendees", default="0")
    notes = Prompt.ask("[bold yellow]Notes (optional)", default="")

    with app.app_context():
        try:
            event = Event(
                contract_id=int(contract_id),
                support_contact_id=int(support_contact_id) if support_contact_id != "None" else None,
                name=name,
                status=status,
                start_date=start_date,
                end_date=end_date,
                location=location,
                attendees=int(attendees),
                notes=notes
            )
            db.session.add(event)
            db.session.commit()
            console.print("[bold green]Event successfully created!")

        except Exception as e:
            console.print(f"[bold red]Event creation error: {str(e)}[/bold red]")


def list_events():
    """Show events"""

    console.print("\n[bold yellow]Event list")

    with app.app_context():
        events = Event.query.all()

        if not events:
            console.print("[bold red]No event found!")
            return

        table = Table(title="Registered events")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Contract", style="magenta")
        table.add_column("Contact support", style="magenta")
        table.add_column("Name", style="magenta")
        table.add_column("Status", style="magenta")
        table.add_column("Start", style="magenta")
        table.add_column("End", style="magenta")
        table.add_column("Location", style="magenta")
        table.add_column("Attendees", style="magenta")

        for event in events:
            table.add_row(
                str(event.id),
                str(event.contract_id),
                str(event.support_contact_id) if event.support_contact_id else "None",
                event.name,
                str(event.status.value),
                event.start_date.strftime("%Y-%m-%d"),
                event.end_date.strftime("%Y-%m-%d"),
                event.location,
                str(event.attendees)
            )

        console.print(table)

def update_event():
    """Update event"""

    if not has_permission(UserRole.SUPPORT):
        console.print("[bold red]Permission denied : only supports and managers can update events.")
        return

    console.print("\n[bold yellow]Updating an event")

    event_id = Prompt.ask("[bold yellow]ID of the event to update")

    with app.app_context():
        event = db.session.get(Event, event_id)
        if not event:
            console.print("[bold red]Event not found!")
            return

        # Prompt for new values
        contract_id = Prompt.ask("[bold yellow]Contract ID", default=str(event.contract_id))
        support_contact_id = Prompt.ask("[bold yellow]Support Contact ID", default=str(event.support_contact_id) if event.support_contact_id else "None")
        name = Prompt.ask("[bold yellow]Event Name", default=event.name)
        status = Prompt.ask("[bold yellow]Status (Planned, In_progress, Completed)", default=event.status)
        start_date = Prompt.ask("[bold yellow]Start Date (YYYY-MM-DD)", default=event.start_date.strftime("%Y-%m-%d"))
        end_date = Prompt.ask("[bold yellow]End Date (YYYY-MM-DD)", default=event.end_date.strftime("%Y-%m-%d"))
        location = Prompt.ask("[bold yellow]Location", default=event.location)
        attendees = Prompt.ask("[bold yellow]Number of Attendees", default=str(event.attendees))
        notes = Prompt.ask("[bold yellow]Notes", default=event.notes if event.notes else "")

        try:
            # Update the event
            event.contract_id = int(contract_id)
            event.support_contact_id = int(support_contact_id) if support_contact_id.lower() != "none" else None
            event.name = name
            event.status = status
            event.start_date = start_date
            event.end_date = end_date
            event.location = location
            event.attendees = int(attendees)
            event.notes = notes
            db.session.commit()
            console.print("[bold green]Event updated successfully!")
        except Exception as e:
            console.print(f"[bold red]Error updating the event: {str(e)}[/bold red]")


def delete_event():
    """Delete event"""

    if not has_permission(UserRole.MANAGEMENT):
        console.print("[bold red]Permission denied : only managers can delete events.")
        return

    console.print("\n[bold yellow]Deleting an event")

    event_id = Prompt.ask("[bold yellow]ID of the event to delete")

    with app.app_context():
        event = db.session.get(Event, event_id)
        if not event:
            console.print("[bold red]Event not found!")
            return

        try:
            # Delete the event
            db.session.delete(event)
            db.session.commit()
            console.print("[bold green]Event deleted successfully!")
        except Exception as e:
            console.print(f"[bold red]Error deleting the event: {str(e)}[/bold red]")
