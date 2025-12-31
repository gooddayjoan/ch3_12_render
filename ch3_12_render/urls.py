"""
URL configuration for ch3_12_render project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/',views.test),
    # path('search_list/',views.search_list, name='search_list'),
    path('search_list/',views.search_list),
    path('search_name/',views.search_name),
    path('index/',views.index),
    path('post/',views.post),
    path('edit/<int:id>/',views.edit),
    path('delete/<int:id>/',views.delete),
    # -------------web api----------------------
    path('getAllItems/',views.getAllItems),
    path('getItem/<int:id>/',views.getItem),
    path('createItem/',views.createItem),
    path('updateItem/<int:id>/', views.updateItem, name='updateItem'),
    path('deleteItem/<int:id>/', views.deleteItem, name='deleteItem')
]
