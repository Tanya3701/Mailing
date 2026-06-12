from django.core.exceptions import ValidationError
from django.forms import ModelForm

from mailing.models import Mail, Message, Recipient


class MailForm(ModelForm):
    class Meta:
        model = Mail
        exclude = ("owner", "status")

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        if start_time > end_time:
            raise ValidationError("Начало рассылки не может быть позже ее окончания")
        elif start_time < start_time:
            raise ValidationError("Начало рассылки не может быть раньше ее начала")

    def __init__(self, *args, **kwargs):
        super(MailForm, self).__init__(*args, **kwargs)
        self.fields["message"].widget.attrs.update({"class": "form-control"})
        self.fields["recipients"].widget.attrs.update({"class": "form-control"})


class MailManagerForm(ModelForm):
    class Meta:
        model = Mail
        fields = ("status", "end_time")


class RecipientForm(ModelForm):
    class Meta:
        model = Recipient
        fields = "__all__"


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
