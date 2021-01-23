from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View

from django.http import HttpResponse

#EMail imports
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# LMS app imports
from lms.forms.dashboard.mail_to_admin_form import MailToAdminForm


class MailToAdminView(LoginRequiredMixin, View):
    """
    Send Mail to admin/teacher
    """
    context_object = {"mail_to_admin_form": MailToAdminForm}
    template_name = 'dashboard/student/mail_to_admin.html'

    home_template = 'dashboard/student/dashboard_home.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):
        email_form = MailToAdminForm(data=request.POST)
        if email_form.is_valid():
            html_message = email_form.cleaned_data['body']
            subject = email_form.cleaned_data['subject']
            plain_message = strip_tags(html_message)
            res = send_mail(subject=subject, message=plain_message, from_email = request.user.email,recipient_list= email_form.cleaned_data['staff_email'],html_message=html_message )
            return render(request,self.home_template)
