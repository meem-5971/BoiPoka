from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('details/<int:pk>/', views.DetailBookView.as_view(), name='book_detail'),
]