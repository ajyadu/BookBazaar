from django.urls import path
from .import views as v

app_name="order"
urlpatterns=[
    path("chackout",v.checkout,name="checkout"),
    path("history",v.order_history,name="history"),
    path("<int:pk>/",v.order_detail,name="detail"),
    path("orderlistcreate",v.OrderListCreate.as_view()),
    path("orderRUD/<int:pk>",v.OrderRUD.as_view(),),
    path("orderitemlistcreate",v.OrderItemListCreate.as_view()),
    path("orderitemRUD/<int:pk>",v.OrderItemRUD.as_view()),

]