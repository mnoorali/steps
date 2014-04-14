from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from stepsapp.models import Contact, Members, Groups, Stepslog
from django.forms.extras.widgets import SelectDateWidget
import datetime


class UserForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class MembersForm(forms.ModelForm):

    class Meta:
        model = Members
        fields = ['first_name', 'last_name']

class StepsForm(forms.ModelForm):
 #   date = forms.DateField(widget=SelectDateWidget(), initial=datetime.date.today)
 #   steps = forms.IntegerField(initial=0)
    stepsdate = forms.DateField(label='Select a Date:')
    steps = forms.IntegerField(label='Total steps for this date:')

    class Meta:
        model = Stepslog
        fields = ['stepsdate', 'steps']
        widgets = {
            'stepsdate': forms.DateInput(attrs={'id':'datepicker'}),
        }
