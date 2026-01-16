
from django.contrib import admin
from django.urls import include, path
from .views import RegistrationView, LoginView, LogoutView, TokenRefreshView

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]