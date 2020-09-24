from django.shortcuts import render
from django.shortcuts import redirect

def switch_currency(request):
    if request.method == 'POST':
        pass
    currency = request.GET['currency']
    request.session['currency'] = currency
    return redirect(request.META.HTTP_REFERER)