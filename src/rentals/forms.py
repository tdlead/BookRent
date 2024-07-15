import django.forms as forms
from .choices import FORMAT_CHOICES


class SearchBookForm(forms.Form):
    search = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'search by book id ...'}))

class SelectExportOptions(forms.Form):
    format = forms.ChoiceField(choices=FORMAT_CHOICES, widget=forms.RadioSelect())