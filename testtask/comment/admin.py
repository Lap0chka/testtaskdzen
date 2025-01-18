from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from comment.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):  # type: ignore
    """
    Admin configuration for the Comment model.
    """

    list_display = (
        "username",
        "email",
        "text_snippet",
        "is_approved",
        "created",
        "updated",
    )
    list_filter = ("is_approved", "created", "updated")
    search_fields = ("username", "email", "text")
    ordering = ("-created",)
    raw_id_fields = ("parent",)
    actions = ["approve_comments"]

    def text_snippet(self, obj: Comment) -> str:
        """
        Returns a truncated snippet of the comment text.
        """
        return obj.text[:50] + ("..." if len(obj.text) > 50 else "")  # type: ignore

    text_snippet.short_description = "Comment Snippet"  # type: ignore

    @admin.action(description="Approve selected comments")  # type: ignore
    def approve_comments(self, request: HttpRequest, queryset: QuerySet[Comment]) -> None:
        """
        Custom action to mark selected comments as approved.
        """
        updated_count = queryset.update(is_approved=True)
        self.message_user(request, f"{updated_count} comment(s) successfully approved.")
