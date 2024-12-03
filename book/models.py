from django.db import models
from genre.models import Genre 
from django.contrib.auth.models import User
from django.db import models
from account.models import UserAccount

class Book(models.Model):
    title = models.CharField(max_length=50)
    # user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    borrower = models.ManyToManyField(User, blank=True)
    author = models.CharField(max_length=100,blank=True,null=True)
    content = models.TextField()
    price=models.IntegerField()
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='book/uploads/images/', blank=True, null=True)  # Separate folder for images
    ppdf = models.FileField(upload_to='book/uploads/files/', blank=True, null=True)  
    pdf_url = models.URLField(null=True, blank=True) 
    def __str__(self):
        return self.title 

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=30)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"Comments by {self.name}"

