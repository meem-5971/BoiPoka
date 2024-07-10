from django.contrib import admin
from .models import UserAccount,Transactions,Borrow
# Register your models here.
admin.site.register(Borrow)
@admin.register(Transactions)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'amount']