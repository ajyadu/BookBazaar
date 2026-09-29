from django.urls import path
from . import views as v

app_name="book"
urlpatterns = [
    path('',v.home, name='home'),
    path('book', v.book_list, name='book_list'),
    path('book/<int:pk>/', v.book_detail, name='book_detail'),
    path("booklistcreate",v.BookListCreateAPIView.as_view()),
    path("bookrud/<int:pk>/", v.BookRUDAPIView.as_view()),
    path("bookviewlistcreate", v.BookViewListCreateAPIView.as_view()),
    path("bookviewrud/<int:pk>/", v.BookViewRUDAPIView.as_view()),
    ]