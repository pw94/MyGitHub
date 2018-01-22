from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from projects.models import Project, MyUser


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class SignUpForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username', 'password1', 'password2', 'token')
