from django.db import models

class ExchangeRate (models.Model):
    date: models.DateField(null=True)
    usd_to_mxn: models.DecimalField(max_digits=10, default=0)
    mxn_to_usd: models.DecimalField(max_digits=10, default=0)

    def __str__(self):
        return f"${self.usd_to_mxn}mxn - ${self.mxn_to_usd}"

# Create your models here.
