from django.shortcuts import render
from customers.models import Customer
from books.models import Book, BookTitle
from django.http import HttpResponseRedirect

def change_theme(request):
    """
    This checks if the `is_dark_mode` key exists in the session data. Session data is used to store information 
    about a user's session across different requests.
    """
    if 'is_dark_mode' in request.session:

        """
         If the `is_dark_mode` key exists, this line toggles its value. 
         If it was `True`, it becomes `False`, and vice versa.
        """
        request.session['is_dark_mode'] = not request.session['is_dark_mode']

    else:
        """
        If the `is_dark_mode` key doesn't exist in the session, this initializes it and sets it to `True`, enabling dark mode.
        """
        request.session['is_dark_mode'] = True

        """
         This redirects the user back to the page they came from. `HTTP_REFERER` is an HTTP header 
         sent by the browser that indicates the URL of the page that referred the user to the current page.
        """
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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