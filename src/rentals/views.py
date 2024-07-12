from django.shortcuts import render
from .forms import SearchBookForm
from books.models import Book
# Create your views here.
def search_book_view (request):
    form= SearchBookForm(request.POST or None)
    search_query = request.POST.get('search', None)
    book_ex = Book.objects.filter(isbn = search_query).exists()

    if search_query != None and book_ex:
        pass

    context = {'form': form}

    return render(request, 'rentals/main.html', context)