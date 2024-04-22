from django.shortcuts import render, redirect

from django.views.generic import View, ListView
from django.contrib import messages

from .models import Cart
from .forms import CartForm

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
    