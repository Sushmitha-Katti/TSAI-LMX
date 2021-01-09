from django import forms
from  lms.models.users_model import Student

STUDENT_EMAILS = [
   ( student.user.email,student.user.username,) for student in Student.objects.all()
]



class GroupCreationRequestForm(forms.Form):

    
    student_email = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={
            "name": "student_email", "class": "input100"
           
        }),
        
        choices = STUDENT_EMAILS)

    