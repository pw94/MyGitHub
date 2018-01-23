"""MyGitHub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from projects.views import show_categories, add_category, delete_category, add_project, get_projects, delete_project, \
    signup, home, import_projects

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('signup/', signup, name='signup'),
    path('categories/', show_categories, name='categories'),
    path('categories/add/', add_category, name='add_category'),
    path('categories/delete/<int:category_id>/', delete_category, name='delete_category'),
    path('projects/', get_projects, name='projects'),
    path('projects/add/<int:category_id>/', add_project, name='add_project'),
    path('projects/add/', add_project, name='add_project'),
    path('projects/delete/<int:project_id>/', delete_project, name='delete_project'),
    path('projects/import/', import_projects, name='import_projects'),
]
