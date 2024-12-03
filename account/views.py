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

# Create your views here.
class UserRegistrationView(FormView):
    template_name='account/registration.html'
    form_class=UserRegistrationForm
    success_url=reverse_lazy('register')

    def form_valid(self,form):
        user=form.save()
        login(self.request,user)
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
