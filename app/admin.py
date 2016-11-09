from django import forms
from django.contrib import admin
from django.contrib.auth.models import User

from .models import *

admin.site.register(Goal)
admin.site.register(Step)
admin.site.register(Timezone)


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, user):
        return user.email


class SubscriptionAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubscriptionAdminForm, self).__init__(*args, **kwargs)
        self.fields['user'] = UserChoiceField(queryset=User.objects.all())


class SubscriptionAdmin(admin.ModelAdmin):
    form = SubscriptionAdminForm

admin.site.register(Subscription, SubscriptionAdmin)
