from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import Sum

class BaseModel(models.Model):
    uid = models.UUIDField(default = uuid.uuid4, editable = False, primary_key = True)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now_add = True)

    class Meta:
        abstract = True


class FoodCategory(BaseModel):
    category_name = models.CharField(max_length = 100)

    def __str__(self) -> str:
        return self.category_name


class Food(BaseModel):
    category = models.ForeignKey(FoodCategory, on_delete = models.CASCADE, related_name = 'food')
    food_name = models.CharField(max_length =  100)
    price = models.IntegerField(default = 100)
    image = models.ImageField(upload_to = 'food')

    def __str__(self) -> str:
        return self.food_name

class Cart(BaseModel):
    user = models.ForeignKey(User, null = True, blank = True, on_delete = models.SET_NULL, related_name = "cart")
    is_paid = models.BooleanField(default = False)

    def order_total(self):
        return CartItems.objects.filter(cart = self).aggregate(Sum('food__price'))['food__price__sum']



class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, related_name = "cart_items")
    food = models.ForeignKey(Food, on_delete = models.CASCADE)