from http import HTTPStatus
from typing import Union, Tuple

from flask import Blueprint, request, jsonify, Response

from app import db
from app.models.event import Event
from app.models.user import UserRole
from app.utils import get_current_user, has_permission

event_bp = Blueprint('event', __name__)


@event_bp.route("/create", methods=["POST"])
def create_event() -> Union[Response, Tuple[Response, int]]:
    """Create an event"""

    # Verify current user
    user, error = get_current_user()
    if error:
        return error

    # Permission check: only "Support" or "Management" users can create events
    if not has_permission(user, UserRole.SUPPORT):
        return jsonify({"error": "Permission denied"}), HTTPStatus.OK

    # Retrieve request data
    data = request.get_json()
    contract_id = data.get("contract_id")
    name = data.get("name")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    location = data.get("location")
    attendees = data.get("attendees")
    notes = data.get("notes")

    if not all([contract_id, name, start_date, end_date, location, attendees, notes]):
        return jsonify({"error": "These fields [contract_id, name, start_date, end_date, location, attendees and notes]"
                                 " are required!"}), HTTPStatus.OK

    # Create a new event
    event = Event(
        contract_id=contract_id,
        support_contact_id=user.id,
        name=name,
        start_date=start_date,
        end_date=end_date,
        location = location,
        attendees = attendees,
        notes = notes)

    # Add the new event in the database
    db.session.add(event)
    db.session.commit()

    return jsonify({"message": "Event created successfully!"}), HTTPStatus.OK


@event_bp.route("/update/<int:event_id>", methods=["PUT"])
def update_event(event_id) -> Union[Response, Tuple[Response, int]]:
    """Update an event"""

    # Verify current user
    user, error = get_current_user()
    if error:
        return error

    # Permission check: only "Support" or "Management" users can create events
    if not has_permission(user, UserRole.SUPPORT):
        return jsonify({"error": "Permission denied"}), HTTPStatus.OK

    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), HTTPStatus.OK

    data = request.get_json()
    event.contract_id = data.get("contract_id", event.contract_id)
    event.support_contact_id = data.get("support_contact_id", event.support_contact_id)
    event.name = data.get("name", event.name)
    event.status = data.get("status", event.status)
    event.start_date = data.get("start_date", event.start_date)
    event.end_date = data.get("end_date", event.end_date)

    db.session.commit()
    return jsonify({"message": "Event updated successfully!"}), HTTPStatus.OK


@event_bp.route("/delete/<int:event_id>", methods=["DELETE"])
def delete_customer(event_id) -> Union[Response, Tuple[Response, int]]:
    """ Delete an event"""

    # Verify current user
    user, error = get_current_user()
    if error:
        return error

    # # Permission check: only "Management" users can delete events
    if not has_permission(user, UserRole.MANAGEMENT):
        return jsonify({"error": "Permission denied"}), HTTPStatus.OK

    event_to_delete = Event.query.get(event_id)
    if not event_to_delete:
        return jsonify({"error": "Event not found"}), HTTPStatus.OK

    db.session.delete(event_to_delete)
    db.session.commit()

    return jsonify({"message": "Event deleted successfully!"}), HTTPStatus.OK

