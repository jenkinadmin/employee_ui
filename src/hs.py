import numpy as np
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

# Function to calculate the ATR (Average True Range)
def calculate_atr(data, period=14):
    high_low = data['High'] - data['Low']
    high_close = np.abs(data['High'] - data['Close'].shift())
    low_close = np.abs(data['Low'] - data['Close'].shift())
    
    true_range = pd.DataFrame({
        'high_low': high_low,
        'high_close': high_close,
        'low_close': low_close
    })
    
    atr = true_range.max(axis=1)
    return atr.rolling(window=period).mean()

# Function to calculate Supertrend
def calculate_supertrend(data, period=14, multiplier=3):
    atr = calculate_atr(data, period)
    
    # Calculate the basic bands
    hl2 = (data['High'] + data['Low']) / 2
    upper_band = hl2 + (multiplier * atr)
    lower_band = hl2 - (multiplier * atr)
    
    # Initialize the Supertrend series with NaNs and correct index
    supertrend = pd.Series(index=data.index)
    
    # The first Supertrend value is set to the middle value of the first row (hl2)
    supertrend.iloc[0] = hl2.iloc[0]
    
    # Calculate the Supertrend for each row
    for i in range(1, len(data)):
        if data['Close'][i] <= supertrend.iloc[i-1]:
            supertrend.iloc[i] = upper_band.iloc[i]
        else:
            supertrend.iloc[i] = lower_band.iloc[i]
    
    return supertrend

# Function to generate buy/sell signals
def generate_signals(data):
    data['supertrend'] = calculate_supertrend(data)
    
    # Buy Signal: Price crosses above Supertrend
    data['buy_signal'] = (data['Close'] > data['supertrend']) & (data['Close'].shift(1) <= data['supertrend'].shift(1))
    
    # Sell Signal: Price crosses below Supertrend
    data['sell_signal'] = (data['Close'] < data['supertrend']) & (data['Close'].shift(1) >= data['supertrend'].shift(1))
    return data

# Plotting the results using Plotly
def plot_strategy(data):
    fig = go.Figure()

    # Plot closing price (Candlestick chart)
    fig.add_trace(go.Candlestick(x=data.index,
                open=data['Open'], high=data['High'],
                low=data['Low'], close=data['Close'],
                name='Candlestick'))

    # Plot Supertrend
    fig.add_trace(go.Scatter(x=data.index, y=data['supertrend'], 
                             mode='lines', line=dict(color='green', width=2),
                             name='Supertrend'))

    # Plot buy signals
    fig.add_trace(go.Scatter(x=data.index[data['buy_signal']], 
                             y=data['Close'][data['buy_signal']],
                             mode='markers', marker=dict(symbol='triangle-up', color='green', size=10),
                             name='Buy Signal'))

    # Plot sell signals
    fig.add_trace(go.Scatter(x=data.index[data['sell_signal']], 
                             y=data['Close'][data['sell_signal']],
                             mode='markers', marker=dict(symbol='triangle-down', color='red', size=10),
                             name='Sell Signal'))

    # Layout for better visual clarity
    fig.update_layout(
        title='Nifty50 Supertrend Trading Strategy (5-Minute Timeframe)',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_dark',
        xaxis_rangeslider_visible=False
    )
    
    fig.show()

# Main function to fetch Nifty50 data and apply strategy
def main():
    # Fetch Nifty50 data from Yahoo Finance (5-Minute Interval for the last 7 days)
    data = yf.download('^NSEI', period='7d', interval='5m')  # 7 days of 5-minute data
    
    # Generate signals based on Supertrend strategy
    data = generate_signals(data)

    # Plot the strategy with buy/sell signals using Plotly
    plot_strategy(data)

if __name__ == "__main__":
    main()
