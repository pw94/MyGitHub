from django.shortcuts import render, redirect

from projects.forms import ProjectForm
from projects.models import Category


def show_categories(request):
    return render(request, "categories.html", {'categories': Category.objects.all()})


def add_category(request):
    if request.method == 'POST':
        parent_id = request.POST['parent_id']
        parent = Category.objects.get(id=parent_id) if parent_id else None
        name = request.POST['category_name']
        Category.objects.create(name=name, parent=parent)
    return redirect(show_categories)


def delete_category(request, category_id):
    node = Category.objects.get(id=category_id)
    if request.method == 'POST':
        node.delete()
        return redirect(show_categories)
    else:
        return render(request, "delete_category.html", {'node': node})


def add_project(request, category_id=None):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(show_categories)
    category = Category.objects.get(id=category_id) if category_id else Category.objects.all()[:1].get()
    form = ProjectForm(initial={'category': category})
    return render(request, 'add_project.html', {'form': form})
