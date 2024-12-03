from django.shortcuts import render,redirect
from django.views.generic import FormView,View
from django.contrib.auth.views import LoginView
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth import login,logout
from django.urls import reverse_lazy
from . import forms
from django.contrib.auth.decorators import login_required
from book.models import Book
from transaction.models import Borrow
from account.models import UserAccount,UserAddress
#from django.db import IntegrityError
from django.utils.crypto import get_random_string

class UserRegistrationView(FormView):
    template_name = 'account/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('register')

    def generate_unique_account_no(self):
        """Generate a unique account number."""
        while True:
            account_no = get_random_string(length=12, allowed_chars='0123456789')  # Increased length
            if not UserAccount.objects.filter(account_no=account_no).exists():
                break
        return account_no

    def form_valid(self, form):
        # Create the user instance
        user = form.save()

        # Generate a unique account_no
        account_no = self.generate_unique_account_no()

        # Create the UserAccount instance
        user_account = UserAccount.objects.create(
            user=user,
            account_no=account_no,
            age=form.cleaned_data['age'],
            gender=form.cleaned_data['gender'],
            balance=0,  # Default balance
            birth_date=form.cleaned_data['birth_date']
        )

        # Create the UserAddress instance
        user_address = UserAddress.objects.create(
            user=user,
            street_name=form.cleaned_data['street_name'],
            city=form.cleaned_data['city'],
            postal_code=form.cleaned_data['postal_code'],
            country=form.cleaned_data['country']
        )

        # Log the user in after creation
        login(self.request, user)

        return super().form_valid(form)


    
class UserLoginView(LoginView):
    template_name='account/login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    
def user_logout(request):
    logout(request)
    return redirect('home')

class UserAccountUpdateView(View):
    template_name = 'account/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})
