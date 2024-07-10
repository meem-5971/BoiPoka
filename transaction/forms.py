from django import forms
from .models import Transactions

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['amount',]

        #transaction type customer ar edit korar option off kore dicchi
    def __init__(self,*args,**kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args,**kwargs)
       
    def save(self,commit=True):
        self.instance.account = self.account
        return super().save()
    
class DepositForm(TransactionForm):
    def clean_amount(self): #amount k filter korbo
        min_deposit_amount =100
        amount=self.cleaned_data.get('amount') #amount value from user filled form
        if amount < min_deposit_amount:
            raise forms.ValidationError(f'You need to deposit at least {min_deposit_amount}tk')
        return amount