from datetime import datetime
import re

def validate_date(input_date):
    """
    Validates if the input_date is in the correct format (YYYY-MM-DD).
    """

    if datetime.strptime(input_date, "%Y-%m-%d"):
        return True
    return False


def validate_email(email):
    """
    Validates if the email is in a proper format.
    """
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(regex, email):
        return False
    return True

def validate_phone(phone):
    """
    Validates if the phone number contains only digits and has 10 to 15 characters.
    """
    if not phone.isdigit() or not (10 <= len(phone) <= 15):
        return False
    return True
