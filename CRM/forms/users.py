from django.forms import ModelForm
from django.contrib.auth.models import User

class User_form(ModelForm):
    class Meta:
        model=User
        fields=['username', 'email', 'password']

    def save(self, commit=True):
        user = super(User_form, self).save(commit = False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
