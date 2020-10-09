from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
import requests
import os

class JSONResponse(HttpResponse):
	"""An HttpResponse that renders its content into JSON."""
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

@login_required
def twoCheckoutCo(request):
    context = None
    return render(request, 'shop/custom-payment.html', context)


def customConfirmPayment(request):
    pass


def customPaymentSession(request):
    publicToken = request.GET['publicToken']
    url = os.environ.get('SNIPCART_PAYMENT_URL', 'https://payment.snipcart.com') + '/api/public/custom-payment-gateway/payment-session?publicToken=' + publicToken
    # headers = {'authorization': SECRET_KEY}
    req = requests.get(url, headers=None)
    if req.status_code == 200:
        res = req.json()
        return JSONResponse(res, status=200)
    else:
        return JSONResponse(None, status=500)
