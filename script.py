import streamlit as st
import plotly.figure_factory as ff
import plotly.graph_objects as go

import pandas as pd
import pandas_datareader as web

from datetime import date


def main():
    st.write("""
    # Stock Market Web Application
    Visually show data on a stock! 
    """)
    st.sidebar.header('User Input')
    start, end, symbol = get_input()
    df = get_data(symbol, start, end)

    if df.empty:
        show_error(symbol)
    else:
        show_data(symbol, df)


def get_input():
    start_date = st.sidebar.text_input('Start Date')
    end_date = st.sidebar.text_input(
        'End Date', date.today().strftime('%Y-%m-%d'))
    stock_symbol = st.sidebar.text_input('Stock Symbol')
    return start_date, end_date, stock_symbol


def get_data(symbol, start, end):
    try:
        return web.DataReader(symbol, data_source='yahoo', start=start, end=end)
    except:
        return pd.DataFrame()


def candlestick_chart(symbol, df):
    fig = go.Figure(data=[go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name=symbol)])
    fig.update_layout(
        title=symbol + ' Daily Chart',
        xaxis_title="Date",
        yaxis_title="Price ($)",
    )
    return fig


def show_data(symbol, df):
    st.header(f'{symbol.upper()}\n')
    st.plotly_chart(candlestick_chart(symbol, df))

    st.header(f'{symbol.upper()} Volume\n')
    st.line_chart(df['Volume'])

    st.header('Data Statistics')
    st.write(df.describe())


def show_error(symbol):
    st.write(f"""
    ### Error while loading symbol: {symbol} 
    Please control if the stock name is correct!
    """)


if __name__ == '__main__':
    main()
