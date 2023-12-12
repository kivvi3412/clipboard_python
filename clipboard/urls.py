"""
URL configuration for clipboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from mainapp import views
from mainapp.views import upload_file, list_files, download_file, delete_file
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('api/register/', views.register),
    path('api/login/', views.login),
    path('api/text/', views.user_text),

    path('api/upload/', upload_file),
    path('api/files/', list_files),
    path('api/download/', download_file),
    path('api/delete/', delete_file),

    path('register/', views.register_page, name='register_page'),
    path('login/', views.login_page, name='login_page'),
    path('', views.text_page, name='text_page'),
]

urlpatterns += staticfiles_urlpatterns()
