import openpyxl
from numpy import less, maximum
import pandas as pd
from nsepython import *

loc = r'D:\MEERAN DOC\Internships\Rishab Pruthi  _Python Dev __ORB\BankNifty2020\Monthly Segregated\january'
fileName = '\BANKNIFTY.CSV'
file = loc + fileName


sheet = pd.read_csv(file, header=None)
# print(len(sheet))


listOfDates = {}

val = 0
while val<len(sheet):
    date = sheet.iloc[val][1]
    # print(date)
    if date not in listOfDates:
        # listOfDates.append(date)
        listOfDates[date] = val
    val+=1

print (listOfDates)

buyStopLoss=0
sellStopLoss=0
buy = sell = False
Open = close =  high = 0
low = maximum
print(low)
for dt, index in listOfDates.items():
    i= index    
    # print(index)
    openVal = sheet.iloc[i][3]
    closeVal = sheet.iloc[i+14][6]
    while True:
        if (sheet.iloc[i][2]>='09:16') and (sheet.iloc[i][2]<='09:31'):
            highVal = sheet.iloc[i][4]
            lowVal = sheet.iloc[i][5]
            Open = openVal
            close = closeVal
            if str(highVal) > str(high):
                high = highVal
            if str(lowVal) < str(low):
                low = lowVal
            i+=1

        elif (sheet.iloc[i][2]>'09:31'):
            if sheet.iloc[i][4]>high:
                buyStopLoss = high - ((sheet.iloc[i][4]/100)*0.5)
                print("Buy initiated with stoploss of " + str(buyStopLoss))
                print("Buy init val " +str(sheet.iloc[i][2]) +"   " + str(sheet.iloc[i][4]))
                buy = True
                i+=1
                break
            elif sheet.iloc[i][5]<low:
                sellStopLoss = low + ((sheet.iloc[i][5]/100)*0.5)
                print("Sell initiated with stoploss of " + str(sellStopLoss))
                print("sell init val" +str(sheet.iloc[i][2]) +"   " + str(sheet.iloc[i][5]))
                sell = True
                i+=1
                break
            else: i+=1
    


            

while True:
    if (sheet.iloc[i][2]>='09:32') and (sheet.iloc[i][2]<='15:15'):
        # print(buyStopLoss,sellStopLoss)
        if (sheet.iloc[i][4] <= buyStopLoss) and buy:
            print('Sell at '+ str(sheet.iloc[i][4]))
            print("sell init val" +str(sheet.iloc[i][2]) +"   " + str(sheet.iloc[i][4]))
            i+=1
            break
        elif (sheet.iloc[i][5] >= sellStopLoss) and sell:
            print('Buy at '+ str(sheet.iloc[i][5]))
            i+=1
            break
        elif sheet.iloc[i][2]=='15:15':
            if buy:
                print('Position Squared Off')
                print('Stocks Sold')
            elif sell:
                print('Position Squared Off')
                print('Stocks Bought')
        else: i+=1
    else: i+=1
