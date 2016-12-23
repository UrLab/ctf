from .models import User
from django.forms import ModelForm


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'team', 'affiliation')
