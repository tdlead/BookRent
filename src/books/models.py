from typing import Iterable
import uuid
from django.db import models
from publishers.models import Publisher
from authors.models import Author

# qr code
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image 


from django.urls import reverse
# to create a slug need to import
from django.utils.text import slugify

# Create your models here.
class BookTitle(models.Model):
    # information
    title = models.CharField(max_length=200, unique=True)
    # slug Harry Potter -> harry_potter
    slug = models.SlugField(blank=True)
    # cascade - whenerver the publisher gets deleted, the book will be deleted as well
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def books(self):
        return self.book_set.all()

    def get_absolute_url(self):
        letter = self.title[:1].lower()
        return reverse("books:detail", kwargs={"letter":letter,"slug": self.slug})

    def __str__(self) :
        return str(self.title)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args,**kwargs)


class Book(models.Model):
    title = models.ForeignKey(BookTitle, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=24, blank=True, unique=True)
    #qr_code
    # upload_to - where to save files
    # null - this field can be empty
    # for ImageField we need to install pillow
    qr_code = models.ImageField(upload_to='qr_code', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) :
        return str(self.title)
    
    def save(self, *args, **kwargs):
        # generate id
        if not self.isbn:
            self.isbn = str(uuid.uuid4()).replace('-','')[:24].lower()

        # generate qr_code
        qrcode_image = qrcode.make(self.isbn)

        # parameters: mode, size, background color
        canvas = Image.new('RGB', (qrcode_image.pixel_size, qrcode_image.pixel_size), 'white')

        # insert qr_code
        canvas.paste(qrcode_image)
        # name 
        fname= f'qr_code-{self.isbn}.png'

        buffer = BytesIO()

        canvas.save(buffer, 'PNG')

        self.qr_code.save(fname, File(buffer), save=False)

        canvas.close()
        
        super().save(*args,**kwargs)
