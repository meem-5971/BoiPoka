from django.urls import path
from .views import DepositMoneyView,BorrowBookView,ReturnBookView,BorrowHistoryView,WriteReviewView

urlpatterns = [
    path('deposit/',DepositMoneyView.as_view(),name='deposit_money'),
    path('return_book/<int:pk>', ReturnBookView.as_view() ,name='return_book'),
    path('borrow_book/<int:pk>', BorrowBookView.as_view(), name='borrow_book'),
    path('borrow_history/',BorrowHistoryView.as_view(), name='borrow_history'),
    path('write_review/<int:pk>/', WriteReviewView.as_view(), name='write_review'),
]
