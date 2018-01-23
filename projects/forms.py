from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Form, URLField, CharField, ChoiceField, BooleanField

from projects.models import Project, MyUser


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class SignUpForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username', 'password1', 'password2', 'token')


def make_import_projects_form(categories):
    class ImportProjectsForm(Form):
        use = BooleanField(label='Import')
        name = CharField(max_length=50)
        url = URLField()
        tags = CharField(max_length=50, required=False)
        category = ChoiceField(choices=categories)
    return ImportProjectsForm
