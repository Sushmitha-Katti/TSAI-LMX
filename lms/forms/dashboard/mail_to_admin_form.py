from django import forms
from  lms.models.users_model import Staff
from ckeditor_uploader.widgets import  CKEditorUploadingWidget

STAFF_EMAILS = [
   ( staff.user.email,staff.user.username,) for staff in Staff.objects.all()
]



class MailToAdminForm(forms.Form):

    
    body = forms.CharField(widget=CKEditorUploadingWidget())
    subject = forms.CharField(widget=forms.TextInput(attrs={
            "name": "subject", "class": "input100",
            "placeholder": "Subject Of Email"
        }))
    staff_email = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={
            "name": "staff_email", "class": "input100"
        }),
        choices = STAFF_EMAILS)