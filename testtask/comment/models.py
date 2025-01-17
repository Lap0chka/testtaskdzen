from django.core.validators import FileExtensionValidator
from django.db import models

from django.db.models import QuerySet


class ApprovedManager(models.Manager):
    """
    Custom manager to retrieve only approved objects.
    """

    def get_queryset(self) -> QuerySet:
        """
        Overrides the default QuerySet to return only approved objects.

        This method filters the QuerySet to include only those objects
        where the `is_approved` field is set to `True`.

        Returns:
            QuerySet: A filtered QuerySet containing only approved objects.
        """
        return super().get_queryset().filter(is_approved=True)


class Comment(models.Model):
    """
    Model representing a comment with optional file attachments and nested replies.
    """

    username = models.CharField(
        max_length=100, help_text="The name of the user who posted the comment."
    )
    email = models.EmailField(
        max_length=100, help_text="The email address of the user."
    )
    text = models.TextField(help_text="The content of the comment.")
    file = models.FileField(
        upload_to="comments/",
        validators=[
            FileExtensionValidator(allowed_extensions=["txt", "jpg", "png", "gif"])
        ],
        null=True,
        blank=True,
        help_text="Optional file attachment. Allowed formats: txt, jpg, png, gif.",
    )
    created = models.DateTimeField(
        auto_now_add=True, help_text="The timestamp when the comment was created."
    )
    updated = models.DateTimeField(
        auto_now=True, help_text="The timestamp when the comment was last updated."
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        help_text="The parent comment for nested replies.",
    )
    is_approved = models.BooleanField(
        default=False, help_text="Indicates whether the comment is approved."
    )

    # Default and custom managers
    objects = models.Manager()
    approved = ApprovedManager()

    class Meta:
        ordering = ["-created"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self) -> str:
        """
        Returns a string representation of the comment, showing the username and the first 20 characters of the text.
        """
        return f"{self.username}: {self.text[:20]}"
