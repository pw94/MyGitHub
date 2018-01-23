from collections import namedtuple

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.shortcuts import render, redirect
from github import Github

from projects.forms import ProjectForm, SignUpForm, make_import_projects_form
from projects.models import Category, Project


def home(request):
    return render(request, "home.html", {'title': 'Home'})


@login_required
def show_categories(request):
    return render(request, "categories.html", {'categories': request.user.categories.all(), 'title': 'Categories'})


@login_required
def add_category(request):
    if request.method == 'POST':
        parent_id = request.POST['parent_id']
        parent = Category.objects.get(id=parent_id) if parent_id else None
        name = request.POST['category_name']
        Category.objects.create(name=name, parent=parent, owner=request.user)
    return redirect(show_categories)


@login_required
def delete_category(request, category_id):
    node = Category.objects.get(id=category_id)
    if request.method == 'POST':
        node.delete()
        return redirect(show_categories)
    else:
        return render(request, "delete_category.html", {'node': node, 'title': 'Delete category'})


@login_required
def add_project(request, category_id=None):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(show_categories)
    category = Category.objects.get(id=category_id) if category_id else Category.objects.all()[:1].get()
    form = ProjectForm(initial={'category': category})
    form.fields['category'].queryset = request.user.categories.all()
    return render(request, 'add_project.html', {'form': form, 'title': 'Add project'})


@login_required
def get_projects(request):
    if request.method == 'POST':
        project_name = request.POST['project_name']
        projects = Project.search(project_name, request.user)
        Project_DAO = namedtuple('Project_DAO', ['name', 'url'], verbose=True)
        pros = [Project_DAO(p.name, p.url) for p in projects]
        return render(request, 'projects.html', {'projects': pros, 'title': 'Projects', 'empty': 'No projects found.'})
    return render(request, 'projects.html', {'projects': [], 'title': 'Projects', 'empty': 'Search for the project'})


@login_required
def delete_project(request, project_id):
    node = Project.objects.get(id=project_id)
    if request.method == 'POST':
        node.delete()
        return redirect(show_categories)
    else:
        return render(request, "delete_project.html", {'node': node, 'title': 'Delete project'})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(show_categories)
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form, 'title': 'Sign up'})


@login_required
def import_projects(request):
    categories = [(c.id, c.name) for c in request.user.categories.all()]
    if request.method == 'POST':
        ImportProjectFormSet = formset_factory(make_import_projects_form(categories))
        formset = ImportProjectFormSet(request.POST)
        forms = formset.forms
        for form in forms:
            if form.is_valid() and 'use' in form.cleaned_data and form.cleaned_data['use']:
                project = form.cleaned_data
                del project['use']
                project['category_id'] = project.pop('category')
                tags = [p.strip() for p in project.pop('tags').split(',') if p]
                p = Project.objects.create(**project)
                if tags:
                    p.tags.add(*tags)
        return redirect(show_categories)
    g = Github(request.user.token)
    repos = [{'name': repo.name, 'url': repo.html_url} for repo in g.get_user().get_repos()]
    ImportProjectFormSet = formset_factory(make_import_projects_form(categories), min_num=len(repos), max_num=len(repos))
    formset = ImportProjectFormSet(initial=repos)
    return render(request, 'import_projects.html', {'formset': formset, 'title': 'Import projects'})
