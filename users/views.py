import secrets

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from mailing.models import STATUS_ATTEMPT, STATUS_CHOICES, Mail, MailingAttempt, Recipient
from users.forms import UserRegisterForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Верификация",
            message=f"Здравствуйте, перейдите по ссылке для подтверждения {url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = "user"

    def get_queryset(self):
        if self.request.user.has_perm("users.view_users"):
            return User.objects.all()
        raise PermissionDenied


class UserListView(ListView):
    model = User
    context_object_name = "users"
    template_name = "user_list.html"

    def get_queryset(self):
        if self.request.user.has_perm("users.view_users"):
            return User.objects.all()
        else:
            return User.objects.none()


class UserBlockView(LoginRequiredMixin, UserPassesTestMixin, View):
    model = User
    context_object_name = "user"

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.is_block = True
        user.is_active = False
        user.save()
        return redirect("users:user_detail", id=user_id)

    def test_func(self):
        if self.request.user.groups.filter(name="manager").exists():
            return True
        return None


class UserStatisticView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = "user_statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        mails = Mail.objects.filter(owner=user)
        for mail in mails:
            mailing_attempts = MailingAttempt.objects.filter(mail=mail)
            recipients = Recipient.objects.filter(mail=mail)
            context["total_attempt"] = mailing_attempts.count()
            context["attempt_ok"] = mailing_attempts.filter(
                status=STATUS_ATTEMPT[0][0]
            ).count()
            context["attempt_fail"] = mailing_attempts.filter(
                status=STATUS_ATTEMPT[1][0]
            ).count()
            context["recipients"] = recipients.count()
        context["mails"] = mails.count()
        context["mail_create"] = mails.filter(status=STATUS_CHOICES[1][0]).count()
        context["mail_complete"] = mails.filter(status=STATUS_CHOICES[0][0]).count()
        context["mail_run"] = mails.filter(status=STATUS_CHOICES[2][0]).count()
        return context
