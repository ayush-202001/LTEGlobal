from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from more_itertools import quantify
from .models import *
# Category, Product, Stock, Invoice, Invoice_Item
from datetime import datetime


class UserRegistration(UserCreationForm):
    email = forms.EmailField(max_length=250, help_text="The email field is required.")
    first_name = forms.CharField(max_length=250, help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250, help_text="The Last Name field is required.")

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")


class UpdateProfile(UserChangeForm):
    username = forms.CharField(max_length=250, help_text="The Username field is required.")
    email = forms.EmailField(max_length=250, help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250, help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250, help_text="The Last Name field is required.")
    current_password = forms.CharField(max_length=250)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')

    def clean_current_password(self):
        if not self.instance.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError(f"Password is Incorrect")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")


class UpdatePasswords(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm rounded-0'}), label="Old Password")
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm rounded-0'}), label="New Password")
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm rounded-0'}),
        label="Confirm New Password")

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')






class insertstudentform(forms.ModelForm):
    class Meta:
        model=tbl_student
        fields='__all__'
#
# class studentform(forms.ModelForm):
#     class Meta:
#         model=tbl_student
#         fields='__all__'
#
# class studentupdateform(forms.ModelForm):
#     class Meta:
#         model = tbl_student
#         fields = ['student_name','student_emailid','student_contactno','student_whatsappno','student_gender','student_dateOfbirth',
#                   'student_address','student_city','student_pincode','student_state',
#                   'student_qualification','student_course','modeofcourse','student_occupation','reference_by']


class stateform(forms.ModelForm):
    class Meta:
        model=tbl_state
        fields='__all__'

# class stateupdateform(forms.ModelForm):
#     class Meta:
#         model = tbl_state
#         fields = ['state_name','state_shortform']


class cityform(forms.ModelForm):
    class Meta:
        model=tbl_city
        fields='__all__'

# class cityupdateform(forms.ModelForm):
#     class Meta:
#         model = tbl_city
#         fields = ['city_name']


class qualificationform(forms.ModelForm):
    class Meta:
        model=tbl_qualification
        fields='__all__'
#
# class qualificationupdateform(forms.ModelForm):
#     class Meta:
#         model = tbl_qualification
#         fields = ['qualification_name']


class courceform(forms.ModelForm):
    class Meta:
        model=tbl_course
        fields='__all__'

# class courceupdateform(forms.ModelForm):
#     class Meta:
#         model = tbl_course
#         fields = ['course_name']

class referencebyform(forms.ModelForm):
    class Meta:
        model=tbl_referenceby
        fields='__all__'



class firstreceiptform(forms.ModelForm):
    class Meta:
        model=tbl_firstreceipt
        fields=('total','discountedfees','deposit','balance','discount')

class secondreceiptform(forms.ModelForm):
    class Meta:
        model=tbl_secondreceipt
        fields=('discountedfees','deposit','balance')



class exfeesdateform(forms.ModelForm):
    class Meta:
        model=tbl_exfeesdate
        fields=('current_date','paying_date','remark')


#########################################33




#####################Krunal############

class courseform(forms.ModelForm):
    class Meta:
        model=tbl_course
        fields='__all__'

class courseupdateform(forms.ModelForm):
    class Meta:
        model =tbl_course
        fields = ['course_name']

class chapterform(forms.ModelForm):
    class Meta:
        model=tbl_chapter
        fields='__all__'

class chapterupdateform(forms.ModelForm):
    class Meta:
        model = tbl_chapter
        fields = ['course_id','chapter_name']

class sessionform(forms.ModelForm):
    class Meta:
        model=tbl_session
        fields='__all__'

class sessionupdateform(forms.ModelForm):
    class Meta:
        model = tbl_session
        fields = ['chapter_id','session_name']


class studenttypeform(forms.ModelForm):
    class Meta:
        model=tbl_studenttype
        fields='__all__'

class studenttypeupdateform(forms.ModelForm):
    class Meta:
        model = tbl_studenttype
        fields = ['studenttype']



class exfeesdateform(forms.ModelForm):
    class Meta:
        model=tbl_city
        fields='__all__'


# class referencebyupdateform(forms.ModelForm):
#     class Meta:
#         model = tbl_referenceby
#         fields = ['referenceby_name']
#
#
# class SaveReceiptfees(forms.ModelForm):
#     class Meta:
#         model = tbl_feesreceipt
#         fields = ('invoice','site', 'customer','total', 'deposit', 'balance')