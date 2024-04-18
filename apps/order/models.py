from django.db import models

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
        
    