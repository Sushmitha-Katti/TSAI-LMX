from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View
from django.core.mail import send_mail
from django.http import HttpResponse



# LMS app imports
from lms.forms.dashboard.group_creation_request_form import GroupCreationRequestForm


class GroupCreationRequestView(LoginRequiredMixin, View):
    """
    Group Creation Request To another Student
    """
    context_object = {"group_creation_form": GroupCreationRequestForm}
    template_name = 'dashboard/student/group_creation_request.html'

    home_template = 'dashboard/student/dashboard_home.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):
        request_form = GroupCreationRequestForm(data=request.POST)
        if request_form.is_valid():
            message = f"Hi\n{request.user.username} wants to create a group with you"
            subject = "Request to create Group"
            res = send_mail(subject=subject, message=message, from_email= request.user.email,recipient_list= request_form.cleaned_data['student_email'] )
            return render(request,self.home_template)
