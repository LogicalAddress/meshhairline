from django.shortcuts import render
from django.shortcuts import redirect
from shop.cart.cart import Cart

def switch_currency(request):
    if request.method == 'POST':
        pass
    cart = Cart(request.session)
    cart.clear()
    currency = request.GET['currency']
    request.session['currency'] = currency
    return redirect('/')