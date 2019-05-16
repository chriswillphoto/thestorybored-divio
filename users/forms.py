from django import forms
from django.utils.translation import ugettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm


class CustomUserEditForm(UserEditForm):
    bio = forms.CharField(required=False, label=_("Bio"))


class CustomUserCreationForm(UserCreationForm):
    bio = forms.CharField(required=False, label=_("Bio"))
