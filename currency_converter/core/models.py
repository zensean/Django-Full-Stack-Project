from django.db import models

# Create your models here.



class CurrencyRate(models.Model):
    source_currency = models.CharField(max_length=3)
    target_currency = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return f'{self.source_currency} to {self.target_currency}: {self.rate}'
