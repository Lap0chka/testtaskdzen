from django.urls import path

from comment import views

urlpatterns = [
    path("", views.CommentListView.as_view(), name="index"),
    path("preview/", views.preview_message, name="preview_message"),
]
