from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from mailing.forms import MailForm, MailManagerForm, MessageForm, RecipientForm
from mailing.models import STATUS_ATTEMPT, STATUS_CHOICES, Mail, MailingAttempt, Message, Recipient


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    fields = "__all__"
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")

    def form_valid(self, form):
        recipient = form.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()
        return super().form_valid(form)


@method_decorator(cache_page(60 * 15), name="dispatch")
class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    context_object_name = "recipients"

    def get_queryset(self):
        if self.request.user.has_perm("mailing.can_view_recipient_list"):
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    context_object_name = "recipient"

    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    fields = "__all__"
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")

    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user)


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy("mailing:recipient_list")

    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


@method_decorator(cache_page(60 * 15), name="dispatch")
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = "messages"

    def get_queryset(self):
        if self.request.user.has_perm("mailing.can_view_message_list"):
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    context_object_name = "message"

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = "__all__"
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MailCreateView(LoginRequiredMixin, CreateView):
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy("mailing:mail_list")

    def form_valid(self, form):
        mail = form.save()
        user = self.request.user
        mail.owner = user
        mail.save()
        return super().form_valid(form)


@method_decorator(cache_page(60 * 15), name="dispatch")
class MailListView(LoginRequiredMixin, ListView):
    model = Mail
    context_object_name = "mails"

    def get_queryset(self):
        if self.request.user.has_perm("mailing.can_view_mail_list"):
            return Mail.objects.all()
        return Mail.objects.filter(owner=self.request.user)


class MailDetailView(LoginRequiredMixin, DetailView):
    model = Mail
    context_object_name = "mail"

    def get_context_data(self, **kwargs):
        context = super(MailDetailView, self).get_context_data(**kwargs)
        context["mail_recipients"] = self.object.recipients.all()
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        obj.save()
        return obj


class MailUpdateView(LoginRequiredMixin, UpdateView):
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy("mailing:mail_list")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailForm
        if user.has_perm("mailing.can_disabling_mailing"):
            return MailManagerForm
        raise PermissionDenied


class MailDeleteView(LoginRequiredMixin, DeleteView):
    model = Mail
    success_url = reverse_lazy("mailing:mail_list")

    def get_queryset(self):
        return Mail.objects.filter(owner=self.request.user)


@method_decorator(cache_page(60 * 15), name="dispatch")
class HomeView(TemplateView):
    template_name = "mailing/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mails"] = Mail.objects.all().count()
        context["mail_create"] = Mail.objects.filter(
            status=STATUS_CHOICES[1][0]
        ).count()
        context["mail_complete"] = Mail.objects.filter(
            status=STATUS_CHOICES[0][0]
        ).count()
        context["mail_run"] = Mail.objects.filter(status=STATUS_CHOICES[2][0]).count()
        context["total_attempt"] = MailingAttempt.objects.all().count()
        context["attempt_ok"] = MailingAttempt.objects.filter(
            status=STATUS_ATTEMPT[0][0]
        ).count()
        context["attempt_fail"] = MailingAttempt.objects.filter(
            status=STATUS_ATTEMPT[1][0]
        ).count()
        context["recipients"] = Recipient.objects.all().count()
        return context
