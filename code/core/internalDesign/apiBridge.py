# apiBridge.py
# Teilen dev May 30th, 2017.

'''
Module in charge of the interpretation of the JSON results
for an easy access from the main Teilen class.
'''

import json

def getDataFromTicker(cryptoPair):
    try:
        with open('tickerJSON', 'r') as ticker:
            cryptoData = json.load(ticker)
            if "error" in cryptoData:
                return None
            else:
                return cryptoData[cryptoPair]["lowestAsk"]
    except:
        return None

def getFeeFromCrypto(crypto):
    try:
        with open('feeJSON', 'r') as fee:
            feeData = json.load(fee)
            if "error" in feeData:
                return None
            else:
                return feeData[crypto]["txFee"]
    except:
        return None

def isOpenOrder(cryptoPair, orderNumber):
    try:
        with open('ordersJSON', 'r') as openOrder:
            orderData = json.load(openOrder)
            if "error" in orderData:
                return None
            else:
                if len(orderData[cryptoPair]) > 0:
                    return orderData[cryptoPair][orderNumber]
                else:
                    return None
    except:
        return None
