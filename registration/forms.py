from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from manager.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define attributes
        field_attributes = {
            'username': {
                'class': 'form-control rounded-3',
                'id': 'username',
                'placeholder': 'Username',
            },
            'email': {
                'class': 'form-control rounded-3',
                'id': 'email',
                'placeholder': 'Email',
            },
            'password1': {
                'class': 'form-control rounded-3',
                'id': 'password1',
                'placeholder': 'Password',
            },
            'password2': {
                'class': 'form-control rounded-3',
                'id': 'password2',
                'placeholder': 'Password confirmation',
            },
        }

        # Set attributes
        for field_name, attributes in field_attributes.items():
            for attribute_name, attribute_value in attributes.items():
                self.fields[field_name].widget.attrs[attribute_name] = attribute_value

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define attributes
        field_attributes = {
            'username': {
                'class': 'form-control rounded-3',
                'id': 'username',
                'placeholder': 'Username',
            },
            'password': {
                'class': 'form-control rounded-3',
                'id': 'password',
                'placeholder': 'Password',
            },
        }

        # Set attributes
        for field_name, attributes in field_attributes.items():
            for attribute_name, attribute_value in attributes.items():
                self.fields[field_name].widget.attrs[attribute_name] = attribute_value


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define attributes
        field_attributes = {
            'email': {
                'class': 'form-control rounded-3',
                'id': 'email',
                'placeholder': 'Email',
            },
        }
        
        # Set attributes
        for field_name, attributes in field_attributes.items():
            for attribute_name, attribute_value in attributes.items():
                self.fields[field_name].widget.attrs[attribute_name] = attribute_value


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define attributes
        field_attributes = {
            'new_password1': {
                'class': 'form-control rounded-3',
                'id': 'new_password1',
                'placeholder': 'New Password',
            },
            'new_password2': {
                'class': 'form-control rounded-3',
                'id': 'new_password2',
                'placeholder': 'Confirm New Password',
            }
        }
        
        # Set attributes
        for field_name, attributes in field_attributes.items():
            for attribute_name, attribute_value in attributes.items():
                self.fields[field_name].widget.attrs[attribute_name] = attribute_value