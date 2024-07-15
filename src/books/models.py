from typing import Iterable
import uuid
from django.db import models
from publishers.models import Publisher
from authors.models import Author
from rentals.choices import STATUS_CHOICES
from .utils import hash_book_info

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
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    title = models.ForeignKey(BookTitle, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=64, blank=True)
    #qr_code
    # upload_to - where to save files
    # null - this field can be empty
    # for ImageField we need to install pillow
    qr_code = models.ImageField(upload_to='qr_code', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    @property
    def status(self):
        if len(self.rental_set.all()) > 0:
            statuses = dict(STATUS_CHOICES)
            return statuses[self.rental_set.first().status]
        #there is no rentals then false
        return False
    
    @property
    def rental_id(self):
        if len(self.rental_set.all()) > 0:
            return self.rental_set.first().id
        #there is no rentals then false
        return None

    @property 
    def is_available(self):
        if len(self.rental_set.all()) > 0:
            status = self.rental_set.first().status
            return True if status == '#1' else False
        return True

    def get_absolute_url(self):
        letter = self.title.title[:1].lower()
        return reverse("books:detail-book", kwargs={"letter":letter,"slug": self.title.slug, "book_id":self.id})

    def delete_object(self):
        letter = self.title.title[:1].lower()
        return reverse('books:delete-book', kwargs={'letter':letter,'slug': self.title.slug, 'book_id':self.id})
    
    def __str__(self) :
        return str(self.title)
    
    def save(self, *args, **kwargs):
        # generate id
        if not self.isbn:
            self.isbn = hash_book_info(self.title,self.title.publisher.name)

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
