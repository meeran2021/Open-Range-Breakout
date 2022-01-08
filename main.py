import sys
import pandas as pd

global mProfit, mLoss

def getListOfDates(sheet):         #To iterate over dates
    listOfDates = {}
    val = 0
    while val < len(sheet):
        date = sheet.iloc[val][1]
        if date not in listOfDates:
            listOfDates[date] = val
        val += 1
    return listOfDates


def create15MinCandel(i):           #Creating first 15 min candle
    global Open, close, high, low
    Open = close = high = 0
    low = sys.maxsize
    openVal = sheet.iloc[i][3]
    closeVal = sheet.iloc[i + 14][6]
    while True:
        if (sheet.iloc[i][2] >= "09:16") and (sheet.iloc[i][2] <= "09:31"):
            highVal = sheet.iloc[i][4]
            lowVal = sheet.iloc[i][5]
            Open = openVal
            if str(highVal) > str(high):
                high = highVal
            if str(lowVal) < str(low):
                low = lowVal
            close = closeVal
            i += 1
        else:
            break
    return [Open, high, low, close]


def initiate(i):                    #Initiating Buy or Loss with 0.5% as stoploss
    global buy, sell, sellStopLoss, buyStopLoss, sellVal, buyVal
    buy = sell = False
    while True:
        if sheet.iloc[i][2] >= "09:31":
            if sheet.iloc[i][4] > high:
                buyStopLoss = high - ((sheet.iloc[i][4] / 100) * 0.5)
                print("Buy initiated with stoploss at " + str(round(buyStopLoss,2)) 
                    + " on " + str(sheet.iloc[i][1])
                    + " at " + str(sheet.iloc[i][2]) 
                    + " with High: " + str(round(float(sheet.iloc[i][4]),2))
                )
                buyVal = sheet.iloc[i][4]
                buy = True
                return i + 1
            elif sheet.iloc[i][5] < low:
                sellStopLoss = low + ((sheet.iloc[i][5] / 100) * 0.5)
                sellVal = sheet.iloc[i][5]
                print("Sell initiated with stoploss at " + str(round(sellStopLoss))
                    + " on " + str(sheet.iloc[i][1])
                    + " at " + str(sheet.iloc[i][2]) 
                    + " with Low: " + str(round(float(sheet.iloc[i][5]),2))
                )
                sell = True
                return i + 1
            else:
                i += 1
        else:
            i += 1


def finishTrading(i, profit, loss):      #Buying/Selling the initiated stocks along with counting the profit and loss accounts

    while i < len(sheet):
        if (sheet.iloc[i][2] >= "09:32") and (sheet.iloc[i][2] < "15:35"):
            if sheet.iloc[i][4] <= buyStopLoss and buy:
                print("StopLoss Hit")
                print("Sold out val: " + str(round(float(sheet.iloc[i][4]),2))
                    + " on " + str(sheet.iloc[i][1]) 
                    + " at " + str(sheet.iloc[i][2])
                )
                loss += 1
                break
            if sheet.iloc[i][5] >= sellStopLoss and sell == True:
                print("StopLoss Hit")
                print("Buy back val: " + str(round(float(sheet.iloc[i][5]),2))
                    + " on " + str(sheet.iloc[i][1]) 
                    + " at " + str(sheet.iloc[i][2])
                )
                loss += 1
                break
            if sheet.iloc[i][2] == "15:15":
                if buy == True:
                    print("Position Squared Off at ", end="")
                    print(round(float(sheet.iloc[i][4]),2))
                    if sheet.iloc[i][4] > buyVal:
                        print("Stocks Sold with profit")
                        profit += 1
                    else:
                        print("Stocks Sold with loss")
                        loss += 1
                    break
                elif sell == True:
                    print("Position Squared Off at ", end="")
                    print(round(float(sheet.iloc[i][5]),2))
                    if sheet.iloc[i][5] < sellVal:
                        print("Stocks Bought with profit")
                        profit += 1
                    else:
                        print("Stocks Bought with loss")
                        loss += 1
                    break
            else:
                i += 1
        else:
            i += 1
    return profit, loss


if __name__ == "__main__":
    # mProfit = mLoss = 0
    buyStopLoss = 0
    sellStopLoss = 0
    Open = close = high = 0
    low = sys.maxsize
    listOfMnths = [
        r"\January", r"\February", r"\March", r"\April", r"\May", r"\June", 
        r"\July", r"\August", r"\September", r"\October", r"\November", r"\December"
        ]
    
    # Replace loc with your location
    loc = r"D:\MEERAN DOC\Internships\Rishab Pruthi  _Python Dev __ORB\BankNifty2020\Monthly Segregated"
    fileName = "\BANKNIFTY.CSV"
    totalProfit = totalLoss = 0
    for month in listOfMnths:
        mProfit = mLoss = 0
        file = loc + month + fileName
        sheet = pd.read_csv(file, header=None)    
        listOfDates = getListOfDates(sheet)  
        
        for dt, i in listOfDates.items():
            
            candel = create15MinCandel(i)
            print()
            print(candel)
            i = initiate(i)
            mProfit, mLoss = finishTrading(i, mProfit, mLoss)
        
        print("Num of profit in the month of: " + month[1:] +": " + str(mProfit) 
            + "\nNum of Loss in the month of: " + month[1:] +": " + str(mLoss)
        )
        totalProfit += mProfit
        totalLoss += mLoss
    print("Total num of profit in this year: " + str(totalProfit) 
        + "\nTotal num of Loss in the year: " + str(totalLoss)
    )