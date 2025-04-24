import pandas as pd
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CryptoDashboardForm
from .utils import plot_plotly_chart, get_coin_image
from django.contrib import messages
from dotenv import load_dotenv
import os

def crypto_dashboard_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, "⚠️ You need to log in to access this page.")
        return redirect(reverse('login') + f'?next={request.path}')

    df = None
    chart_div = None
    coin_image_url = None

    if request.method == 'POST':
        form = CryptoDashboardForm(request.POST)
        if form.is_valid():
            coin = form.cleaned_data['coin']
            vs_currency = form.cleaned_data['vs_currency']
            days = form.cleaned_data['days']
            chart_type = request.POST.get('chart_type', 'price')

            # Fetch CoinGecko data
            url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
            headers = {"accept": "application/json", "x-cg-demo-api-key": os.getenv("COINGECKO_API")}
            params = {"vs_currency": vs_currency, "days": days, 'precision': '2'}
            response = requests.get(url, headers=headers, params=params)
            data = response.json()

            # Build DataFrame
            df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['date'] = df['timestamp'].dt.date

            volume_df = pd.DataFrame(data['total_volumes'], columns=['timestamp', 'volume'])
            volume_df['timestamp'] = pd.to_datetime(volume_df['timestamp'], unit='ms')
            cap_df = pd.DataFrame(data['market_caps'], columns=['timestamp', 'market_cap'])
            cap_df['timestamp'] = pd.to_datetime(cap_df['timestamp'], unit='ms')

            df = df.merge(volume_df, on='timestamp')
            df = df.merge(cap_df, on='timestamp')
            df = df[['date', 'price', 'volume', 'market_cap']]
            df = df.round(2)

            metric = chart_type
            min_value = df[metric].min()
            max_value = df[metric].max()
            avg_value = df[metric].mean()

            min_date = df.loc[df[metric].idxmin(), 'date'].strftime('%m/%d/%y')
            max_date = df.loc[df[metric].idxmax(), 'date'].strftime('%m/%d/%y')

        
            chart_div = plot_plotly_chart(df, vs_currency, days, y_column=chart_type)
            coin_image_url = get_coin_image(coin)
            chart_type = chart_type.replace('_', ' ').title()

            return render(request, 'crypto/crypto_chart.html', {
            'coin': coin,
            'timeframe' : days,
            'vs_currency' : vs_currency,
            'chart_div': chart_div,
            'chart_type': chart_type,
            'coin_image_url': coin_image_url,
            'min_value': f"{min_value:,.2f}",
            'max_value': f"{max_value:,.2f}",
            'avg_value': f"{avg_value:,.2f}",
            'min_date': min_date,
            'max_date': max_date,
            })
    else:
        form = CryptoDashboardForm()
        return render(request, 'crypto/crypto.html', {
            'form': form,
        })

def download_csv_view(request):
    coin = request.POST.get('coin')
    currency = request.POST.get('vs_currency')
    days = request.POST.get('days')
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    headers = {"accept": "application/json", "x-cg-demo-api-key": "CG-irvQs4a86UrgfQTxLNHfYtpY\t"}
    params = {"vs_currency": currency, "days": days,'precision': '2'}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['date'] = df['timestamp'].dt.date

    df_vol = pd.DataFrame(data['total_volumes'], columns=['timestamp', 'volume'])
    df_vol['timestamp'] = pd.to_datetime(df_vol['timestamp'], unit='ms')

    df_cap = pd.DataFrame(data['market_caps'], columns=['timestamp', 'market_cap'])
    df_cap['timestamp'] = pd.to_datetime(df_cap['timestamp'], unit='ms')

    df = df.merge(df_vol, on='timestamp')
    df = df.merge(df_cap, on='timestamp')
    df = df[['date', 'price', 'volume', 'market_cap']]
    df = df.round(2)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{coin}_{currency}_{days}d.csv"'
    df.to_csv(path_or_buf=response, index=False)
    return response

