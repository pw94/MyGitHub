from django.shortcuts import render, redirect

from projects.models import Category


def show_categories(request):
    return render(request, "categories.html", {'categories': Category.objects.all()})


def add_category(request):
    if request.method == 'POST':
        parent_id = request.POST['parent_id']
        parent = Category.objects.get(id=parent_id)
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
