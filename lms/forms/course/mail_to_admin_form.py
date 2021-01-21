from django import forms
from  lms.models.staff_course_model import StaffCourse
from ckeditor_uploader.widgets import  CKEditorUploadingWidget


def get_teachers(course_id): 
   
    STUDENT_EMAILS = [
   (staffcourse.staff.user.email,staffcourse.staff.user.username,) for staffcourse in StaffCourse.objects.filter(course_id = course_id)

    ]

    print("d,fd", STUDENT_EMAILS)
    

    return STUDENT_EMAILS


class MailToAdminForm(forms.Form):

    def __init__(self,*args, **kwargs):
       
    
        pk = kwargs.pop('pk')
        super(MailToAdminForm,self).__init__(*args, **kwargs) 
        mails = get_teachers(course_id = pk)

        print('mails', mails)
        self.fields['staff_email'] = forms.MultipleChoiceField(
   
        widget=forms.CheckboxSelectMultiple(attrs={
            "name": "staff_email", "class": "input100"
           
        }),
        choices = mails )
    
    body = forms.CharField(widget=CKEditorUploadingWidget())
    subject = forms.CharField(widget=forms.TextInput(attrs={
            "name": "subject", "class": "input100",
            "placeholder": "Subject Of Email"
        }))
    class Meta : 
        model = StaffCourse
        fields = ['staff_email', 'body', 'subject']