from typing import List

from celery import shared_task
import logging

from django.core.mail import send_mail

from testtask import settings

logger = logging.getLogger(__name__)


@shared_task  # type: ignore
def send_comment_notification(username: str, text: str) -> bool:
    """
    Sends an email notification when a new comment is added.

    Args:
        username (str): The username of the person who wrote the comment.
        text (str): The text of the comment.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    subject = f"The comments were updated by {username}"
    message = f"The user {username} wrote:\n{text}"
    recipients: List[str] = ["danya.tkachenko.1997@gmail.com"]

    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipients)
        return True
    except Exception as e:
        # Log the error (replace with proper logging in production)
        print(f"Error sending email: {e}")
        return False
