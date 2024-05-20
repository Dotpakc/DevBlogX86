from django.db import models
from django.urls import reverse

from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.
class Page(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=255)
    slug = models.SlugField(verbose_name="URL", max_length=255, unique=True)
    content = CKEditor5Field('Текст', config_name='extends')
    
    sort = models.IntegerField(verbose_name="Сортировка", default=0)
    
    
    class Meta:
        ordering = ['-sort']
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        
    def get_absolute_url(self):
        return reverse('main:page', kwargs={'slug': self.slug})