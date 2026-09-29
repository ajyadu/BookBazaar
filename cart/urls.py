from django.urls import path
from . import views as v

app_name="cart"
urlpatterns=[
    path("",v.cart_view,name="cart"),
    path("add/<int:book_id>/",v.add_to_cart,name="add"),
    path("update/<int:item_id>/",v.update_cart,name="update"),
    path("remove/<int:item_id>/",v.remove_from_cart,name="remove"),
    path("cartlistcreate",v.CartListCreate.as_view()),
    path("cartRUD/<int:pk>",v.CartRUD.as_view()),
    path("cartitemlistcreate",v.CartItemListCreate.as_view()),
    path("cartitemRUD/<int:pk>",v.CartItemRUD.as_view()),
]