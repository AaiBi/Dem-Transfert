from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User


#Edit the first name, last name, email and the username
class EditUserInfoForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'username', 'password'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'name': 'first_name',
                                                 'placeholder': 'Entrez votre prénom : '}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'name': 'username',
                                            'placeholder': 'Entrez votre nom d\'utilisateur (Exemple: ibou2241)'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'name': 'last_name',
                                                'placeholder': 'Entrez votre nom de famille :'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'name': 'email',
                                            'placeholder': 'Entrez votre email :'}),
        }

    def clean(self):
        cleaned_data = super(EditUserInfoForm, self).clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')


class EditUserPasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = [
            'old_password', 'new_password1', 'new_password2'
        ]
        widgets = {
            'old_password': forms.PasswordInput(attrs={'class': 'form-control', 'name': 'old_password', 'type': 'password',
                                               'placeholder': 'Entrez votre actuel mot de passe :'}),
            'new_password1': forms.PasswordInput(attrs={'class': 'form-control', 'name': 'new_password1', 'type': 'password',
                                                   'placeholder': 'Entrez votre nouveau mot de passe :'}),
            'new_password2': forms.PasswordInput(attrs={'class': 'form-control', 'name': 'new_password2', 'type': 'password',
                                                   'placeholder': 'Entrez a nouveau votre nouveau mot de passe :'}),
        }

    def clean(self):
        cleaned_data = super(EditUserPasswordForm, self).clean()
        password = cleaned_data.get('password')