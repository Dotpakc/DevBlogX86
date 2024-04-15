import uuid

from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.admin import display

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill, ResizeToCover

from django_ckeditor_5.fields import CKEditor5Field

from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=255, verbose_name='Назва')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')
    description = models.TextField(verbose_name='Опис', blank=True, null=True)
    
    image = ProcessedImageField(
        verbose_name='Зображення',
        upload_to='categories/',
        processors=[ResizeToFit(820, 440)],
        format='WEBP',
        options={'quality': 90},
        blank=True,
        null=True
    )
    parent = TreeForeignKey(
        to = 'self',
        on_delete = models.CASCADE,
        related_name = 'children',
        blank = True,
        null = True,
    )
    

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['title']

    def __str__(self):
        full_path = [self.title]
        parent = self.parent
        while parent is not None:
            full_path.append(parent.title)
            parent = parent.parent
        return ' -> '.join(full_path[::-1])       
        
        
class Product(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    
    title = models.CharField(max_length=255, verbose_name='Назва')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')
    description = CKEditor5Field(verbose_name='Опис', blank=True, null=True)
    
    quantity = models.PositiveIntegerField(verbose_name='Кількість', default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    
    category = models.ManyToManyField(
        to = Category,
        related_name = 'products',
        through='ProductCategory', # це модель проміжного зв'язку
        verbose_name = 'Категорії',
        blank=True,
    )
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    def main_image(self):
        main_image = self.images.filter(is_main=True).first()
        if main_image:
            return main_image
        return self.images.first()
    
    def main_category(self):
        main_category = self.category.filter(productcategory__is_main=True).first()
        if main_category:
            return main_category
        return self.category.first()
    
    
class ProductCategory(models.Model):
    product = models.ForeignKey(
        to = Product,
        on_delete = models.CASCADE,
    )
    
    category = models.ForeignKey(
        to = Category,
        on_delete = models.CASCADE,
    )
    
    is_main = models.BooleanField(default=False, verbose_name='Основна категорія')
    
    
    class Meta:
        verbose_name = 'Категорія товару'
        verbose_name_plural = 'Категорії товарів'
        unique_together = ['product', 'category']
        
    def __str__(self):
        return f'{self.product.title} - {self.category.title}'
    
    def save(self, *args, **kwargs):
        if self.is_main:
            ProductCategory.objects.filter(product=self.product).update(is_main=False)
        super().save(*args, **kwargs)


def get_image_path(instance, filename):
    return f'products/{instance.product.id}/{filename}'    
    
class Image(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    
    image = ProcessedImageField(
        verbose_name='Зображення',
        upload_to=get_image_path,
        processors=[],
        format='WEBP',
        options={'quality': 90},
    )
    
    thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToCover(300, 300)],
        format='WEBP',
        options={'quality': 50},
    )

    product = models.ForeignKey(
        to = Product,
        on_delete = models.CASCADE,
        related_name = 'images',
        verbose_name = 'Товар',
    )
    
    is_main = models.BooleanField(default=False, verbose_name='Основне зображення')
    
    def save(self, *args, **kwargs):
        if self.is_main:
            Image.objects.filter(product=self.product).update(is_main=False)
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = 'Зображення'
        verbose_name_plural = 'Зображення'
        ordering = ['product', '-is_main']
        
    def __str__(self):
        return self.product.title
    
    @display(description='Зображення')
    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" height="100" />')