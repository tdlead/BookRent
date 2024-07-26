from django.shortcuts import render, get_object_or_404, redirect
from customers.models import Customer
from books.models import Book, BookTitle
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView
from django.db.models import Count,Sum

from rentals.models import Rental
from rentals.choices import STATUS_CHOICES
from publishers.models import Publisher

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import LoginForm, OTPForm
from .utils import send_otp, is_ajax
from datetime import datetime
import pyotp
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required

def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST': 
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                send_otp(request)
                request.session['username'] = username
                return redirect('otp')
            else:
                messages.add_message(request, messages.ERROR, 'Invalid username or password')
    context = {
        'form':form
    }
    return render(request, 'login.html', context)

def otp_view(request):
    error_message= None
    form = OTPForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            username = request.session.get('username')
            otp_secret_key = request.session.get('otp_secret_key')
            otp_valid_until = request.session.get('otp_valid_date')
            
            if otp_secret_key and otp_valid_until:
                valid_until = datetime.fromisoformat(otp_valid_until)
                if valid_until > datetime.now():
                    totp = pyotp.TOTP(otp_secret_key, interval=60)
                    if totp.verify(otp):
                        user = get_object_or_404(User, username=username)
                        login(request, user)
                        del request.session['otp_secret_key']
                        del request.session['otp_valid_date']
                        return redirect('home')
                    else:
                        error_message = 'Invalid one-time password'
                else: 
                    error_message = 'Once time password has expired'
            else: 
                error_message = 'Oops something went wrong :('
    if error_message : messages.add_message(request, messages.ERROR, error_message)

    context = {'form': form}

    return render(request, 'otp.html', context)

@login_required                                     
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

class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard.html'

class AboutView(LoginRequiredMixin, TemplateView):
    template_name = 'about.html'
    

@login_required
def chart_data(request, ):
    if not is_ajax(request):
        return redirect('home')
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