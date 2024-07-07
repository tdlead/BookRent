from django.shortcuts import render

from .models import BookTitle

from django.views.generic import ListView

from django.views.generic import FormView
from .forms import BookTitleForm

from django.urls import reverse_lazy
# Create your views here.

# def book_title_list_view(request):
#     books = BookTitle.objects.all()
#     return render(request,'books/main.html', {'books' : books})

class BookTitleListView(ListView,FormView):
    # we have defaults, and one of the defaults is template name
    # will look for template which is mode
    model=BookTitle
    # Overrite the query set 
    # queryset = BookTitle.objects.all().order_by('-created')
    #ordering = ('-created')
    template_name='books/main.html'
    context_object_name = 'books'
    form_class = BookTitleForm
    
    # model_list.html -> booktitle_list.html 
    # object_list

    def get_queryset(self):
        parameter = 's'
        return BookTitle.objects.filter(title__startswith=parameter)


def book_title_detail_view(request, pk):
    book_details = BookTitle.objects.get(pk=pk)
    return render(request, 'books/detail.html', {'book_details':book_details})


""" with slug
def book_title_detail_view(request, **kwargs):
    slug = kwargs.get('slug')
"""
