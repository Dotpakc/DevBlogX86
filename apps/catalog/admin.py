from django.contrib import admin

from .models import Category, Product, Image, ProductCategory
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    

class ProductCategoryInline(admin.TabularInline):
    model = ProductCategory
    extra = 1
    
class ImageInline(admin.TabularInline):
    model = Image
    fields = ('image_tag','product', 'image', 'is_main'),
    readonly_fields = ('image_tag',)
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'quantity', 'price', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'category', 'quantity')
    search_fields = ('title', 'description')
    list_editable = ('quantity', 'price')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductCategoryInline, ImageInline]