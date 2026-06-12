from django.contrib import admin

from mailing.models import Mail, MailingAttempt, Message, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("name", "email")
    search_fields = (
        "name",
        "email",
    )
    list_filter = ("name",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("theme", "body")
    search_fields = (
        "theme",
        "body",
    )
    list_filter = ("theme",)


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ("start_time", "end_time", "message", "status")
    search_fields = (
        "message",
        "status",
    )
    list_filter = ("status",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("date", "status", "mail_server_response", "mail")
    list_filter = ("status",)
