from django import forms
from django_registration.forms import RegistrationFormUniqueEmail

from .models import CustomUser


class CustomRegistrationForm(RegistrationFormUniqueEmail):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(max_length=100, help_text='eg. youremail@mail.com')
    date_of_birth = forms.DateField(required=False, help_text='MM/DD/YYYY')

    class Meta(RegistrationFormUniqueEmail.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',
                  'username', 'date_of_birth', 'password1', 'password2')
