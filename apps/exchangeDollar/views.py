import requests 
from django.conf import settings
from django.http import JsonResponse
from datetime import datetime, timedelta

# def mxn2usd(request):
    # importar el serializer para manipular la bd
    
# def usd2mxn(request):
    # importar el serializer para manipular la bd
    
def consumirApi(request):
    url = settings.URL_API
    fecha = datetime.now().date()
    fecha_ten_days_ago = fecha - timedelta(days=10)

    params = {'token':settings.TOKEN_API}

    try:
        response = requests.get(f'{url}/datos/{fecha_ten_days_ago}/{fecha}',params=params)

        if(response.status_code == 200):
            data = response.json()
            # importar data en BD
            return JsonResponse(data)
        else:
            return JsonResponse({'error': f'Error en la solicitud. Codigo {response.status_code}'}, status=500)
    except requests.exceptions.RequestException as error:
        return JsonResponse({'error': f'Error en la solicitud: {str(error)}'}, status=500)
    

