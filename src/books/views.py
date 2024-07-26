from django.shortcuts import render, get_object_or_404

from .models import BookTitle, Book

from django.views.generic import (
    ListView, 
    DetailView,
    FormView,
    DeleteView)

from django.views.generic import FormView
from .forms import BookTitleForm

from django.urls import reverse_lazy, reverse


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

import string
# Create your views here.

# def book_title_list_view(request):
#     books = BookTitle.objects.all()
#     return render(request,'books/main.html', {'books' : books})

class BookTitleListView(LoginRequiredMixin,ListView,FormView):
    # we have defaults, and one of the defaults is template name
    # will look for template which is mode
    model=BookTitle
    # Overrite the query set 
    # queryset = BookTitle.objects.all().order_by('-created')
    #ordering = ('-created')
    template_name='books/main.html'
    context_object_name = 'books'

    #forms
    form_class = BookTitleForm
    success_url = reverse_lazy("books:main")
    
    i_instance = None
    # model_list.html -> booktitle_list.html 
    # object_list

    def form_valid(self,form):
        self.i_instance=form.save()
        messages.add_message(self.request, messages.INFO, f"Book title: {self.i_instance.title} has been created")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        self.object_list = self.get_queryset()
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)
    
    def get_success_url(self):
        return self.request.path

    def get_queryset(self):
        parameter=self.kwargs.get('letter') if self.kwargs.get('letter')!=None else 'a'
        print(f'parameter: {parameter}')
        return BookTitle.objects.filter(title__startswith=parameter)
    
    # Create context
    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        context['letters'] = list(string.ascii_uppercase)
        context['selected_letter'] = self.kwargs.get('letter') if self.kwargs.get('letter')!=None else 'a'
        return context

        
# OPTION 1 - BOOK LIST VIEW + overriding get_queryset 
class BookListView(LoginRequiredMixin, ListView):
    template_name='books/detail.html'
    paginate_by = 2

    def get_queryset(self):
        title_slug = self.kwargs.get('slug')
        # title - foreign key then slug attr __
        return Book.objects.filter(title__slug=title_slug)
    
# OPTION 2 BOOKTITLE DETIAL VIEW + model method
class BookTitleDetailView(LoginRequiredMixin, DetailView):
    template_name = "books/detail.html"
    model=BookTitle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_page"] = reverse('books:main') 
        return context
        

class BookDetailView(LoginRequiredMixin, DetailView):
    model=Book
    template_name="books/detail_book.html"

    def get_object(self):
        id = self.kwargs.get('book_id')
        #obj = Book.objects.get(isbn = id)
        obj = get_object_or_404(Book, id=id)
        return obj
    

class BookDeleteView(LoginRequiredMixin, DeleteView):
    model=Book
    template_name = 'books/confirm_delete.html'

    def get_object(self):
        id = self.kwargs.get('book_id')
        #obj = Book.objects.get(isbn = id)
        obj = get_object_or_404(Book, id=id)
        return obj
    
    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, f"The book with id {self.get_object().id} has been deleted")
        letter = self.kwargs.get('letter')
        slug = self.kwargs.get('slug')
        #return to this url after deleting
        return reverse('books:detail', kwargs={'letter':letter, 'slug': slug})
    


# def book_title_detail_view(request, **kwargs):
#     slug = kwargs.get('slug')
#     book_details = BookTitle.objects.get(slug=slug)
#     return render(request, 'books/detail.html', {'book_details':book_details})


""" with slug
def book_title_detail_view(request, **kwargs):
    slug = kwargs.get('slug')
"""
