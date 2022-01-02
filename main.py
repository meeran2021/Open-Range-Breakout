from numpy import less
import pandas as pd
import openpyxl
from nsepython import *

loc = r'D:\MEERAN DOC\Internships\Rishab Pruthi Python Dev\BankNifty2020\Yearly Consolidated\InCsvForm'
fileName = '\BANKNIFTY.CSV'
file = loc + fileName

sheet = pd.read_csv(file)


buyStopLoss=0
sellStopLoss=0
buy = sell = False
_open = close = low = high = 0
i=0

while True:
    if (sheet.iloc[i][2]>='09:16') and (sheet.iloc[i][2]<='09:31'):
        _open+=sheet.iloc[i][3]
        high+=sheet.iloc[i][4]
        low+=sheet.iloc[i][5]
        close+=sheet.iloc[i][6]
        i+=1
    else: break


_open = _open/i+1
high = high/i+1
low = low/i+1
close = close/i+1

# first15MinCandle = [_open, high, low, close]
# print(first15MinCandle)

while True:
    if (sheet.iloc[i][2]>='09:31'):
        if sheet.iloc[i][4]>high:
            buyStopLoss = high - ((sheet.iloc[i][4]/100)*0.5)
            print("Buy initiated with stoploss of " + str(buyStopLoss))
            buy = True
            i+=1
            break
        elif sheet.iloc[i][5]<low:
            sellStopLoss = low + ((sheet.iloc[i][5]/100)*0.5)
            print("Sell initiated with stoploss of " + str(sellStopLoss))
            sell = True
            i+=1
            break
        else: i+=1
    else: i+=1
        

while True:
    if (sheet.iloc[i][2]>='09:32') and (sheet.iloc[i][2]<='15:15'):
        # print(buyStopLoss,sellStopLoss)
        if (sheet.iloc[i][4] <= buyStopLoss) and buy:
            print('Sell at '+ str(sheet.iloc[i][4]))
            i+=1
            break
        elif (sheet.iloc[i][5] >= sellStopLoss) and sell:
            print('Buy at '+ str(sheet.iloc[i][5]))
            i+=1
            break
        else: i+=1
    else: i+=1