
from django.db.models.query import QuerySet
from django.shortcuts import redirect,get_object_or_404
from django.views.generic import DetailView,View,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from book.models import Book
from book.forms import ReviewForm


from django.contrib.auth.decorators import login_required
# Create your views here.

class DetailBookView(DetailView):
    model = Book
    pk_url_kwarg = 'pk'
    template_name = 'book/book_detail.html'
    
    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(data=self.request.POST)
        book = self.get_object()
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book= book
            new_review.save()
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        reviews = book.reviews.all()
        review_form =ReviewForm()
        
        context['review'] = reviews
        context['review_form'] = review_form
        return context
