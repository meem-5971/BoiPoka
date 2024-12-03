from http.client import HTTPResponse
from django.views.generic import CreateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transactions,Borrow
from .forms import TransactionForm,DepositForm
from django.contrib import messages
from django.shortcuts import get_object_or_404,render,redirect
from django.views import View
from django.urls import reverse_lazy
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from account.models import UserAccount
from book.models import Book
from django.contrib.auth.decorators import login_required
from book.forms import ReviewForm

def send_transaction_email(user,amount,subject,template):
        message=render_to_string(template,{
            'user':user,
            'amount':amount,
        })
        
        send_email =EmailMultiAlternatives(subject,'',to=[user.email])
        send_email.attach_alternative(message,'text/html')
        send_email.send()

class TransactionCreateMixin(LoginRequiredMixin,CreateView):
    template_name= 'transaction/transaction_form.html'
    model_name=Transactions
    title=''
    success_url=reverse_lazy('profile')
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
        })
        return context
    
class DepositMoneyView(TransactionCreateMixin):
    form_class=DepositForm
    title='Add Money' #user j title dekhbe page ar tab ay

    
    def form_valid(self, form):
        amount=form.cleaned_data.get('amount')
        account=self.request.user.account
        account.balance+=amount
        account.save(
            update_fields=['balance']
        )
        messages.success(self.request,f"{amount}tk was added successfully")
        
        send_transaction_email(self.request.user,amount,"Deposit Message","transaction/deposite_email.html")
        return super().form_valid(form)
    
def send_borrow_email(user_account, borrow, subject, template):
    context = {
        'user': user_account.user,  # Assuming UserAccount has a related user
        'borrow': borrow,
    }
    
    message = render_to_string(template, context)
    
    send_email = EmailMultiAlternatives(subject, '', to=[user_account.user.email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()


class BorrowBookView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        user_account = get_object_or_404(UserAccount, user=request.user)
        
        if user_account.balance >= book.price:
            user_account.balance -= book.price
            user_account.save()

            borrow, created = Borrow.objects.get_or_create(borrow_user=request.user, book=book)
            borrow.balance_after_borrow = user_account.balance
            borrow.save()

            messages.success(request, f"{book.title} is borrowed successfully!")
            send_borrow_email(user_account, borrow, "Book Borrowing Message", "transaction/borrow_email.html")
            return redirect('borrow_history')
        else:
            messages.error(request, "Insufficient balance to borrow this book.")
            return redirect('book_detail', pk=book.pk)

class ReturnBookView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        user_account = get_object_or_404(UserAccount, user=request.user)
        borrow_book = get_object_or_404(Borrow, borrow_user=request.user, book=book)
        
        user_account.balance += book.price
        user_account.save()

        messages.success(request, f"{book.title} is returned successfully!")
        send_borrow_email(user_account, borrow_book, "Book Returning Message", "transaction/return_email.html")
        borrow_book.delete()
        
        return redirect('borrow_history')

class BorrowHistoryView(LoginRequiredMixin, View):
    def get(self, request):
        borrow_history = Borrow.objects.filter(borrow_user=request.user)
        return render(request, 'transaction/borrow_history.html', {'borrow_history': borrow_history})
     

class WriteReviewView(LoginRequiredMixin, View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        initial_data = {
            'user': request.user,
            'book': book,
        }
        review_form = ReviewForm(initial=initial_data)
        return render(request, 'transaction/review_form.html', {'review_form': review_form, 'book': book})
    
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.user = request.user
            new_review.book = book
            new_review.save()
            messages.success(request, "Your review has been added successfully.")
            return redirect('book_detail', pk=pk)  # Redirect to book detail page or any other appropriate page
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, 'transaction/review_form.html', {'review_form': review_form, 'book': book})