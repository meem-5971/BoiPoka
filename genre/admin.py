from django.contrib import admin
from . import models
# Register your models here.

# admin.site.register(models.Category)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    
admin.site.register(models.Genre, GenreAdmin)