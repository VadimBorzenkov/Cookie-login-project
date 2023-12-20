"""
URL configuration for laba3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from users.views import IndexView, UserLoginView, UserRegistrationView, UserLogoutView,  user_json_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('user/', user_json_view, name='user_json_view'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
