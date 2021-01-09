import yfinance as yf

list_of_stocks = ['AC.TO', 'CTC-A.TO', 'SU.TO']
all_SMA = {}

for stock_name in list_of_stocks:
    stock = yf.Ticker(stock_name)
    hist = stock.history(period="2y", interval="60m")
    length = len(hist)
    #print(length)

    list_of_open_prices = []
    for i in range(length):
        list_of_open_prices.append(hist.iloc[i]['Open'])
    #print(list_of_open_prices)

    # Get the success rate of SMA and add info to all_SMA dict
    curr_long_SMA, buy_price_SMA, sell_price_SMA, successes_SMA, failures_SMA = \
        0, 0, 0, 0, 0,

    for i in range(50, length):
        #calculate 50 day SMA
        total = 0
        for j in range(i-50, i):
            total += list_of_open_prices[j]
        fifty_day_average = total / 50

        #calculate 10 day SMA
        total_1 = 0
        for k in range(i-10, i):
            total_1 += list_of_open_prices[k]
        ten_day_average = total_1 / 10

        #buy if 10 day SMA is > 50 day SMA. sell otherwise, if we have bought to begin with
        if ten_day_average > fifty_day_average and curr_long_SMA == 0:
            buy_price_SMA = list_of_open_prices[i]
            curr_long_SMA = 1

        elif ten_day_average < fifty_day_average and curr_long_SMA == 1:
            sell_price_SMA = list_of_open_prices[i]
            curr_long_SMA = 0
            if buy_price_SMA > sell_price_SMA:
                successes_SMA += 1
            else:
                failures_SMA += 1

    all_SMA[stock_name] = ['instances evaluated: ' + str(length), 'success rate: ' +
                           str(round(successes_SMA / (successes_SMA + failures_SMA) * 100, 2)) + '%']

print('\nThe following are the backtesting results of 3 TSX stocks \nusing the '
      'SMA indicator.\nInterval: 60 mins\nTotal Period of Time: 2 year\n')
#print('SMA')
for item in all_SMA:
    print(item +':', all_SMA[item])
