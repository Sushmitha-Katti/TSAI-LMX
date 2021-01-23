# Core Django imports.
from django.utils.encoding import force_bytes, force_text
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404


from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages



from django.core.mail import send_mail
from django.http import HttpResponse
from lms.token import account_activation_token

from lms.models.enrollment_model import Section, Enrollment

# Blog application imports.
from lms.models.course_model import Course, Section


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
        pk = self.kwargs['pk']
        user_id = request.user.id
        request_form = GroupCreationRequestForm(data=request.POST, user_id = user_id, pk = pk)
        
        if request_form.is_valid():
            current_site = get_current_site(request)
            student_emails =  request_form.cleaned_data['student_email']
            group_name = request_form.cleaned_data['name']
            try : 
                is_group_exists = Section.objects.get(name = group_name )
            except :
                is_group_exists = None
            course_enrolled = Enrollment.objects.get(course_id = pk, student__user_id = user_id)
           
            try :

                course_enrolled = Enrollment.objects.get(course_id =pk, student__user_id = user_id)
                
            except : 
                print("error")
                course_enrolled = None

            if(not(is_group_exists) and course_enrolled and not(course_enrolled.section) ):
                group = Section(name = group_name)
                group.save()
                course_enrolled.section = group
                course_enrolled.save()

            else : 
                print("Either you are already in a group nor the group name already exists")
                HttpResponse("Error!")


            for mail in student_emails : 
               
                user = User.objects.get(username = 'test_student')
                message = render_to_string('dashboard/student/group_creation_request_email.html',
                {
                    'user':user ,
                    'course_id' : kwargs['pk'],
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(str(user.pk)+"+"+group_name)),
                    'token': account_activation_token.make_token(user),
                    'from_user' : request.user
                })
            
                subject = "Request to create Group"
                res = send_mail(subject=subject, message=message, from_email= request.user.email,recipient_list= [mail] )
            
            return render(request,self.home_template)

class GroupCreationRequestSentView(View):

    def get(self, request, ck, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            
            
            pk = int(uid.split("+")[0])

            group_name = uid.split("+")[-1]
   
            user = User.objects.get(pk=pk)
            
                
        except (TypeError, ValueError, OverflowError):
            user = None
            print(TypeError, ValueError, OverflowError)
        
        
        if user is not None and group_name is not None and account_activation_token.check_token(user,token):
           
            if( request.user == user):
                course_enrolled = Enrollment.objects.get(course_id =ck, student__user = user)
                
                try :

                    course_enrolled = Enrollment.objects.get(course_id =ck, student__user = user)
                    
                    section = Section.objects.get(name = group_name)
                    print(course_enrolled.section, section)
                    
                except : 
                    print("error")
                    course_enrolled = None
                    messages.error(request, f"You are not enrolled in any course or section section doesn't exist"
                             )
                if(course_enrolled  and  not(course_enrolled.section)):
                    course_enrolled.section = section
                    course_enrolled.save()
                    print("enrolled successfully!")

                
                    messages.success(request, f"Congratulations {user.username} !!! "
                                      f"Now you are part of {group_name}"
                             )
                else :
                     messages.error(request, f"You may be already in a group. Check out!!! "
                                      
                             )

            else : 

                messages.error(request, f"You are not the one whom the request is sent to or you may be already existed in some group"
                             )

           

            

            

            return redirect('lms:login')
        else:
            return render(request, 'account/account_activation_invalid.html')
            
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
