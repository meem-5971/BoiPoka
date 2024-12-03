from django.shortcuts import render
from book.models import Book
from genre.models import Genre

def home(request, genre_slug = None):
    data = Book.objects.all()

    if genre_slug is not None:
        genre = Genre.objects.get(slug=genre_slug)
        data = Book.objects.filter(genre=genre)
    genres = Genre.objects.all()

    return render(request, 'index.html', {'data' : data, 'genre' : genres})