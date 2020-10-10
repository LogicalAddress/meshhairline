from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
import requests
import os
from common.models import WebsiteSettings

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
    paymentSessionId = request.GET['sessionId']
    data = {
        'paymentSessionId': paymentSessionId,
        'state': 'processed',
        'transactionId': request.POST.get('requestId'),
        'instructions': 'Your payment will appear on your statement in the coming days',
        'links': {
            'refunds': 'https://meshhairline.com/custom-refund?transactionId=' + request.POST.get('requestId')
        },
    }
    url = os.environ.get('SNIPCART_PAYMENT_URL', 'https://payment.snipcart.com') + '/api/private/custom-payment-gateway/payment'
    settings = WebsiteSettings.objects.filter()[0]
    print("testing...")
    print(settings)
    headers = {'Authorization': 'Bearer ' + settings.snipcart_private_key}
    req = requests.post(url, data=data, headers=headers)
    if req.status_code == 200:
        res = req.json()
        return JSONResponse({
            'returnUrl': res['returnUrl']
        }, status=200)
    else:
        return JSONResponse(None, status=500)

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
