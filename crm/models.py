from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # validate phone format in serializer
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    product_ids = models.ManyToManyField(Product, related_name='order_products')
    order_date = models.DateTimeField(auto_now_add=True)

    @property
    def total_amount(self):
        price = 0
        for product in self.product_ids.all():
            price += product.price

        return price