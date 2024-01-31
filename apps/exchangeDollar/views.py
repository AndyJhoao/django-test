import requests 
from django.conf import settings
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from rest_framework import permissions, authentication
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from datetime import datetime, timedelta
from decimal import Decimal
from .models import ExchangeRate
import base64

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
# from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm

def validateUser(request):
    authorization_header = request.headers.get('Authorization')
    
    if not authorization_header or not authorization_header.startswith('Basic '):
        return {'error': 'No se ingreso la autenticacion', 'status': 404}

    encoded_credentials = authorization_header[len('Basic '):]
    credentials = base64.b64decode(encoded_credentials).decode('utf-8')

    username, password = credentials.split(':', 1)

    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return {'error': 'No se encontro el usuario', 'status': 401}

    if not user.check_password(password):
        return {'error': 'No es valida la contraseña', 'status': 401}

    corredores_group = Group.objects.get(name='corredor')
    valid = corredores_group in user.groups.all()
    if valid:
        return{'error': None, 'status': 200}
    else:
        return {'error': 'No es valida la contraseña', 'status': 401}

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([authentication.BasicAuthentication])
def mxn2usd(request):
    auth = validateUser(request)
    if auth['status'] == 200:
        exchanges = ExchangeRate.objects.values('mxn_to_usd', 'date')
        data = list(exchanges)
        data_fix = [{'fecha': d.pop('date'), **d} for d in data]
        return JsonResponse({'error': 'ninguno', 'status': 200, 'data': data_fix}, safe=False)
    else:
        return JsonResponse({'error': auth['error'], 'status': auth['status']}, safe=False)
    
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([authentication.BasicAuthentication])
def usd2mxn(request):
    auth = validateUser(request)
    if auth['status'] == 200:
        exchanges = ExchangeRate.objects.values('usd_to_mxn', 'date')
        data = list(exchanges)
        data_fix = [{'fecha': d.pop('date'), **d} for d in data]
        return JsonResponse({'error': 'ninguno', 'status': 200, 'data': data_fix}, safe=False)
    else:
        return JsonResponse({'error':  auth['error'], 'status': auth['status']}, safe=False)
    
def consumirApi(request):
    url = settings.URL_API
    fecha = datetime.now().date()
    fecha_ten_days_ago = fecha - timedelta(days=10)

    params = {'token':settings.TOKEN_API}

    try:
        response = requests.get(f'{url}/datos/{fecha_ten_days_ago}/{fecha}',params=params)

        if response.status_code == 200 :
            data = response.json()
            exchanges = [ExchangeRate(date=datetime.strptime(exchange['fecha'], "%d/%m/%Y").date(), usd_to_mxn=exchange['dato'], mxn_to_usd=1 / Decimal(exchange['dato'])) for exchange in data['bmx']['series'][0]['datos']]
            ExchangeRate.objects.bulk_create(exchanges)

            return JsonResponse({'error': 'ninguno', 'status': 200 }, safe=False)
        else:
            return JsonResponse({'error': f'Error en la solicitud. Codigo {response.status_code}'}, status=500, safe=False)
    except requests.exceptions.RequestException as error:
        return JsonResponse({'error': f'Error en la solicitud: {str(error)}'}, status=500, safe=False)
    
def home(request):
    if request.method == "GET":
        return render(request,'home.html',{
            'form': AuthenticationForm
        })
    elif request.method == "POST":
        return redirect(request.POST.get('convert_to'))
        


