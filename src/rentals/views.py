from typing import Any
from django.shortcuts import render
from .forms import SearchBookForm
from django.views.generic import ListView, UpdateView, CreateView
from books.models import Book
from .models import Rental
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q

from django.contrib import messages
from datetime import datetime

# Create your views here.
def search_book_view (request):
    form= SearchBookForm(request.POST or None)
    search_query = request.POST.get('search', None)
    book_ex = Book.objects.filter(Q(isbn=search_query) | Q(id=search_query)).exists()

    if search_query != None and book_ex:
        return redirect('rentals:detail', search_query)

    context = {'form': form}

    return render(request, 'rentals/main.html', context)


class BookRentalView(ListView):
    model=Rental
    context_object_name = 'rentals'
    template_name = 'rentals/detail.html'
    
    def get_queryset(self):
        # Assuming you have a way to determine the current book (e.g., through URL params)
        book_id = self.kwargs['book_id']  # Example: getting book_id from URL params
        return Rental.objects.filter(Q(book__isbn=book_id) | Q(book__id=book_id))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context= super().get_context_data(**kwargs)
        book_id = self.kwargs['book_id']
        book = Book.objects.filter(Q(isbn=book_id) | Q(id=book_id)).first()
        context['book'] = book  # Add book to context
        return context
    
class UpdateRentalStatus(UpdateView):
    model = Rental
    template_name = 'rentals/update.html'
    fields=('status',)

    def get_success_url(self) -> str:
        book_id = self.kwargs.get('book_id')
        return reverse('rentals:detail', kwargs={'book_id':book_id}) 
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        if instance.status == '#1':
            instance.return_date = datetime.today().date()
            instance.is_closed = True
        instance.save()
        messages.add_message(self.request, messages.INFO, f'Status of book {instance.book_id} was successufully updated')
        return super().form_valid(form)

class CreateNewRental(CreateView):
    model = Rental
    template_name = 'rentals/new.html'
    fields = ('customer',)

    def form_valid(self, form):
        book_id = self.kwargs.get('book_id')  # Get book_id from URL parameters
        print(f"Received Book ID: {book_id}")  # Debugging line
        book = get_object_or_404(Book, id=book_id)  # Fetch the Book instance
        form.instance.book = book  # Assign the Book to the Rental
        return super().form_valid(form)

    def get_success_url(self):
        book_id = self.kwargs.get('book_id')  # Get book_id for the success URL
        return reverse('rentals:detail', kwargs={'book_id': book_id})