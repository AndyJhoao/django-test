import requests 
from django.conf import settings
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import ExchangeRate

def mxn2usd(request):
    exchanges = ExchangeRate.objects.values('mxn_to_usd', 'date')
    data = list(exchanges)
    data_fix = [{'fecha': d.pop('date'), **d} for d in data]
    return JsonResponse({'error': 'ninguno', 'status': 200, 'data': data_fix}, safe=False)

def usd2mxn(request):
    exchanges = ExchangeRate.objects.values('usd_to_mxn', 'date')
    data = list(exchanges)
    data_fix = [{'fecha': d.pop('date'), **d} for d in data]
    return JsonResponse({'error': 'ninguno', 'status': 200, 'data': data_fix}, safe=False)

def consumirApi(request):
    url = settings.URL_API
    fecha = datetime.now().date()
    fecha_ten_days_ago = fecha - timedelta(days=10)

    params = {'token':settings.TOKEN_API}

    try:
        response = requests.get(f'{url}/datos/{fecha_ten_days_ago}/{fecha}',params=params)

        if(response.status_code == 200):
            data = response.json()
            exchanges = [ExchangeRate(date=datetime.strptime(exchange['fecha'], "%d/%m/%Y").date(), usd_to_mxn=exchange['dato'], mxn_to_usd=1 / exchange['dato']) for exchange in data['bmx']['series'][0]['datos']]
            ExchangeRate.objects.bulk_create(exchanges)

            return JsonResponse({'error': 'ninguno', 'status': 200 }, safe=False)
        else:
            return JsonResponse({'error': f'Error en la solicitud. Codigo {response.status_code}'}, status=500, safe=False)
    except requests.exceptions.RequestException as error:
        return JsonResponse({'error': f'Error en la solicitud: {str(error)}'}, status=500, safe=False)
    

