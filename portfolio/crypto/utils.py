import requests
import plotly.graph_objs as go
from plotly.offline import plot
from dotenv import load_dotenv
import os

def get_supported_coins():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": os.getenv("COINGECKO_API"),
    }
    params = {"vs_currency": 'usd'}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        coins = response.json()
        sorted_coins = sorted(coins, key=lambda x: x["market_cap_rank"])
        # Format: ("bitcoin", "BTC")
        return [(c["id"], c['symbol'].upper()) for c in sorted_coins]
    return []

def get_coin_image(coin_id):
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}'
    headers = {"accept": "application/json", "x-cg-demo-api-key": "CG-irvQs4a86UrgfQTxLNHfYtpY\t"}
    params = {"id": coin_id, "localization": False, 'market_data': False, 'community_data': False, 'developer_data': False}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['image']['large']  
    return None

def plot_plotly_chart(df, vs_currency, days, y_column='price', title=''):

    min_y = df[y_column].min() - df[y_column].min()*0.01
    baseline_y = [min_y] * len(df)

    fig = go.Figure()

    # Invisible baseline at min price
    fig.add_trace(go.Scatter(
        x=df['date'].tolist(),
        y=baseline_y,
        mode='lines',
        line=dict(color='rgba(0,0,0,0)'), # invisible
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=df['date'].tolist(),
        y=df[y_column].tolist(),
        mode='lines',
        name=y_column.capitalize(),
        line=dict(color='#34b7a7', width=2),
        fill='tonexty', 
        fillcolor='rgba(52, 183, 167, 0.3)',  
        showlegend=False
    ))

    fig.update_layout(
        title=title or f"{y_column.replace('_', ' ').title()} over {days} {'day' if days == '1' else 'days'}",
        xaxis_title='Date',
        yaxis_title=f"{y_column.replace('_', ' ').title()} in {vs_currency.upper()}",
        margin=dict(l=20, r=20, t=40, b=20),
        template='plotly_white',
    )

    # Generate embeddable HTML string (JS+DIV)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div
