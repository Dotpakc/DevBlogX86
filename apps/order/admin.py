from django.contrib import admin

# Register your models here.
from .models import Cart, Order, OrderProduct

admin.site.register(Cart)


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'phone', 'delivery', 'address', 'paid', 'status')
    list_filter = ('status', 'delivery', 'paid')
    search_fields = ('first_name', 'last_name', 'phone', 'email', 'address','id')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status', 'paid')
    
    fieldsets = (
        ('Basic', {
            'fields': ('user', 'first_name', 'last_name', 'phone', 'email', 'delivery', 'address')
        }),
        ('Status', {
            'fields': ('paid', 'status')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        })
    )
    ordering = ('-created_at',)
    inlines = (OrderProductInline,)