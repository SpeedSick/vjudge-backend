"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter

from authentication.views import UserViewSet, StudentsListView, TeachersListView, PasswordChangeView, PasswordResetView, \
    PasswordResetConfirmView

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='User')

urlpatterns = [
                  path('login/', obtain_jwt_token, name='login'),
                  path('students/', StudentsListView.as_view(), name='students-list'),
                  path('teachers/', TeachersListView.as_view(), name='teachers-list'),
                  path(route='change_password/', view=PasswordChangeView.as_view(), name='change_password'),
                  path(route='password_reset/', view=PasswordResetView.as_view(), name='password_reset'),
                  path(route='password_reset/<slug:reset_token>/', view=PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm')

              ] + router.urls
