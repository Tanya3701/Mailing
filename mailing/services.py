from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from mailing.models import STATUS_ATTEMPT, Mail, MailingAttempt, Recipient


class MailingService:

    @staticmethod
    def send_mailing(self, mailing_id):
        mailing = Mail.objects.get(id=mailing_id)
        if timezone.now() < mailing.start_time:
            raise Exception("Нельзя отправлять рассылки раньше начальной даты")
        elif timezone.now() > mailing.end_time:
            raise Exception("Нельзя отправлять рассылки после даты окончания")
        else:
            ok = STATUS_ATTEMPT[0][0]
            fail = STATUS_ATTEMPT[1][0]
            recipients = Recipient.objects.filter(mailing_id=mailing_id)
            for recipient in recipients:
                try:
                    send_mail(
                        subject=mailing.message.body,
                        message=mailing.message.theme,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[recipient.email],
                        fail_silently=False,
                    )
                    attempt = ok
                    response = "ok"
                except Exception as e:
                    response = str(e)
                    attempt = fail

                MailingAttempt.objects.create(
                    date=timezone.now(),
                    status=attempt,
                    mail_server_response=response,
                )
                mailing.save()
