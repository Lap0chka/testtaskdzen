from captcha.models import CaptchaStore
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from .form import CommentForm
from .models import Comment


class IndexViewTests(TestCase):  # type: ignore
    def setUp(self) -> None:
        """
        Set up test environment with a client, URL, and a parent comment.
        """
        self.client = Client()
        self.url = reverse("index")
        self.parent_comment = Comment.objects.create(
            username="tester",
            email="tester@gmail.com",
            text="Parent Comment",
            is_approved=True,
        )

    def test_get_request_renders_template(self) -> None:
        """
        Test that a GET request to the index view renders the correct template
        and includes expected context variables.
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")
        self.assertIn("comments", response.context)
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], CommentForm)

    def test_post_request_valid_form(self) -> None:
        """
        Test that a valid POST request adds a new comment, links it correctly,
        and redirects back to the index page with a success message.
        """
        captcha_key = CaptchaStore.generate_key()
        captcha_value = CaptchaStore.objects.get(hashkey=captcha_key).response
        data = {
            "username": "tester2",
            "email": "tester2@gmail.com",
            "text": "New comment text",
            "parent": self.parent_comment.id,
            "captcha_0": captcha_key,
            "captcha_1": captcha_value,
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)

        self.assertEqual(Comment.objects.count(), 2)
        new_comment = Comment.objects.latest("id")
        self.assertEqual(new_comment.text, "New comment text")
        self.assertEqual(new_comment.parent, self.parent_comment)
        self.assertTrue(new_comment.is_approved)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "The comment has been added.")

    def test_post_request_invalid_form(self) -> None:
        """
        Test that an invalid POST request does not create a new comment
        and redirects back with error messages.
        """
        data = {
            "username": "tester3",
            "email": "tester3@gmail.com",
            "text": "",  # Invalid: text field is empty
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)
        self.assertEqual(Comment.objects.count(), 1)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("This field is required." in str(message) for message in messages))

    def test_parent_comment_linking(self) -> None:
        """
        Test that a new comment correctly links to its parent comment.
        """
        captcha_key = CaptchaStore.generate_key()
        captcha_value = CaptchaStore.objects.get(hashkey=captcha_key).response
        data = {
            "username": "tester2",
            "email": "tester2@gmail.com",
            "text": "Reply to parent",
            "parent": self.parent_comment.id,
            "captcha_0": captcha_key,
            "captcha_1": captcha_value,
        }

        self.client.post(self.url, data)

        new_comment = Comment.objects.latest("id")
        self.assertEqual(new_comment.parent, self.parent_comment)

    def test_missing_parent_comment(self) -> None:
        """
        Test that submitting a comment with a non-existent parent ID handles gracefully.
        """
        captcha_key = CaptchaStore.generate_key()
        captcha_value = CaptchaStore.objects.get(hashkey=captcha_key).response
        data = {
            "username": "tester2",
            "email": "tester2@gmail.com",
            "text": "Reply to non-existent parent",
            "parent": 9999,  # Non-existent ID
            "captcha_0": captcha_key,
            "captcha_1": captcha_value,
        }

        response = self.client.post(self.url, data)

        self.assertEqual(Comment.objects.count(), 1)  # No new comment should be created
        self.assertEqual(response.status_code, 302)
