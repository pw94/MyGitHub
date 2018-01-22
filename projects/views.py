from collections import namedtuple

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projects.forms import ProjectForm, SignUpForm
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
