from django.contrib import admin
from .models import ExchangeRate
from django import forms

class ExchangeRateAdminForm(forms.ModelForm):
    class Meta:
        model= ExchangeRate
        fields = ['date','usd_to_mxn','mxn_to_usd']

class ExchangeRateAdmin(admin.ModelAdmin):
    form = ExchangeRateAdminForm
    list_display = ['date','usd_to_mxn','mxn_to_usd']

admin.site.register(ExchangeRate,ExchangeRateAdmin)
