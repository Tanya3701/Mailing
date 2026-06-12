from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from mailing.models import STATUS_ATTEMPT, Mail, MailingAttempt


class Command(BaseCommand):
    help = "Send mail"

    def handle(self, *args, **options):
        mails = Mail.objects.filter(status="Запущена" or "Создана")
        for mail in mails:
            for recipient in mail.recipients.all():
                try:
                    send_mail(
                        mail.message.theme,
                        mail.message.body,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[recipient.email],
                        fail_silently=False,
                    )
                    MailingAttempt.objects.create(
                        date=timezone.now(),
                        status=STATUS_ATTEMPT[0][0],
                        mail=mail,
                    )
                    print("Рассылка успешна")
                except Exception as e:
                    MailingAttempt.objects.create(
                        date=timezone.now(),
                        status=STATUS_ATTEMPT[1][0],
                        mail_server_response=str(e),
                        mail=mail,
                    )
                    print("Попытка рассылки не удалась")
                    print(str(e))
            mail.save()
