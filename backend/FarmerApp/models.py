from django.db import models
from django.conf import settings

class productModel(models.Model):

    farmer_id= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # product_img = models.ImageField(upload_to="produt_photos")
    name = models.CharField(max_length =100)
    category = models.CharField (max_length = 255)
    price_per_unit = models.IntegerField()
    available_quantity = models.IntegerField()
    unit_type = models.CharField(max_length=20)

    QUALITY_CHOICES = [
        ('A', '5'),
        ('B', '4'),
        ('C', '3'),
        ('D', '2'),
        ('E', '1'),
    ]
    quality_grade = models.CharField(
        max_length=20,
        choices=QUALITY_CHOICES
    )
    harvest_date = models.DateField()
    description = models.CharField(max_length=500)
    location = models.CharField(max_length=100)
    delivery_option = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(productModel, on_delete=models.CASCADE, related_name="images")
    product_img = models.ImageField(upload_to="products/")

# class Order(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     buyer = models.ForeignKey(User, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=50, default="pending")
#     created_at = models.DateTimeField(auto_now_add=True)





# buyerrr=====
from django.contrib.auth.models import User
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(productModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(productModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product') 

