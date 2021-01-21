# Core Django imports.
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from django.core.mail import send_mail
from django.http import HttpResponse

# Blog application imports.
from lms.models.course_model import Course


#EMail imports
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# LMS app imports
from lms.forms.course.group_creation_request_form import GroupCreationRequestForm
from lms.forms.course.mail_to_admin_form import MailToAdminForm





class CourseListView(ListView):
    model = Course
    context_object_name = "courses"
    template_name = "lms/course/home.html"





class GroupCreationRequestView(LoginRequiredMixin, View):
    """
    Group Creation Request To another Student
    """
    template_name = 'dashboard/student/group_creation_request.html'

    home_template = 'dashboard/student/dashboard_home.html'

    def get(self, request, *args, **kwargs):
        
        pk = self.kwargs['pk']
     
        self.context_object = {"group_creation_form": GroupCreationRequestForm(user_id = request.user.id, pk = pk),'pk' : pk}

        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):
        request_form = GroupCreationRequestForm(data=request.POST)
        if request_form.is_valid():
            message = f"Hi\n{request.user.username} wants to create a group with you"
            subject = "Request to create Group"
            res = send_mail(subject=subject, message=message, from_email= request.user.email,recipient_list= request_form.cleaned_data['student_email'] )
            return render(request,self.home_template)


class MailToAdminView(LoginRequiredMixin, View):
    """
    Send Mail to admin/teacher
    """
   
    template_name = 'dashboard/student/mail_to_admin.html'

    home_template = 'dashboard/student/dashboard_home.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        
        self.context_object = {"mail_to_admin_form": MailToAdminForm(pk = pk)}

        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):
        email_form = MailToAdminForm(data=request.POST)
        if email_form.is_valid():
            html_message = email_form.cleaned_data['body']
            subject = email_form.cleaned_data['subject']
            plain_message = strip_tags(html_message)
            res = send_mail(subject=subject, message=plain_message, from_email = request.user.email,recipient_list= email_form.cleaned_data['staff_email'],html_message=html_message )
            return render(request,self.home_template)
