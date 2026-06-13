from datetime import datetime

from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from mailing.models import MailingAttempt


class MailingService:

    @staticmethod
    def send_mailing(mail):
        recipients = mail.recipients.all()
        for recipient in recipients:
            try:
                answer = send_mail(
                    mail.message.theme,
                    mail.message.body,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[recipient.email],
                    fail_silently=False,
                )
                attempt_status = "Успешно"

            except Exception as e:
                answer = str(e)
                attempt_status = "Не успешно"

            MailingAttempt.objects.create(
                mail=mail, sending_status=attempt_status, mail_server_response=answer
            )
        if attempt_status == "Успешно":
            mail.status = "Запущена"
            mail.start_time = datetime.today
            mail.save()
