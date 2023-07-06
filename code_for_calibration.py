import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from Data_scrapping import get_funding_rate
from Computing_IV import get_Implied_volatility
from SVI_curves import computing_SVI_IV
import os


ticker = 'ETH'
DATA = os.listdir('DATA//Crypto_currencies//ETH')
discount_curve = pd.read_csv('DATA//discount_curve.csv')

result_ETH = pd.DataFrame()
for data_date in DATA:
    print(data_date)
    filename_for_option_chain = "DATA//Crypto_currencies//" + ticker + '//' + data_date
    options_data = pd.read_csv(filename_for_option_chain)
    Implied_Volatility = get_Implied_volatility(options_data, discount_curve)
    Implied_Volatility_without_extrapolation = computing_SVI_IV(Implied_Volatility, ticker, low_limit = 0.1, high_limit = 2.5, N = 1000, extrapolation=False)
    for r in Implied_Volatility_without_extrapolation['implied_volatility_surface']:
        rk = np.delete(r['max_relative_error'],0)
        rk = np.delete(rk,-1)
        if rk.any():
            if rk.max() > 0.1:
                result_ETH = pd.concat([result_ETH, pd.DataFrame([data_date, r['expiry_date']]).T])
                print(r['expiry_date'])           
    result_ETH.to_csv('DATA//Result_ETH.csv', index=False)

ticker = 'BTC'
DATA = os.listdir('DATA//Crypto_currencies//BTC')
discount_curve = pd.read_csv('DATA//discount_curve.csv')

result_BTC = pd.DataFrame()
for data_date in DATA:
    print(data_date)
    filename_for_option_chain = "DATA//Crypto_currencies//" + ticker + '//' + data_date
    options_data = pd.read_csv(filename_for_option_chain)
    Implied_Volatility = get_Implied_volatility(options_data, discount_curve)
    Implied_Volatility_without_extrapolation = computing_SVI_IV(Implied_Volatility, ticker, low_limit = 0.1, high_limit = 2.5, N = 1000, extrapolation=False)
    for r in Implied_Volatility_without_extrapolation['implied_volatility_surface']:
        rk = np.delete(r['max_relative_error'],0)
        rk = np.delete(rk,-1)
        if rk.any():
            if rk.max() > 0.1:
                result_BTC = pd.concat([result_BTC, pd.DataFrame([data_date, r['expiry_date']]).T])
                print(r['expiry_date'])
    result_BTC.to_csv('DATA//Result_BTC.csv', index=False)