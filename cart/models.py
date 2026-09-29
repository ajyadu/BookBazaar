from django.db import models
from django.contrib.auth.models import User
from book.models import Book


# Create your models here.

class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    created_at=models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.subtotal()for item in self.items.select_related("book").all())

    def __str__(self):
        return f"cart - {self.user.username}"

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="items")
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)


    class Meta:
        unique_together = ("cart","book")

    def subtotal(self):
        return self.book.price * self.quantity    


    def __str__(self):
        return f"{self.book.title} X {self.quantity}"
    