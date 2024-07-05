from django.contrib import admin
from .models import BookTitle
from .models import Book
# Register your models here.

admin.site.register(BookTitle)
admin.site.register(Book)
