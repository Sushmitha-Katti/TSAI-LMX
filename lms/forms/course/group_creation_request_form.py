from django import forms
from  lms.models.users_model import Student
from lms.models.enrollment_model import Enrollment

def get_students(user_id, course_id): 
  
    STUDENT_EMAILS = [
   ( enrollment.student.user.email,enrollment.student.user.username,) for enrollment in Enrollment.objects.filter(course_id = course_id).exclude(student__user_id =user_id)

    ]

    print("d,fd", STUDENT_EMAILS)
    

    return STUDENT_EMAILS



class GroupCreationRequestForm(forms.Form):

   
    
        
    def __init__(self,*args, **kwargs):
      
        user_id = kwargs.pop('user_id')
        pk = kwargs.pop('pk')
        super(GroupCreationRequestForm,self).__init__(*args, **kwargs) 
        mails = get_students(user_id = user_id, course_id = pk)

        print('mails', mails)
        self.fields['student_email'] = forms.MultipleChoiceField(
   
        widget=forms.CheckboxSelectMultiple(attrs={
            "name": "student_email", "class": "input100"
           
        }),
        choices = mails )

    class Meta:
        model = Enrollment
        fields = ['student_email']
        
      
        
    
    
    
        
    

    