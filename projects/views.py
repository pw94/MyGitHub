from django.shortcuts import render

from projects.models import Category


def show_categories(request):
    return render(request, "categories.html", {'categories': Category.objects.all()})
