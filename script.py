'''Web application that displays stock charts.'''
from datetime import date

import streamlit as st
import plotly.graph_objects as go

import pandas as pd
import pandas_datareader as web



def main():
    '''Main Function of the Application'''
    st.write("""
    # Stock Market Web Application
    Visually show data on a stock! 
    """)
    st.sidebar.header('User Input')
    start, end, symbol = get_input()
    df: pd.DataFrame = get_data(symbol, start, end)

    if df.empty:
        show_error(symbol)
    else:
        show_data(symbol, df)


def get_input():
    '''Function that handles user inputs in streamlit textboxes'''
    start_date = st.sidebar.text_input('Start Date')
    end_date = st.sidebar.text_input(
        'End Date', date.today().strftime('%Y-%m-%d'))
    stock_symbol = st.sidebar.text_input('Stock Symbol')
    return (start_date, end_date, stock_symbol)


def get_data(symbol: str, start: str, end: str) -> pd.DataFrame:
    '''Function that handles data retrieval from yahoo finance'''
    try:
        return web.DataReader(symbol, 'yahoo', start, end)
        # return web.DataReader(symbol, 'yahoo', start=start, end=end)
    except:
        return pd.DataFrame()


def candlestick_chart(symbol: str, df: pd.DataFrame) -> go.Figure:
    '''Function that creates a candlestick chart'''
    fig = go.Figure(
        data = [go.Candlestick(
            x = df.index,
            open = df['Open'],
            high = df['High'],
            low = df['Low'],
            close = df['Close'],
            name = symbol
        )]
    )
    fig.update_layout(
        title=symbol + ' Daily Chart',
        xaxis_title="Date",
        yaxis_title="Price ($)",
    )
    return fig


def show_data(symbol: str, df: pd.DataFrame) -> None:
    '''Function that shows the data in a chart'''
    st.header(f'{symbol.upper()}\n')
    st.plotly_chart(candlestick_chart(symbol, df))

    st.header(f'{symbol.upper()} Volume\n')
    st.line_chart(df['Volume'])

    st.header('Data Statistics')
    st.write(df.describe())


def show_error(symbol: str) -> None:
    '''Function that shows an error message'''
    st.write(f"""
    ### Error while loading symbol: {symbol} 
    Please control if the stock name is correct!
    """)


if __name__ == '__main__':
    main()
