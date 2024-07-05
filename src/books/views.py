from django.shortcuts import render

from .models import BookTitle

# Create your views here.

def book_title_list_view(request):
    books = BookTitle.objects.all()
    return render(request,'books/main.html', {'books' : books})

def book_title_detail_view(request, pk):
    book_details = BookTitle.objects.get(pk=pk)
    return render(request, 'books/detail.html', {'book_details':book_details})


""" with slug
def book_title_detail_view(request, **kwargs):
    slug = kwargs.get('slug')
"""
