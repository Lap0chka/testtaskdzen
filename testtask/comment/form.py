from captcha.fields import CaptchaField
from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """
    Form for creating and submitting comments, including CAPTCHA validation.
    """

    parent = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(),
        help_text="ID of the parent comment, used for replies.",
    )

    captcha = CaptchaField(
        help_text="Please complete the CAPTCHA to submit your comment."
    )

    class Meta:
        model = Comment
        fields = ["username", "email", "text", "file", "captcha"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Enter your comment",
                    "class": "form-control",
                }
            ),
            "username": forms.TextInput(
                attrs={"placeholder": "Your Name", "class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Your Email", "class": "form-control"}
            ),
            "file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "id": "file-upload",
                    "name": "file",
                    "accept": ".jpg,.jpeg,.png,.gif,.txt",
                }
            ),
        }
        help_texts = {"file": "You can upload files in formats: txt, jpg, png, gif."}

    def clean_text(self) -> str:
        """
        Custom validation for the text field.
        Ensures the comment is not empty or too short.
        """
        text: str = self.cleaned_data.get("text", "").strip()
        if len(text) < 5:
            raise forms.ValidationError(
                "The comment is too short. Please provide more details."
            )
        return text

    def clean_email(self) -> str:
        """
        Custom validation for the email field.
        Ensures the email address is in a valid format and belongs to a real domain.
        """
        email: str = self.cleaned_data.get("email", "").strip()
        if not email:
            raise forms.ValidationError("Email address is required.")
        return email

    def clean_username(self) -> str:
        """
        Custom validation for the username field.
        Ensures the username is at least 2 characters long.
        """
        username: str = self.cleaned_data.get("username", "").strip()
        if len(username) < 2:
            raise forms.ValidationError(
                "The username must be at least 2 characters long."
            )
        return username
