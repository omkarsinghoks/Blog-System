from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        print('login pass')
        self.request = kwargs.pop('request', None)  # Extract the request object
        super().__init__(*args, **kwargs)