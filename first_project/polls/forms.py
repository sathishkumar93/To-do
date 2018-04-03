from django import forms
from . import views
#from .views import ResultsView
#from polls.views import edit_name
# no need this func here
from . import views
from .models import Choice, Question
import datetime
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm

TASK_STATUS_CHOICES= [
    ('new', 'New'),
    ('in progress', 'In Progress'),
    ('done', 'Done'),
    ]

class NameForm(forms.Form):
    your_name = forms.CharField(label='Task name', max_length=20)

class LoginForm(forms.Form):
    user_name = forms.CharField(label='User name', max_length=25)
    pass_word = forms.CharField(widget=forms.PasswordInput)

class EditForm(forms.Form):
    edit_text = forms.CharField(label='Edit task name', max_length=50)
    task_status = forms.CharField(label='Edit task status', widget=forms.Select(choices=TASK_STATUS_CHOICES))

class DeleteForm(forms.Form):
    delete_text = forms.CharField(label='Delete text', max_length=50)

class SignupForm(forms.Form):
    user_name = forms.CharField(label='User name', max_length=25)
    pass_word = forms.CharField(widget=forms.PasswordInput)
    contact_num = forms.CharField(label='contact number', max_length=25)

