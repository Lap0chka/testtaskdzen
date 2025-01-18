import logging
from typing import Any, Dict

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView

from .form import CommentForm
from .models import Comment
from .task import send_comment_notification
from .utils import clean_html, comment_limit

logger = logging.getLogger(__name__)


@method_decorator(never_cache, name="dispatch")
class CommentListView(ListView):  # type: ignore
    """
    View for displaying a list of comments and handling comment submissions.
    """
    model = Comment
    template_name = "base.html"
    context_object_name = "comments"
    paginate_by = 25

    def get_queryset(self) -> Comment.objects.none[...] | Comment.objects.all[...]:
        """
        Fetches the queryset of approved parent comments with prefetching for replies.

        Returns:
            QuerySet: A queryset of approved parent comments with sorting applied.
        """
        try:
            queryset = Comment.approved.filter(parent__isnull=True).prefetch_related(
                "replies"
            )
            logger.info("Fetched %d approved comments.", queryset.count())

            # Sorting logic
            sort_by = self.request.GET.get("sort", "created")
            order = self.request.GET.get("order", "asc")

            if sort_by in ["username", "email", "created"]:
                if order == "desc":
                    sort_by = f"-{sort_by}"
                queryset = queryset.order_by(sort_by)
            return queryset
        except Exception as e:
            logger.error(
                "An error occurred while fetching comments: %s", str(e), exc_info=True
            )
            return Comment.objects.none()

    def get_context_data(self, **kwargs: Any) -> Dict[Any, Any]:
        """
        Adds the comment form to the context.

        Args:
            **kwargs: Additional keyword arguments for the context.

        Returns:
            Dict[Any, Any]: The updated context with the comment form included.
        """
        context: Dict[Any, Any] = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["current_sort"] = self.request.GET.get("sort", "created")
        context["current_order"] = self.request.GET.get("order", "asc")
        return context

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Handles the submission of a new comment.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Redirects to the index view after processing the comment.
        """
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                if not request.user.is_authenticated and not comment_limit(request):
                    messages.error(
                        request,
                        "You cant add more comments.Try latter after 10 minutes"
                    )
                    return redirect(reverse("index"))
                # Create a new comment object but don't save it yet
                comment = form.save(commit=False)
                comment.is_approved = (
                    True  # Automatically approve the comment (if required)
                )
                cleaned_content = clean_html(form.cleaned_data["text"])
                comment.text = cleaned_content
                # Handle parent comment linking
                parent_id = form.cleaned_data.get("parent")
                if parent_id:
                    parent_comment = get_object_or_404(Comment, pk=parent_id)
                    comment.parent = parent_comment
                    logger.info(
                        "Linked the new comment to parent comment ID: %d", parent_id
                    )

                # Save the comment and display success message
                comment.save()
                # Send email notification to the admin
                send_comment_notification.delay(comment.username, comment.text)
                logger.info("New comment saved successfully: %s", comment)
                messages.success(request, "The comment has been added.")
            except Exception as e:
                logger.error(
                    "An error occurred while saving the comment: %s",
                    str(e),
                    exc_info=True,
                )
                messages.error(request, "An error occurred while adding the comment.")
        else:
            logger.warning("Invalid form submission: %s", form.errors)
            # Display error messages if the form is invalid
            for error in form.errors.values():
                messages.error(request, error)

        # Redirect to the same page to display updated comments
        return redirect(reverse("index"))


@csrf_exempt  # type: ignore
def preview_message(request: HttpRequest) -> HttpResponse:
    """
    Handles the preview of a comment message.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response with the preview data or validation errors.
    """
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)

        # Remove CAPTCHA field for preview
        if "captcha" in form.fields:
            del form.fields["captcha"]

        if form.is_valid():
            try:
                # Clean and extract form data
                username: str = form.cleaned_data["username"]
                email: str = form.cleaned_data["email"]
                text: str = clean_html(form.cleaned_data["text"])

                # Return JSON response with the preview
                return JsonResponse(
                    {
                        "username": username,
                        "email": email,
                        "text": text,
                    }
                )
            except Exception as e:
                # Log the error and return a server error response
                print(f"Error during comment preview: {e}")
                return JsonResponse({"error": "Server error"}, status=500)

        # Return validation errors
        return JsonResponse({"errors": form.errors}, status=400)

    # Handle invalid request method
    return JsonResponse({"error": "Invalid request method"}, status=405)
