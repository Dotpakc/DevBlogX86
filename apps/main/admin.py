from django.contrib import admin

# Register your models here.
from .models import Page

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'sort')
    list_editable = ('sort',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}