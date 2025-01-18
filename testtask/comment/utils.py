from typing import Dict, Any

import bleach
from django.http import HttpResponse, HttpRequest
from django.utils.timezone import now
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


def comment_limit(request: HttpRequest) -> bool:
    """
    Limits the number of comments a user can make within a given time period.
    If the limit is exceeded, the user is banned for 10 minutes.

    Args:
        request: The HTTP request object.

    Returns:
        bool: True if the user can comment, False if banned.
    """
    COMMENT_LIMIT = 3
    BAN_DURATION = 10 * 60  # 10 minutes

    # Get the client's IP address from the request
    user_ip = getattr(request, 'ip_address', None)
    if not user_ip:
        raise ValueError("IP address not found. Ensure UserStatsMiddleware is properly configured.")

    # Access session data
    session = request.session
    if 'comment_data' not in session:
        session['comment_data'] = {}

    user_data: Dict[str, Any] = session['comment_data'].get(user_ip, {'comments': 0, 'ban_until': None})

    # Check if the user is currently banned
    current_time = now().timestamp()
    if user_data['ban_until'] and current_time < user_data['ban_until']:
        return False  # User is banned

    # Increment comment count
    user_data['comments'] += 1

    # If the user exceeds the comment limit, ban them
    if user_data['comments'] > COMMENT_LIMIT:
        user_data['ban_until'] = current_time + BAN_DURATION
        user_data['comments'] = 0  # Reset comment counter after banning
        session['comment_data'][user_ip] = user_data
        session.save()
        return False   # User is now banned

    # Save updated user data to session
    session['comment_data'][user_ip] = user_data
    session.save()
    return True   # User is allowed to comment
