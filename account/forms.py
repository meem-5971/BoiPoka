from typing import Any
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from account.models import UserAccount, UserAddress
from account.constants import GENDER_TYPE

from django.db import IntegrityError

from django.core.exceptions import ValidationError

class UserRegistrationForm(UserCreationForm):
    age = forms.IntegerField(label='বয়স')
    gender = forms.ChoiceField(choices=GENDER_TYPE, label='জেন্ডার')
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='জন্মতারিখ')
    street_name = forms.CharField(max_length=100, label='রাস্তার নাম')
    city = forms.CharField(max_length=100, label='শহর')
    postal_code = forms.IntegerField(label='পোস্টাল কোড')
    country = forms.CharField(max_length=100, label='দেশ')
    first_name = forms.CharField(max_length=100, label='প্রথম নাম')
    last_name = forms.CharField(max_length=100, label='শেষ নাম')
    email = forms.EmailField(max_length=100, label='ইমেইল')
    username = forms.CharField(label='ইউজারনেম')
    password1 = forms.CharField(label='পাসওয়ার্ড', widget=forms.PasswordInput)
    password2 = forms.CharField(label='পাসওয়ার্ড নিশ্চিত করুন', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2',
                  'age', 'gender', 'birth_date', 'street_name', 'city', 'postal_code', 'country']

    def save(self, commit=True):
        # Create the user instance without committing to the database
        new_user = super().save(commit=False)
        
        if commit:
            new_user.save()  # Save the user instance first

            # Check if the user already has a UserAccount
            try:
                user_account = UserAccount.objects.get(user=new_user)
                # If the UserAccount already exists, raise an error
                raise ValidationError("This user already has a registered account.")
            except UserAccount.DoesNotExist:
                # If no UserAccount exists, create it
                age = self.cleaned_data.get('age')
                gender = self.cleaned_data.get('gender')
                birth_date = self.cleaned_data.get('birth_date')
                
                account_no = 10000 + new_user.id  # Generate account number
                
                user_account = UserAccount.objects.create(
                    user=new_user,
                    account_no=account_no,
                    age=age,
                    gender=gender,
                    birth_date=birth_date
                )

            # Create UserAddress
            street_name = self.cleaned_data.get('street_name')
            city = self.cleaned_data.get('city')
            postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')
            
            user_address = UserAddress.objects.create(
                user=new_user,
                street_name=street_name,
                postal_code=postal_code,
                city=city,
                country=country
            )

        return new_user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add CSS classes for form styling
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })

class UserUpdateForm(forms.ModelForm):
    age = forms.IntegerField(label='বয়স')
    gender = forms.ChoiceField(choices=GENDER_TYPE, label='জেন্ডার')
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='জন্মতারিখ')
    street_name = forms.CharField(max_length=100, label='রাস্তার নাম')
    city = forms.CharField(max_length=100, label='শহর')
    postal_code = forms.IntegerField(label='পোস্টাল কোড')
    country = forms.CharField(max_length=100, label='দেশ')
    first_name = forms.CharField(max_length=100, label='প্রথম নাম')
    last_name = forms.CharField(max_length=100, label='শেষ নাম')
    email = forms.EmailField(max_length=100, label='ইমেইল')

    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
        
        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
            except UserAccount.DoesNotExist:
                user_account = None
                user_address = None

            if user_account:
                self.fields['gender'].initial = user_account.gender
                self.fields['age'].initial = user_account.age
                self.fields['birth_date'].initial = user_account.birth_date
                self.fields['street_name'].initial = user_address.street_name
                self.fields['city'].initial = user_address.city
                self.fields['postal_code'].initial = user_address.postal_code
                self.fields['country'].initial = user_address.country

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            user_account, create = UserAccount.objects.get_or_create(user=user)
            user_address, create = UserAddress.objects.get_or_create(user=user)

            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.gender = self.cleaned_data['gender']
            user_account.age = self.cleaned_data['age']
            user_account.save()

            user_address.street_name = self.cleaned_data['street_name']
            user_address.city = self.cleaned_data['city']
            user_address.country = self.cleaned_data['country']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.save()

        return user
