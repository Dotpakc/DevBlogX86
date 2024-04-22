from django.shortcuts import render, redirect

from django.views.generic import View

from .forms import CartForm

class CartHandler(View):
    def post(self, request):
        form = CartForm(request.POST)
        if form.is_valid():
            cart = form.save(commit=False)
            cart.user = request.user
            cart.save()
            return redirect('main:index')
        