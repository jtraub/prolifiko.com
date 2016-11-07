import pytz
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
import django.contrib.auth.forms as auth
from django.core.validators import validate_email
from django.conf import settings
from uuid import uuid4

from django.db import transaction

from .models import Goal, Step, Timezone, Subscription


def validate_unique_email(value):
    if User.objects.filter(email=value).count() > 0:
        raise forms.ValidationError('Email address already registered')


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label='First name', required=True)

    email = forms.EmailField(required=True, validators=[
        validate_email, validate_unique_email])

    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput)

    timezone = forms.ChoiceField(label='Timezone', required=True,
                                 choices=[(tz, tz) for tz in
                                          pytz.common_timezones])

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password',)

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.username = uuid4().hex[:-2]

        password_validation.validate_password(
            self.cleaned_data.get('password'), self.instance)
        user.set_password(self.cleaned_data.get('password'))

        if commit:
            with transaction.atomic():
                user.save()

                Timezone.objects.create(user=user,
                                        name=self.cleaned_data['timezone'])

                if user.email in settings.CONTINUE_USERS:
                    Subscription.objects.create(user=user, name='auto')

        return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(strip=False, widget=forms.PasswordInput)


new_step_tip = 'Tip: Don’t think about the project as a whole. Just think ' \
               'about the one thing you can do next to progress your writing.'


class NewStepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['name', 'description']
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': new_step_tip,
                'onClick': 'limitText(this, true)'
            })}


track_step_tip = 'Tell us what progress you made.'


class TrackStepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['comments']
        widgets = {
            'comments': forms.Textarea(attrs={
                'placeholder': track_step_tip,
                'onClick': 'limitText(this, true)'
            })}


class SetPasswordForm(auth.SetPasswordForm):
    new_password2 = None

    def clean_new_password2(self):
        self.cleaned_data.set('new_password2', 'new_password1')

        return super().clean_new_password2()
