'''
Utilizing financialmodelingprep.com for their free-endpoint API
to gather company financials.

NOTE: Some code taken directly from their documentation. See: https://financialmodelingprep.com/developer/docs/. 
'''

from urllib.request import urlopen
import json

api_key = 'xxxxx'

def get_jsonparsed_data(url):
    '''
    Fetch url, return parsed json. 

    args:
        url: the url to fetch.
    
    returns:
        parsed json
    '''
    response = urlopen(url)
    data = response.read().decode('utf-8')
    return json.loads(data)

def get_EV_statement(ticker, period = 'annual'):
    '''
    Fetch EV statement, with details like total shares outstanding, from FMP.com

    args:
        ticker: company tickerr
    returns:
        parsed EV statement
    '''
    if period == 'annual':
        url = 'https://financialmodelingprep.com/api/v3/enterprise-value/{}'.format(ticker)
    elif period == 'quarter':
        url = 'https://financialmodelingprep.com/api/v3/enterprise-value/{0}?period=quarter&apikey={1}'.format(ticker, api_key)
    else:
        raise ValueError("in get_EV_statement: invalid period")     # may as well throw...
    print(url)
    return get_jsonparsed_data(url)

#! TODO: maybe combine these with argument flag for which statement, seems pretty redundant tbh
def get_income_statement(ticker, period = 'annual'):
    '''
    Fetch income statement.

    args:
        ticker: company ticker.
        period: annual default, can fetch quarterly if specified. 

    returns:
        parsed company's income statement
    '''
    if period == 'annual':
        url = 'https://financialmodelingprep.com/api/v3/income-statement/{}'.format(ticker)
    elif period == 'quarter':
        url = 'https://financialmodelingprep.com/api/v3/income-statement/{0}?period=quarter&apikey={1}'.format(ticker, api_key)
    else:
        raise ValueError("in get_income_statement: invalid period")     # may as well throw...

    print(url)
    return get_jsonparsed_data(url)


def get_cashflow_statement(ticker, period = 'annual'):
    '''
    Fetch cashflow statement.

    args:
        ticker: company ticker.
        period: annual default, can fetch quarterly if specified. 

    returns:
        parsed company's cashflow statement
    '''
    if period == 'annual':
        url = 'https://financialmodelingprep.com/api/v3/cash-flow-statement/{}'.format(ticker)
    elif period == 'quarter':
        url = 'https://financialmodelingprep.com/api/v3/cash-flow-statement/{0}?period=quarter&apikey={1}'.format(ticker, api_key)
    else:
        raise ValueError("in get_cashflow_statement: invalid period")     # may as well throw...

    print(url)
    return get_jsonparsed_data(url)

def get_balance_statement(ticker, period = 'annual'):
    '''
    Fetch balance sheet statement.

    args:
        ticker: company ticker.
        period: annual default, can fetch quarterly if specified. 

    returns:
        parsed company's balance sheet statement
    '''
    if period == 'annual':
        url = 'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{}'.format(ticker)
    elif period == 'quarter':
        url = 'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{0}?period=quarter&apikey={1}'.format(ticker, api_key)
    else:
        raise ValueError("in get_balancesheet_statement: invalid period")     # may as well throw...

    print(url)
    return get_jsonparsed_data(url)

def get_stock_price(ticker):
    '''
    Fetches the stock price for a ticker

    args:
        ticker
    
    returns:
        {'symbol': ticker, 'price': price}
    '''
    url = 'https://financialmodelingprep.com/api/v3/stock/real-time-price/{}'.format(ticker)
    return get_jsonparsed_data(url)

def get_batch_stock_prices(tickers):
    '''
    Fetch the stock prices for a list of tickers.

    args:
        tickers: a list of  tickers........
    
    returns:
        dict of {'ticker':  price}
    '''
    prices = {}
    for ticker in tickers:
        prices[ticker] = get_stock_price(ticker)['price']

    return prices

def get_historical_share_prices(ticker, dates):
    '''
    Fetch the stock price for a ticker at the dates listed.

    args:
        ticker: a ticker.
        dates: a list of dates from which to fetch close price.

    returns:
        {'date': price, ...}
    '''
    prices = {}
    for date in dates:
        date_start, date_end = date[0:8] + str(int(date[8:]) - 2), date
        url = 'https://financialmodelingprep.com/api/v3/historical-price-full/{}?from={}&to={}&apikey={}'.format(ticker, date_start, date_end, api_key)
        print(url)
        historical_price_full = get_jsonparsed_data(url)
        print(historical_price_full)
        try:
            prices[date_end] = historical_price_full['historical'][0]['close']
        except IndexError:
            #  RIP nested try catch, so many issues with dates just try a bunch and get within range of earnings release
            try:
                prices[date_start] = historical_price_full['historical'][0]['close']
            except IndexError:
                print(date + ' ', historical_price_full)

    return prices

if __name__ == '__main__':
    ''' quick test, to use run data.py directly '''

    ticker = 'AAPL'
    data = get_cashflow_statement(ticker)
    print(data)
