from django.forms import ModelForm
from django.contrib.auth.models import User

class User_form(ModelForm):
    class Meta:
        model=User
        fields=['username', 'email', 'password']

