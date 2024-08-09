from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

# Create your views here.



def home(request):
    return render(request, 'core/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})


from .models import CurrencyRate
from .forms import CurrencyRateForm

def rate_list(request):
    rates = CurrencyRate.objects.all()
    return render(request, 'core/rate_list.html', {'rates': rates})

def rate_create(request):
    if request.method == 'POST':
        form = CurrencyRateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rate_list')
    else:
        form = CurrencyRateForm()
    return render(request, 'core/rate_form.html', {'form': form})

def rate_update(request, pk):
    rate = CurrencyRate.objects.get(pk=pk)
    if request.method == 'POST':
        form = CurrencyRateForm(request.POST, instance=rate)
        if form.is_valid():
            form.save()
            return redirect('rate_list')
    else:
        form = CurrencyRateForm(instance=rate)
    return render(request, 'core/rate_form.html', {'form': form})

def rate_delete(request, pk):
    rate = CurrencyRate.objects.get(pk=pk)
    if request.method == 'POST':
        rate.delete()
        return redirect('rate_list')
    return render(request, 'core/rate_confirm_delete.html', {'rate': rate})

from decimal import Decimal

# def convert_currency(request):
#     if request.method == 'GET':
#         source = request.GET.get('source')
#         target = request.GET.get('target')
#         amount = request.GET.get('amount')

#         if not source or not target or not amount:
#             return render(request, 'core/convert.html', {'error': 'Missing parameters'})

#         try:
#             amount = Decimal(amount)
#         except ValueError:
#             return render(request, 'core/convert.html', {'error': 'Invalid amount'})

#         try:
#             rate = CurrencyRate.objects.get(source_currency=source, target_currency=target)
#             result = amount * rate.rate
#             return render(request, 'core/convert.html', {'result': result})
#         except CurrencyRate.DoesNotExist:
#             return render(request, 'core/convert.html', {'error': 'Currency not supported'})
#     return render(request, 'core/convert.html')


from django.shortcuts import render
from .models import CurrencyRate
from decimal import Decimal
from django.db.models import Q

def convert_currency(request):
    source_currencies = CurrencyRate.objects.values_list('source_currency', flat=True).distinct()
    target_currencies = CurrencyRate.objects.values_list('target_currency', flat=True).distinct()
    
    currencies = set(source_currencies).union(set(target_currencies))
    
    if request.method == 'GET':
        source = request.GET.get('source')
        target = request.GET.get('target')
        amount = request.GET.get('amount')

        if not source or not target or not amount:
            return render(request, 'core/convert.html', {'error': 'Missing parameters', 'currencies': currencies})

        try:
            amount = Decimal(amount)
        except ValueError:
            return render(request, 'core/convert.html', {'error': 'Invalid amount', 'currencies': currencies})

        try:
            rate = CurrencyRate.objects.get(source_currency=source, target_currency=target)
            result = amount * rate.rate
            return render(request, 'core/convert.html', {'result': result, 'currencies': currencies})


        except CurrencyRate.DoesNotExist:
            # 嘗試反方向查找匯率
            try:
                reverse_rate = CurrencyRate.objects.get(source_currency=target, target_currency=source)
                result = amount / reverse_rate.rate
                return render(request, 'core/convert.html', {'result': result, 'currencies': currencies})
            except CurrencyRate.DoesNotExist:
                return render(request, 'core/convert.html', {'error': 'Currency not supported', 'currencies': currencies})


    return render(request, 'core/convert.html', {'currencies': currencies})
