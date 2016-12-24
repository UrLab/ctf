from .models import User, Team
from django import forms


class UserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.widgets.PasswordInput,
                                label="Password")
    password2 = forms.CharField(widget=forms.widgets.PasswordInput,
                                label="Password (again)")

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username', 'affiliation')

    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        super(UserForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


def _team_uniqueness(name):
    if Team.objects.filter(name=name.strip()).exists():
        raise forms.ValidationError("A team with the same name already exists.")


class CreateTeamForm(forms.Form):
    name = forms.CharField(max_length=30, label="Team name", validators=[_team_uniqueness])
