from django.contrib import admin

# Register your models here.


from .models import CurrencyRate

admin.site.register(CurrencyRate)
