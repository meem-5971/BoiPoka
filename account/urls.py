from django.urls import path,include
from .views import UserRegistrationView,UserLoginView,UserAccountUpdateView
from . import views

urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('profile/', UserAccountUpdateView.as_view(), name='profile' )
]