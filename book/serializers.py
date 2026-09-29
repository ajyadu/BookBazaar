from rest_framework import serializers
from .models import Book, BookView


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'price', 'isbn', 'category', 'image', 'stock', 'created_at'] 



class BookViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookView
        fields = ['id', 'book', 'user', 'viewed_at']    

        




