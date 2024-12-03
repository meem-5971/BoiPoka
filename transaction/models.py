from django.db import models
from account.models import UserAccount
from book.models import Book
from django.contrib.auth.models import User


# Create your models here.
class Transactions(models.Model):
    account=models.ForeignKey(UserAccount,related_name='transaction',on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=12,decimal_places=2)
    timestamp=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['timestamp']

class Borrow(models.Model):
    borrow_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='borrow_user')
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING, related_name='user')
    balance_after_borrow=models.IntegerField(null=True, blank=True)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.book.title} Borrowed By {self.borrower.user.username}"