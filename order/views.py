from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from cart.models import Cart
from .models import Order, OrderItem

@login_required(login_url="account:login")
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = list(cart.items.select_related("book"))
    if not items:
        messages.warning(request, "Your cart is empty.")
        return redirect("cart:cart")

    for item in items:
        if item.quantity > item.book.stock:
            messages.error(request, f"Not enough stock for {item.book.title}.")
            return redirect("cart:cart")

    total = cart.total()

    if request.method == "POST":
        with transaction.atomic():
            order = Order.objects.create(user=request.user, total_price=total)
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    book=item.book,
                    quantity=item.quantity,
                    price=item.book.price,
                )
                item.book.stock -= item.quantity
                item.book.save(update_fields=["stock"])
            cart.items.all().delete()
        messages.success(request, f"Order #{order.pk} placed successfully.")
        return redirect("order:detail", pk=order.pk)

    return render(request, "checkout.html", {"cart": cart, "total": total})

@login_required(login_url="account:login")
def order_history(request):
    orders = request.user.orders.prefetch_related("items__book")
    return render(request, "order_history.html", {"orders": orders})

@login_required(login_url="account:login")
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
   
    return render(request, "order_detail.html", {"order": order})



from django.shortcuts import render,redirect
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .serializers import OrderSerializer , OrderItemSerializer


class OrderListCreate(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class=OrderSerializer

class OrderRUD(RetrieveUpdateDestroyAPIView):
    queryset =Order.objects.all()
    serializer_class=OrderSerializer

class OrderItemListCreate(ListCreateAPIView):
    queryset=OrderItem.objects.all()
    serializer_class=OrderItemSerializer


class OrderItemRUD(RetrieveUpdateDestroyAPIView):
    queryset=OrderItem.objects.all()
    serializer_class=OrderItemSerializer





