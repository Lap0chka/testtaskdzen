import uuid
from typing import Optional

import bleach
from django.http import HttpResponse, HttpRequest
from django.utils.cache import patch_cache_control


def clean_html(user_input: str) -> str:
    """
    Sanitizes HTML input by allowing only specific tags and attributes.

    Args:
        user_input (str): The raw HTML input from the user.

    Returns:
        str: The sanitized HTML.
    """
    allowed_tags = ["a", "code", "i", "strong"]
    allowed_attributes = {"a": ["href", "title"]}

    try:
        cleaned_input = bleach.clean(
            user_input,
            tags=allowed_tags,
            attributes=allowed_attributes,
            strip=True
        )
    except Exception as e:
        # Log the error if needed
        print(f"Error during HTML cleaning: {e}")
        return ""

    return cleaned_input


def user_specific_cache_control(response: HttpResponse) -> HttpResponse:
    """
    Applies user-specific cache control to the given HTTP response.

    Args:
        response (HttpResponse): The HTTP response to modify.

    Returns:
        HttpResponse: The modified HTTP response with private cache control.
    """
    patch_cache_control(response, private=True)
    return response

def check_session(request: HttpRequest, user_key: Optional[str]) -> bool:
    """
    Checks and updates the user session based on a user-specific key.

    Args:
        request (HttpRequest): The HTTP request object.
        user_key (Optional[str]): The user key stored in the session.

    Returns:
        bool: False if the user key exceeds a threshold and the user is not authenticated, True otherwise.
    """
    try:
        if user_key is None:
            # Generate a new user key and initialize it with a counter value of 1
            user_key = str(uuid.uuid4())
            request.session['user_key'] = f'{user_key}1'
        else:
            # Extract the numeric value from the last character, increment it, and update the session
            value = int(user_key[-1]) if user_key[-1].isdigit() else 0
            value += 1
            request.session['user_key'] = f'{user_key[:-1]}{value}'

        # Check if the key exceeds the threshold and the user is not authenticated
        if int(request.session['user_key'][-1]) > 3 and not request.user.is_authenticated:
            return False
        return True
    except Exception as e:
        # Log the error (replace print with proper logging in production)
        print(f"Error in check_session: {e}")
        return False
