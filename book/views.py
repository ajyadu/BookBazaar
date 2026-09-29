from django.shortcuts import render,get_object_or_404
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .serializers import BookSerializer,BookViewSerializer
from book.models import Book,BookView
from django.db.models import Q
from decimal import Decimal,InvalidOperation


# Create your views here.
def home(request):
    book=Book.objects.all().order_by('-created_at')
    return render(request, 'home.html',{"book":book[:8]})

def book_list(request):
    book= Book.objects.all().order_by('-created_at')
    q =request.GET.get("q","").strip()
    category = request.GET.get("category","").strip()
    min_price= request.GET.get("min_price","").strip()
    max_price=request.GET.get("max_price","").strip()

    if q:
        book = book.filter(Q(title__icontains=q) | Q(author__icontains=q) | Q(isbn__icontains=q))
    if category:
        book=book.filter(category=category)

    if min_price:
        try:
            book=book.filter(price__gte=Decimal(min_price))
        except InvalidOperation:
            pass  
    if max_price:
            try:
                book=book.filter(price__lte=Decimal(max_price))
            except InvalidOperation:
                pass                
    return render(request, 'book_list.html', {
        'books': book,
        "query":q,
        'category':category,
        "min_price":min_price,
        "max_price":max_price,

     })

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    recommendations=Book.objects.filter(category=book.category).exclude(pk=book.pk)[:4]
    if request.user.is_authenticated:
        BookView.objects.update_or_create(
            user=request.user,
            book=book,
            defaults={},
         )

    return render(request, 'book_detail.html', {'book': book,"recommendations":recommendations,})



class BookListCreateAPIView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer



class BookRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewListCreateAPIView(ListCreateAPIView):
    queryset = BookView.objects.all()
    serializer_class = BookViewSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)



class BookViewRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = BookView.objects.all()
    serializer_class = BookViewSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


    