from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from uuid import uuid4

from .models import Goal, Step


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = uuid4().hex[:-2]

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, strip=False,
                               widget=forms.PasswordInput)


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['text']
        widgets = {
            'text': forms.Textarea(
                attrs={'placeholder': 'Define your step here'}),
        }


class NewStepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['text']
        widgets = {
            'text': forms.Textarea(
                attrs={'placeholder': 'Define your step here'}),
        }


class TrackStepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['comments']
        widgets = {
            'comments': forms.Textarea(
                attrs={'placeholder': 'Add some optional comments'}),
        }
