# forms.py
from django import forms
from .models import BookTitle
from django.core.exceptions import ValidationError

class BookTitleForm(forms.ModelForm):
    class Meta:
        model = BookTitle
        fields = ('title','publisher', 'author')


    def clean(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5: 
            self.add_error('title', 'the title is too short')
            #raise ValidationError('the title is too short')
        
        book_title_exists = BookTitle.objects.filter(title__iexact = title).exists()

        if book_title_exists:
            self.add_error('title', 'the book already exists' )

        return self.cleaned_data
