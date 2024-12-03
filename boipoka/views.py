from django.shortcuts import render, get_object_or_404
from book.models import Book
from genre.models import Genre


def home(request, genre_name=None):
    """
    View for displaying books. If a genre_name is provided, filter books by genre.
    Otherwise, display all books.
    """
    # Fetch all books initially
    data = Book.objects.all()

    # Filter books by genre if genre_name is provided
    if genre_name:
        genre = get_object_or_404(Genre, name=genre_name)  # Fetch genre by name
        data = data.filter(genre=genre)
    else:
        genre = None  # No genre filter applied

    # Fetch all genres for navigation
    genres = Genre.objects.all()

    # Pass data and genres to the template
    return render(request, 'index.html', {
        'data': data,        # List of books
        'genres': genres,    # List of all genres
        'selected_genre': genre  # Currently selected genre, if any
    })
