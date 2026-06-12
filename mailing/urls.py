from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import (HomeView, MailCreateView, MailDeleteView, MailDetailView, MailListView, MailUpdateView,
                           MessageCreateView, MessageDeleteView, MessageDetailView, MessageListView, MessageUpdateView,
                           RecipientCreateView, RecipientDeleteView, RecipientDetailView, RecipientListView,
                           RecipientUpdateView)

app_name = MailingConfig.name


urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path(
        "recipient/recipient_list/", RecipientListView.as_view(), name="recipient_list"
    ),
    path(
        "recipient/recipient_detail/<int:pk>/",
        cache_page(60)(RecipientDetailView.as_view()),
        name="recipient_detail",
    ),
    path("recipient/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path(
        "recipient/<int:pk>/update/",
        RecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipient/<int:pk>/delete/",
        RecipientDeleteView.as_view(),
        name="recipient_delete",
    ),
    path("message/message_list/", MessageListView.as_view(), name="message_list"),
    path(
        "message/message_detail/<int:pk>/",
        cache_page(60)(MessageDetailView.as_view()),
        name="message_detail",
    ),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path(
        "message/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "message/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path("mail/mail_list/", MailListView.as_view(), name="mail_list"),
    path(
        "mail/mail_detail/<int:pk>/",
        cache_page(60)(MailDetailView.as_view()),
        name="mail_detail",
    ),
    path("mail/create/", MailCreateView.as_view(), name="mail_create"),
    path("mail/<int:pk>/update/", MailUpdateView.as_view(), name="mail_update"),
    path("mail/<int:pk>/delete/", MailDeleteView.as_view(), name="mail_delete"),
]
