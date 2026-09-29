from django.contrib import admin
from .models import Book,BookView

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=("title","author","category","price","stock","isbn")
    list_filter=("category",)
    search_fields=("title","author","isbn")
    list_editable=("price","stock")



@admin.register(BookView)
class BookViewAdmin(admin.ModelAdmin):
    list_display=("user","book","viewed_at")
    list_filter=("book__category",)
    search_fields=("user_username","book__title")