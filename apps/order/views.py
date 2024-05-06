from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import View, ListView
from django.contrib import messages
from django.db import transaction

from .models import Cart, Order, OrderProduct
from .forms import CartForm, OrderForm



def get_cart_data(user):
    cart = Cart.objects.filter(user=user).prefetch_related('product').prefetch_related('product__images')
    total_price = sum([item.get_total() for item in cart])
    return {'cart': cart, 'total_price': total_price}

class CartAddHandler(View):
    def post(self, request):
        form = CartForm(request.POST)
        if form.is_valid():
            cart = form.save(commit=False)
            cart_item = Cart.objects.filter(product=cart.product, user=request.user).first()
            if cart_item:
                cart_item.quantity = cart.quantity
                cart_item.save()    
                messages.success(request, 'Кількість товару змінено')
            else:
                cart.user = request.user
                cart.save()
                messages.success(request, 'Товар додано до кошика')
        else:
            messages.error(request, f'Помилка додавання товару до кошика {form.errors}')
        return redirect('order:cart')

        

class CartHandler(ListView):
    model = Cart
    template_name = 'order/cart.html'
    context_object_name = 'cart'
    
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['get_total_cost'] = sum([item.get_total() for item in context['cart']])
        return context
    
    
class CartDeleteHandler(View):
    def get(self, request, pk):
        cart = Cart.objects.get(pk=pk, user=request.user)
        cart.delete()
        messages.success(request, 'Товар видалено з кошика')
        return redirect('order:cart')

class CartClearHandler(View):
    def get(self, request):
        Cart.objects.filter(user=request.user).delete()
        messages.success(request, 'Кошик очищено')
        return redirect('order:cart')
    
    
class CheckoutHandler(View):
    def get(self, request):
        cart = Cart.objects.filter(user=request.user).order_by('product__price')
        total_cost = sum([item.get_total() for item in cart])
        form = OrderForm()
        return render(request, 'order/order_create.html', {'cart': cart, 'total_cost': total_cost})
    
    def post(self, request):
        form = OrderForm(request.POST)
        cart_data = get_cart_data(request.user)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart_data.get('total_price', 99999)
            
            
            #Очищаємо корзину і добавляємо товари в замовлення в одній транзакції
            #транзакція - це група дій, які виконуються як одна атомарна одиниця
            with transaction.atomic():
                order.save()
                for item in cart_data.get('cart'):
                    order_product = OrderProduct(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price
                    )
                    order_product.save()
                    item.product.quantity -= item.quantity
                    item.product.save()
                Cart.objects.filter(user=request.user).delete()
                    
            messages.success(request, 'Замовлення створено')
            return redirect('order:complete', order_id=order.id)
        else:
            
            messages.error(request, f'Помилка створення замовлення ')
            return render(request, 'order/order_create.html', {'cart': cart_data.get('cart'), 'total_cost': cart_data.get('total_price'), 'form': form})    
        
        
class OrderCompleteHandler(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        return render(request, 'order/order_complete.html', {'order': order})