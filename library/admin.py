from django.contrib import admin
from .models import BookType,Book,Review


# Register your models here.
admin.site.register(BookType)
admin.site.register(Book)
admin.site.register(Review)