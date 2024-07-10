from django import forms
from .models import Book,Review

class ReviewForm(forms.ModelForm):
    class Meta: 
        model = Review
        fields = ['name', 'body']
        

class BookForm(forms.ModelForm):
    class Meta: 
        model = Book
        fields = '__all__'