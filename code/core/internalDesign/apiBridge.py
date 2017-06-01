# apiBridge.py
# Teilen dev May 30th, 2017.

'''
Module in charge of the interpretation of the JSON results
for an easy access from the main Teilen class.
'''

import json

'''
Function: getDataFromTicker(cryptoPair)

Parameters:
* cryptoPair - currency Pair used for the exchange.

Return:
* lowestAsk value.

This function purpose is to extract the lowesAsk value requested with the cryptoPair needed for the exchange.

'''
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

'''
Function: getFeeFromCrypto(crypto)

Parameters:
* crypto - currency requested for the exchange.

Return:
* txFee value.

This function purpose is to extract the txFee value from the crypto requested for the exchange.

'''     
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

'''
Function: getOpenOrder(cryptoPair, orderNumber)

Parameters:
* cryptoPair - currency Pair used for the exchange.
* orderNumber - value generated after performing a purchase.

Return:
* open order confirmation.

This function purpose is to validate if there's an open order of the previously performed buy.

'''    
def getOpenOrder(cryptoPair, orderNumber):
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
