from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import uuid

from .models import Goal, Step


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = uuid.uuid4()
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['text']


class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['text']
