from django import forms
from .utils import get_supported_coins

class CryptoDashboardForm(forms.Form):
    TIME_CHOICES = [
        ('1', '1 Day'),
        ('7', '7 Days'),
        ('30', '30 Days'),
        ('90', '90 Days'),
        ('180', '180 Days'),
        ('365', '365 Days'),
    ]

    list_currency = ['usd', 'aed', 'aud', 'brl', 'cad', 'chf', 'clp', 'cny', 'czk', 'dkk', 'eur', 'gbp', 'hkd', 'huf', 
    'idr', 'ils', 'inr', 'jpy', 'krw', 'mxn', 'myr', 'nok', 'nzd', 'php', 'pln', 'rub', 'sar', 'sek', 'sgd', 'thb', 'try', 'twd', 'zar']
    VS_CURRENCY_CHOICES = [(currency, currency.upper()) for currency in list_currency]

    CHART_CHOICES = [
        ('price', 'Price'),
        ('volume', 'Volume'),
        ('market_cap', 'Market Cap'),
    ]

    coin = forms.ChoiceField(
        widget=forms.Select(attrs={
            'id': 'coin-select',
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        })
    )

    vs_currency = forms.ChoiceField(
        choices=VS_CURRENCY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        })
    )

    days = forms.ChoiceField(
        choices=TIME_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        })
    )

    chart_type = forms.ChoiceField(
        choices=CHART_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full',
            'style': 'border: none; outline: none; text-align: left; width: 100%; padding-left: 0;'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['coin'].choices = get_supported_coins()
