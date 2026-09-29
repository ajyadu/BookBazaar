from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model=Book
        fileds=["title","author","description","price","isbn","category","image","stock"]