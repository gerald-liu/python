from pandas_datareader.data import DataReader
# import xml.etree.ElementTree as ET
# import datetime
import numpy as np
# from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

tickers = ['NVDA','INTC','AMD','TXN','SPX']
period = ('09/25/2015', '09/21/2018')
stock_returns_file = 'returns.csv'
ff_factors_file = 'ff_factors.csv'
# treasury_yield_data_file = 'DailyTreasuryYieldCurveRateData.xml'

def get_returns(tickers, period, outfile=''):
    prices_list = []
    for ticker in tickers:
        prices_list.append(DataReader(ticker, data_source='av-weekly-adjusted',
            start=period[0], end=period[1], access_key='W0DV7TX7VA1QQEOA')['adjusted close'].values)

    prices = np.vstack(prices_list)
    returns = np.true_divide(np.diff(prices), prices[:, :-1])
    if outfile != '':
        np.savetxt(outfile, returns, delimiter=",")
    return returns

def get_ff_factors(period, outfile=''):
    ff_factors = DataReader('F-F_Research_Data_Factors_weekly', data_source='famafrench',
        start=period[0], end=period[1], access_key='W0DV7TX7VA1QQEOA')[0].values
    if outfile != '':
        np.savetxt(outfile, ff_factors, delimiter=",")
    return ff_factors

# def get_rf(treasury_yield_data_file):
#     tree = ET.parse(treasury_yield_data_file)
#     root = tree.getroot()
#     dates_daily = [entry[6][0][1].text[:10] for entry in root.findall('entry')]
#     rf_30y_daily = [float(entry[6][0][12].text)/100 for entry in root.findall('entry')]

#     rf_30y = []
#     d = datetime.datetime(2015, 9, 25)
#     i = 0
#     while d <= datetime.datetime(2018, 9, 21):
#         while datetime.datetime.strptime(dates_daily[i], '%Y-%m-%d') < d:
#             i += 1
#         rf_30y.append(rf_30y_daily[i])
#         d += datetime.timedelta(days=7)
    
#     return rf_30y

def get_avg_rp(mkt_prices, rf):
    r_mkt = np.true_divide(mkt_prices[4, 52:] - mkt_prices[4, :-52], mkt_prices[4, :-52])
    risk_premiums = r_mkt - rf[52:]
    return np.mean(risk_premiums)

# def linear_reg(X, y, single=True):
#     reg = LinearRegression()
#     if single:
#         X = np.reshape(X, (-1, 1))
#     else:
#         y = np.reshape(y, (-1, 1))
#     reg.fit(X, y)
#     return reg

def linear_reg(X, y):
    X = np.column_stack((np.ones((X.shape[0],)), X))
    if y.ndim == 1:
        y = np.reshape(y, (-1, 1))
    return np.linalg.inv(X.T @ X) @ X.T @ y

def linear_reg_pred(reg, X):
    X = np.column_stack((X, np.ones(X.shape)))
    return X @ reg

def plot_reg(stock_returns, stock_returns_pred, mkt_returns, ticker, mkt_name):
    plt.figure()
    plt.scatter(mkt_returns, stock_returns)
    plt.plot(mkt_returns, stock_returns_pred, 'b')
    plt.title(ticker + ' ~ ' + mkt_name)
    plt.savefig(ticker + ' ~ ' + mkt_name)

def main(tickers, period, stock_returns_file, ff_factors_file, read_local=True):
    if read_local:
        returns = np.genfromtxt(stock_returns_file, delimiter=",")
    else:
        returns = get_returns(tickers, period, outfile=stock_returns_file)

    betas, returns_pred = [], []

    for stock_returns in returns[:-1]:
        reg = linear_reg(returns[-1], stock_returns)
        betas.append(reg[1][0])
        returns_pred.append(linear_reg_pred(reg, returns[-1]))

    for i in range(len(tickers) - 1):
        print(tickers[i] + ' beta:', betas[i])
        plot_reg(returns[i], returns_pred[i], returns[-1], tickers[i], tickers[-1])

    if read_local:
        ff_factors = np.genfromtxt(ff_factors_file, delimiter=",")[1:]
    else:
        ff_factors = get_ff_factors(period, outfile=ff_factors_file)[1:]

    reg_ff = linear_reg(ff_factors[:, :-1], returns[0][:-3] * 100 - ff_factors[:, -1])
    print('\nFama-French 3-factor model:\nbeta:', reg_ff[1][0], 's:', reg_ff[2][0], 'h:', reg_ff[3][0])
    print('F-F model cost of equity:', ([[5, 3.23, 4.08]] @ reg_ff[1:])[0][0] + 3.2)
if __name__ == '__main__':
    main(tickers, period, stock_returns_file, ff_factors_file, read_local=True)
