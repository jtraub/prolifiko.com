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


new_goal_tip = 'Tip: What you write is up to you but try to be specific, eg ' \
               'you might want to write for an amount of time or to a word ' \
               'count, or on a specific project.'


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['text']
        widgets = {
            'text': forms.Textarea(
                attrs={'placeholder': new_goal_tip})}


new_step_tip = 'Tip: Don’t think about the project as a whole. Just think ' \
               'about the one thing you can do next to progress your writing.'


class NewStepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['text']
        widgets = {
            'text': forms.Textarea(
                attrs={'placeholder': new_step_tip})}


track_step_tip = 'Tip: Tell us any progress you made. Number of words, ' \
                 'length of time etc. If you struggled with this step, be ' \
                 'nice to yourself, set a smaller step next time!'


class TrackStepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['comments']
        widgets = {
            'comments': forms.Textarea(
                attrs={'placeholder': track_step_tip})}
