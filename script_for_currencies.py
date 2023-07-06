import requests
import pandas as pd
from datetime import datetime
import os 

if not os.path.exists('DATA'):
    os.mkdir('DATA')
    os.mkdir('DATA//Crypto_currencies')
    os.mkdir('DATA//Crypto_currencies//ETH')
    os.mkdir('DATA//Crypto_currencies//BTC')

#print('scraping data about ETH')
currency ='ETH'
current_time = str(datetime.now().date())

#get futures price in USD:
url = 'https://deribit.com/api/v2/public/get_instruments?currency=' + currency + '&kind=future&expired=false'
api_response = (requests.get(url)).json()
futures_price = pd.DataFrame()
for k in api_response['result'][:-1]:
    instrument_name = k['instrument_name']
    url = 'https://deribit.com/api/v2/public/get_order_book?instrument_name=' + instrument_name
    order_book = (requests.get(url)).json()
    price = order_book['result']['last_price']
    time1 = datetime.fromtimestamp(k['expiration_timestamp'] / 1000)
    expiry_date =  str(time1.year) + '-' + str(time1.month) + '-' + str(time1.day)
    T_actual_365 = (datetime.strptime(expiry_date, "%Y-%m-%d") - datetime.strptime(current_time,"%Y-%m-%d")).days / 365
    futures_price = pd.concat([futures_price, pd.DataFrame([T_actual_365, price]).T])
futures_price.columns = ['Date', 'Price']

#scrapping data about curenct active option instruments
url = 'https://history.deribit.com/api/v2/public/get_instruments?currency=' + currency + '&kind=option&expired=false'
api_response = (requests.get(url)).json()
data_options = pd.DataFrame()

#scrapping data about crypto options
for k in api_response['result']:
    strike = k['strike']
    option_type = k['option_type']
    time1 = datetime.fromtimestamp(k['expiration_timestamp'] / 1000)
    expiration =  str(time1.year) + '-' + str(time1.month) + '-' + str(time1.day)
    T_actual_365 = (datetime.strptime(expiration, "%Y-%m-%d") - datetime.strptime(current_time,"%Y-%m-%d")).days / 365
    spot_price = np.interp(T_actual_365, futures_price['Date'], futures_price['Price'])
    print(spot_price)
    time1 = datetime.fromtimestamp(k['creation_timestamp'] / 1000)
    last_trade_day =  str(time1.year) + '-' + str(time1.month) + '-' + str(time1.day) + ' ' + str(time1.hour) + ':' + str(time1.minute) + ':' + str(time1.second)

    instrument_name = k['instrument_name']
    # scrapping data about given order book
    instuments_information_url = 'https://deribit.com/api/v2/public/get_order_book?instrument_name=' + instrument_name
    instuments_information = (requests.get(instuments_information_url)).json()
    bid_price = instuments_information['result']['best_bid_price']
    ask_price = instuments_information['result']['best_ask_price']
    mid_price = (ask_price + bid_price) / 2
    volume = instuments_information['result']['stats']['volume']
    open_interest = instuments_information['result']['open_interest']
    DerebitIV = (instuments_information['result']['bid_iv'] + instuments_information['result']['ask_iv']) / 2
    data_options = pd.concat([data_options, pd.DataFrame([instrument_name, last_trade_day, expiration, strike, option_type, spot_price, bid_price,ask_price, mid_price, volume, open_interest, DerebitIV]).T])

#making necessary adjustment
data_options.columns = ['instrumentName', 'lastTradeDate', 'expiryDate', 'strike','optionType','last close', 'bid', 'ask', 'mid', 'volume', 'openInterest', 'DerebitIV']
data_options['yFinance_dividend_yield'] = 0
data_options['optionType'].loc[data_options['optionType'] == 'call'] = 'calls'
data_options['optionType'].loc[data_options['optionType'] == 'put'] = 'puts'
data_options['ticker'] = currency
data_options['bid'] = data_options['bid'] * data_options['last close'].unique()[0]
data_options['ask'] = data_options['ask'] * data_options['last close'].unique()[0]
data_options['mid'] = data_options['mid'] * data_options['last close'].unique()[0]
data_options = data_options.loc[data_options['bid'] != 0]
data_options = data_options.loc[data_options['ask'] != 0]

data_options.to_csv('DATA//Crypto_currencies//' + currency + '//' + str(datetime.now().date()) + '-' + str(datetime.now().hour) + '-' + str(datetime.now().minute) + '.csv', index=False)



#print('scraping data about BTC')
currency ='BTC'
current_time = str(datetime.now().date())

#get futures price in USD:
url = 'https://deribit.com/api/v2/public/get_instruments?currency=' + currency + '&kind=future&expired=false'
api_response = (requests.get(url)).json()
futures_price = pd.DataFrame()
for k in api_response['result'][:-1]:
    instrument_name = k['instrument_name']
    url = 'https://deribit.com/api/v2/public/get_order_book?instrument_name=' + instrument_name
    order_book = (requests.get(url)).json()
    price = order_book['result']['last_price']
    time1 = datetime.fromtimestamp(k['expiration_timestamp'] / 1000)
    expiry_date =  str(time1.year) + '-' + str(time1.month) + '-' + str(time1.day)
    T_actual_365 = (datetime.strptime(expiry_date, "%Y-%m-%d") - datetime.strptime(current_time,"%Y-%m-%d")).days / 365
    futures_price = pd.concat([futures_price, pd.DataFrame([T_actual_365, price]).T])
futures_price.columns = ['Date', 'Price']

#scrapping data about curenct active option instruments
url = 'https://history.deribit.com/api/v2/public/get_instruments?currency=' + currency + '&kind=option&expired=false'
api_response = (requests.get(url)).json()
data_options = pd.DataFrame()

#scrapping data about crypto options
for k in api_response['result']:
    strike = k['strike']
    option_type = k['option_type']
    time1 = datetime.fromtimestamp(k['expiration_timestamp'] / 1000)
    expiration =  str(time1.year) + '-' + str(time1.month) + '-' + str(time1.day)
    T_actual_365 = (datetime.strptime(expiration, "%Y-%m-%d") - datetime.strptime(current_time,"%Y-%m-%d")).days / 365
    spot_price = np.interp(T_actual_365, futures_price['Date'], futures_price['Price'])
    print(spot_price)
    time1 = datetime.fromtimestamp(k['creation_timestamp'] / 1000)
    last_trade_day =  str(time1.year) + '-' + str(time1.month) + '-' + str(time1.day) + ' ' + str(time1.hour) + ':' + str(time1.minute) + ':' + str(time1.second)

    instrument_name = k['instrument_name']
    # scrapping data about given order book
    instuments_information_url = 'https://deribit.com/api/v2/public/get_order_book?instrument_name=' + instrument_name
    instuments_information = (requests.get(instuments_information_url)).json()
    bid_price = instuments_information['result']['best_bid_price']
    ask_price = instuments_information['result']['best_ask_price']
    mid_price = (ask_price + bid_price) / 2
    volume = instuments_information['result']['stats']['volume']
    open_interest = instuments_information['result']['open_interest']
    DerebitIV = (instuments_information['result']['bid_iv'] + instuments_information['result']['ask_iv']) / 2
    data_options = pd.concat([data_options, pd.DataFrame([instrument_name, last_trade_day, expiration, strike, option_type, spot_price, bid_price,ask_price, mid_price, volume, open_interest, DerebitIV]).T])

#making necessary adjustment
data_options.columns = ['instrumentName', 'lastTradeDate', 'expiryDate', 'strike','optionType','last close', 'bid', 'ask', 'mid', 'volume', 'openInterest', 'DerebitIV']
data_options['yFinance_dividend_yield'] = 0
data_options['optionType'].loc[data_options['optionType'] == 'call'] = 'calls'
data_options['optionType'].loc[data_options['optionType'] == 'put'] = 'puts'
data_options['ticker'] = currency
data_options['bid'] = data_options['bid'] * data_options['last close'].unique()[0]
data_options['ask'] = data_options['ask'] * data_options['last close'].unique()[0]
data_options['mid'] = data_options['mid'] * data_options['last close'].unique()[0]
data_options = data_options.loc[data_options['bid'] != 0]
data_options = data_options.loc[data_options['ask'] != 0]

data_options.to_csv('DATA//Crypto_currencies//' + currency + '//' + str(datetime.now().date()) + '-' + str(datetime.now().hour) + '-' + str(datetime.now().minute) + '.csv', index=False)