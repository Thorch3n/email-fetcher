# forms.py

from django import forms
from .models import EmailAccount


class EmailAccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = EmailAccount
        fields = ['email', 'password', 'provider']
