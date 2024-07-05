from django.shortcuts import render
from customers.models import Customer
from books.models import Book, BookTitle

def home_view(request):
    qs = Customer.objects.all()
    # book = Book.objects.get(id=1)
    book = BookTitle.objects.get(id=1)
    
    # we want to retrieve all books associated with this book title related_name='books'
    books = book.books

    print(books)
    context = {
        'qs': qs, 
        'book': book
        }
    
    return render(request, 'main.html', context )