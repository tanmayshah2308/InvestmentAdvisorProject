import yfinance as yf
import math

list_of_stocks = ['AC.TO', 'CTC-A.TO', 'SU.TO']
all_SMA = {}
all_EMA = {}
all_WMA = {}
all_BBone = {}
all_BBtwo = {}
all_MACDOne = {}
all_MACDTwo = {}

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


    # Get the success rate of EMA and add info to all_EMA
    curr_long_EMA, buy_price_EMA, sell_price_EMA, successes_EMA, failures_EMA = \
        0, 0, 0, 0, 0,

    # for the first value in prev EMAs, we use SMA
    # calculation for the 50 day SMA
    total = 0
    for j in range(50):
        total += list_of_open_prices[j]
    fifty_day_SMA = total / 50
    prev_fifty_day_EMA = fifty_day_SMA

    # calculation for 10 day SMA
    total_1 = 0
    for k in range(40, 50):
        total_1 += list_of_open_prices[k]
    ten_day_SMA = total_1 / 10
    prev_ten_day_EMA = ten_day_SMA

    fifty_day_soothing_average = 2/51
    ten_day_soothing_average = 2/11

    for i in range(50, length):
        curr_price = list_of_open_prices[i]
        #calculate 50 day EMA
        curr_fifty_EMA = (fifty_day_soothing_average * (curr_price - prev_fifty_day_EMA)) + prev_fifty_day_EMA

        #calculate 10 day EMA
        curr_ten_EMA = (ten_day_soothing_average * (curr_price - prev_ten_day_EMA)) + prev_ten_day_EMA

        #buy if 10 day SMA is > 50 day SMA. sell otherwise, if we have bought to begin with
        if curr_ten_EMA > curr_fifty_EMA and curr_long_EMA == 0:
            buy_price_EMA = curr_price
            curr_long_EMA = 1

        elif curr_ten_EMA < curr_fifty_EMA and curr_long_EMA == 1:
            sell_price_EMA = curr_price
            curr_long_EMA = 0
            if buy_price_EMA > sell_price_EMA:
                successes_EMA += 1
            else:
                failures_EMA += 1

        #Update prev EMA
        prev_fifty_day_EMA = curr_fifty_EMA
        prev_ten_day_EMA = curr_ten_EMA

    all_EMA[stock_name] = ['instances evaluated: ' + str(length), 'success rate: ' +
                           str(round(successes_EMA / (successes_EMA + failures_EMA) * 100, 2)) + '%']



    # Get the success rate of WMA and add it to all_WMA
    curr_long_WMA, buy_price_WMA, sell_price_WMA, successes_WMA, failures_WMA = \
        0, 0, 0, 0, 0,

    for i in range(50, length):
        #calculate 50 day WMA
        total = 0
        incrementor = 0
        for j in range(i-50, i):
            incrementor += 1
            total += incrementor * list_of_open_prices[j]
        fifty_day_WMA = total / ((50*51)/2)

        #calculate 10 day WMA
        total_1 = 0
        incrementor_1 = 0
        for k in range(i-10, i):
            incrementor_1 += 1
            total_1 += incrementor_1 * list_of_open_prices[k]
        ten_day_WMA = total_1 / ((10*11)/2)

        #buy if 10 day WMA is > 50 day WMA. sell otherwise, if we have bought to begin with
        if ten_day_WMA > fifty_day_WMA and curr_long_WMA == 0:
            buy_price_WMA = list_of_open_prices[i]
            curr_long_WMA = 1

        elif ten_day_WMA < fifty_day_WMA and curr_long_WMA == 1:
            sell_price_WMA = list_of_open_prices[i]
            curr_long_WMA = 0
            if buy_price_WMA > sell_price_WMA:
                successes_WMA += 1
            else:
                failures_WMA += 1

    all_WMA[stock_name] = ['instances evaluated: ' + str(length), 'success rate: ' +
                           str(round(successes_WMA / (successes_WMA + failures_WMA) * 100, 2)) + '%']


    # Using Bollinger Bands Strategy 1: Buy when price dips below support, sell when it hits the SMA again.
    # Downside: this strategy doesn't factor in trends (we could continually buy in downtrends)

    curr_long_BBone, buy_price_BBone, sell_price_BBone, successes_BBone, failures_BBone = 0, 0, 0, 0, 0

    for i in range(20, length):
        total_sum = 0
        for j in range(i-20, i):
            total_sum += list_of_open_prices[j]
        twenty_day_mean = total_sum/20

        variance_sum = 0
        for k in range(i-20, i):
            variance_sum += list_of_open_prices[k] - twenty_day_mean
        variance = variance_sum/20
        standard_dev = math.sqrt(int(variance))

        lower_band_val = twenty_day_mean - (2 * standard_dev)

        curr_price = list_of_open_prices[i]

        if curr_price < lower_band_val and curr_long_BBone == 0:
            buy_price_BBone = curr_price
            curr_long_BBone = 1
        elif curr_price >= twenty_day_mean and curr_long_BBone == 1:
            sell_price_BBone = curr_price
            if sell_price_BBone > buy_price_BBone:
                successes_BBone += 1
            elif sell_price_BBone < buy_price_BBone:
                failures_BBone += 1
            curr_long_BBone = 0

    all_BBone[stock_name] = ['instances evaluated: ' + str(length), 'success rate: ' +
                             str(round(successes_BBone / (successes_BBone + failures_BBone) * 100, 2)) + '%']


    # Bollinger Bands Strategy 2: Same as above except sell when stock goes past resistance (upper band)

    curr_long_BBtwo, buy_price_BBtwo, sell_price_BBtwo, successes_BBtwo, failures_BBtwo = 0, 0, 0, 0, 0

    for i in range(20, length):
        total_sum = 0
        for j in range(i-20, i):
            total_sum += list_of_open_prices[j]
        twenty_day_mean = total_sum/20

        variance_sum = 0
        for k in range(i-20, i):
            variance_sum += (list_of_open_prices[k] - twenty_day_mean)**2
        variance = variance_sum/20
        standard_dev = math.sqrt(int(variance))
        standard_dev_main = standard_dev

        lower_band_val = twenty_day_mean - (2 * standard_dev)
        upper_band_val = twenty_day_mean + (2 * standard_dev)
        curr_price = list_of_open_prices[i]

        if curr_price < lower_band_val and curr_long_BBtwo == 0:
            buy_price_BBtwo = curr_price
            curr_long_BBtwo = 1
        elif curr_price >= upper_band_val and curr_long_BBtwo == 1:
            sell_price_BBtwo = curr_price
            if sell_price_BBtwo > buy_price_BBtwo:
                successes_BBtwo += 1
            elif sell_price_BBtwo < buy_price_BBtwo:
                failures_BBtwo += 1
            curr_long_BBtwo = 0

    all_BBtwo[stock_name] = ['instances evaluated: ' + str(length), 'success rate: ' +
                             str(round(successes_BBtwo / (successes_BBtwo + failures_BBtwo) * 100, 2)) + '%']


    # MACD is the first oscillator I will consider. It tracks momentum using EMA. The first strategy involves finding when
    # the MACD line crosses the centerline (0), and the second strategy is finding when the MACD crosses the signal line,
    # the 9 day EMA of the MACD itself.

    # Strategy 1: MACD = 12 day EMA - 26 day EMA
    # Calculate 26 day SMA as the prevEMA of the first day
    total = 0
    for i in range(26):
        total += list_of_open_prices[i]
    prev_twenty_six_dayEMA = total/26

    # Calculate 12 day SMA as the prev EMA for the first day
    total = 0
    for j in range(14, 26):
        total += list_of_open_prices[j]
    prev_twelve_dayEMA = total/12

    # find the soothing average/multiplier
    twelve_day_soothing_average = 2/13
    twenty_six_day_soothing_average = 2/27

    curr_long_MACDOne, buy_price_MACDOne, sell_price_MACDOne, successes_MACDOne, failures_MACDOne = 0, 0, 0, 0, 0
    curr_long_MACDTwo, buy_price_MACDTwo, sell_price_MACDTwo, successes_MACDTwo, failures_MACDTwo = 0, 0, 0, 0, 0
    total_gain_loss = 0
    num_trades = 0

    #for second strategy
    nine_day_MACD_hist = []

    # We can combine the strategies so we don't have to repeat the same code unnecessarily
    for i in range(26, length):
        curr_price = list_of_open_prices[i]
        curr_twenty_six_dayEMA = (twenty_six_day_soothing_average * (curr_price - prev_twenty_six_dayEMA)) + prev_twenty_six_dayEMA
        curr_twelve_day_EMA = (twelve_day_soothing_average * (curr_price - prev_twelve_dayEMA)) + prev_twelve_dayEMA
        curr_MACD = curr_twelve_day_EMA - curr_twenty_six_dayEMA

        # First Strategy: Centerline Crossover

        if curr_MACD > 0 and curr_long_MACDOne == 0:
            buy_price_MACDOne = curr_price
            curr_long_MACDOne = 1
        elif curr_MACD < 0 and curr_long_MACDOne == 1:
            sell_price_MACDOne = curr_price
            total_gain_loss += sell_price_MACDOne - buy_price_MACDOne
            num_trades += 1
            if sell_price_MACDOne > buy_price_MACDOne:
                successes_MACDOne += 1
            else:
                failures_MACDOne += 1
            curr_long_MACDOne = 0

        # update the prev EMA
        prev_twenty_six_dayEMA = curr_twenty_six_dayEMA
        prev_twelve_dayEMA = curr_twelve_day_EMA

        # Second Strategy: 9 Day EMA crossover
        # Collect the first 9 MACD's to get the prev_nine_day_EMA. Then compare if the MACD crosses it.
        if i < 35:
            nine_day_MACD_hist.append(curr_MACD)
        elif i >= 35:
            prev_nine_day_EMA_of_MACD = sum(nine_day_MACD_hist)/9
            if curr_MACD > prev_nine_day_EMA_of_MACD and curr_long_MACDTwo == 0:
                buy_price_MACDTwo = curr_price
                curr_long_MACDTwo = 1
            elif curr_MACD < prev_nine_day_EMA_of_MACD and curr_long_MACDTwo == 1:
                sell_price_MACDTwo = curr_price
                curr_long_MACDTwo = 0
                if sell_price_MACDTwo > buy_price_MACDTwo:
                    successes_MACDTwo += 1
                else:
                    failures_MACDTwo += 1
            nine_day_MACD_hist.pop(0)
            nine_day_MACD_hist.append(curr_MACD)

    all_MACDOne[stock_name] = ['instances evaluated: ' + str(length), 'success rate: ' +
                               str(round(successes_MACDOne / (successes_MACDOne + failures_MACDOne) * 100, 2)) + '%']

    all_MACDTwo[stock_name] = ['instances evaluated: ' + str(length), 'success rate: ' +
                               str(round(successes_MACDTwo / (successes_MACDTwo + failures_MACDTwo) * 100, 2)) + '%']
    #print(total_gain_loss/num_trades)

print('\nThe following are the backtesting results of 3 TSX stocks \nusing the '
      'SMA indicator.\nInterval: 60 mins\nTotal Period of Time: 2 year\n')

print('SMA')
for item in all_SMA:
    print(item +':', all_SMA[item])

print('\nEMA')
for item in all_EMA:
    print(item +':', all_EMA[item])

print('\nWMA')
for item in all_WMA:
    print(item +':', all_WMA[item])

print('\nBB-One')
for item in all_BBone:
    print(item + ':', all_BBone[item])

print('\nBB-Two')
for item in all_BBtwo:
    print(item + ':', all_BBtwo[item])

print('\nMACD-One')
for item in all_MACDOne:
    print(item + ':', all_MACDOne[item])

print('\nMACD-Two')
for item in all_MACDTwo:
    print(item + ':', all_MACDTwo[item])
