from django.urls import path
from . import views

urlpatterns = [
    path('usd2mxn/', views.usd2mxn, name='usd2mxn'),
    path('mxn2usd/', views.mxn2usd, name='mxn2usd'),
    path('consumirApi/', views.consumirApi, name='consumirApi'),
    path('', views.home, name='home')
]