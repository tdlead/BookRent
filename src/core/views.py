from django.shortcuts import render
from customers.models import Customer
from books.models import Book, BookTitle
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView
from django.db.models import Count,Sum

from rentals.models import Rental
from rentals.choices import STATUS_CHOICES
from publishers.models import Publisher

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

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

def chart_data(request):
    #qs = Book.objects.aggregate(Count('title'))
    data = []

    all_books = len(Book.objects.all())
    all_book_titles = len(BookTitle.objects.all())
    data.append(
        {
            'labels':['books','books titles'],
            'data':[all_books,all_book_titles],
            'description':'unique book title vs books',
            'type':'bar'
        }
    )

    titles_by_publisher = BookTitle.objects.values('publisher__name').annotate(Count('publisher__name'))

    publisher_name = [x['publisher__name'] for x in titles_by_publisher]
    publisher_name_count = [x['publisher__name__count'] for x in titles_by_publisher]
    
    
    data.append({
        'labels' : publisher_name,
        'data':publisher_name_count,
        'description':'book title count by publisher',
        'type':'pie'
    })


    # book by status pie
    book_by_status = Rental.objects.values('status').annotate(Count('book__title'))
    book_title_count = [x['book__title__count'] for x in book_by_status]
    status_keys = [x['status'] for x in book_by_status]
    status = [dict(STATUS_CHOICES)[key] for key in status_keys]
    
    data.append({
        'labels' : status,
        'data':book_title_count,
        'description':'book title count by status',
        'type':'pie'
    })

    #publisher vs customers (bar)

    customers = len(Customer.objects.all())
    publishers = len(Publisher.objects.all())
    data.append({
        'labels' : ['customers', 'publishers'],
        'data':[customers,publishers],
        'description':'publisher vs customers count',
        'type':'bar'
    })

    return JsonResponse({'data':data})

def home_view(request):
    qs = Customer.objects.all()
    book = BookTitle.objects.get(id=1)
    context = {
        'qs': qs, 
        'book': book
        }
    return render(request, 'main.html', context )