from datetime import timedelta

from django.db import models
from django.utils import timezone

from users.models import User

STATUS_CHOICES = [
    ("Завершена", "Завершена"),
    ("Создана", "Создана"),
    ("Запущена", "Запущена"),
]
STATUS_ATTEMPT = [("Успешно", "Успешно"), ("Не успешно", "Не успешно")]


class Recipient(models.Model):
    name = models.CharField(max_length=100, help_text="Введите имя клиента")
    email = models.EmailField(unique=True, help_text="Email клиента")
    comment = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["name"]
        permissions = [("can_view_recipient_list", "can view recipients list")]


class Message(models.Model):
    theme = models.CharField(max_length=100)
    body = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.body

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["theme"]
        permissions = [("can_view_message_list", "can view message list")]


class Mail(models.Model):
    start_time = models.DateTimeField(
        blank=False,
        null=False,
        default=timezone.now(),
        help_text="Введите дату предполагаемой рассылки",
    )
    end_time = models.DateTimeField(
        blank=False,
        null=False,
        default=timezone.now() + timedelta(hours=720),
        help_text="Введите дату окончания рассылки",
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=100, default="Создана")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.message.theme

    def update_status(self):
        start = self.start_time
        end = self.end_time
        if timezone.now() < start:
            self.status = STATUS_CHOICES[1][0]
        elif timezone.now() > end:
            self.status = STATUS_CHOICES[0][0]
        else:
            self.status = STATUS_CHOICES[2][0]

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["message"]
        permissions = [
            ("can_disabling_mailings", "can disabling_mailings"),
            ("can_view_mailing_list", "can view mailings list"),
        ]


class MailingAttempt(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_ATTEMPT, auto_created=True, max_length=100)
    mail_server_response = models.TextField(auto_created=True, blank=True, null=True)
    mail = models.ForeignKey(Mail, on_delete=models.CASCADE)

    def __str__(self):
        return self.mail_server_response

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = ["date"]
