from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView 
from book.models import Book
from cart.serializers import CartItemSerializer, CartSerializer
from .models import Cart, CartItem


@login_required(login_url="accounts:login")
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    return render(
        request,
        "cart.html",
        {
            "cart": cart
        }
    )


@login_required(login_url="account:login")
def add_to_cart(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    # Check stock
    if book.stock <= 0:
        messages.error(request, "This book is out of stock.")
        return redirect("books:book_detail", pk=book.id)

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book
    )

    if created:
        cart_item.quantity = 1
    else:
        if cart_item.quantity < book.stock:
            cart_item.quantity += 1
        else:
            messages.warning(
                request,
                "You cannot add more than available stock."
            )

    cart_item.save()

    messages.success(
        request,
        f"{book.title} added to your cart."
    )

    return redirect("cart:cart")


@login_required(login_url="account:login")
def update_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if request.method == "POST":

        quantity = int(
            request.POST.get("quantity", 1)
        )

        if quantity <= 0:
            item.delete()

        elif quantity <= item.book.stock:
            item.quantity = quantity
            item.save()

        else:
            messages.error(
                request,
                f"Only {item.book.stock} copies are available."
            )

    return redirect("cart:cart")


@login_required(login_url="account:login")
def remove_from_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.delete()

    messages.success(
        request,
        "Book removed from cart."
    )

    return redirect("cart:cart")



class CartListCreate(ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user) 


class CartRUD(RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CartItemListCreate(ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return self.queryset.filter(cart__user=self.request.user)




class CartItemRUD(RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return self.queryset.filter(cart__user=self.request.user)   



    
    