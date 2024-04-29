from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from apps.catalog.models import Product

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f'{self.product.title} - {self.quantity}'
    
    class Meta:
        # unique_together = ['user', 'product']
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        
    def get_total(self):
        return self.product.price * self.quantity
        


class Order(models.Model):
    STATUS_CHOUCES = (
        ('in_progress', 'В обробці'),
        ('sent', 'Відправлено'),
        ('completed', 'Завершено'),
        ('canceled', 'Скасовано')
    )
    
    STATUS_PAID = (
        (True, 'Оплачено'),
        (False, 'Не оплачено')
    )
    
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = PhoneNumberField(verbose_name='Phone')
    email = models.EmailField()
    delivery = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    paid = models.BooleanField(default=False, choices=STATUS_PAID)
    status = models.CharField(max_length=20, choices=STATUS_CHOUCES, default='in_progress')
    
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ('-created_at',)
        
    def __str__(self):
        return f'Order {self.id}'
    
    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products', verbose_name='Order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_products', verbose_name='Product')
    quantity = models.IntegerField(verbose_name='Quantity', default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    
    def __str__(self):
        return f'{self.product.title} - {self.quantity}'
    
    class Meta:
        verbose_name = 'OrderProduct'
        verbose_name_plural = 'OrderProducts'
        
    def get_total(self):
        return self.product.price * self.quantity