from datetime import datetime
import re

def validate_date(input_date):
    """
    Validates if the input_date is in the correct format (YYYY-MM-DD).
    """
    try:
        datetime.strptime(input_date, "%Y-%m-%d")
        return input_date
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

def validate_email(email):
    """
    Validates if the email is in a proper format.
    """
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(regex, email):
        raise ValueError("Invalid email format.")
    return email

def validate_phone(phone):
    """
    Validates if the phone number contains only digits and has 10 to 15 characters.
    """
    if not phone.isdigit() or not (10 <= len(phone) <= 15):
        raise ValueError("Invalid phone number. It must contain only digits and be 10 to 15 characters long.")
    return phone
