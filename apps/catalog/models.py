import uuid

from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=255, verbose_name='Назва')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')
    description = models.TextField(verbose_name='Опис', blank=True, null=True)
    
    image = ProcessedImageField(
        verbose_name='Зображення',
        upload_to='categories/',
        processors=[ResizeToFill(820, 440)],
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
        