import django.forms as forms

class SearchBookForm(forms.Form):
    search = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'search by book id ...'}))