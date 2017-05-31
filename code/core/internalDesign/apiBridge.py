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
            return cryptoData[crypto]["lowestAsk"]
    except:
        return None

def getFeeFromCrypto(crypto):
    try:
        with open('feeJSON', 'r') as fee:
            feeData = json.load(fee)
            return feeData[crypto]["txFee"]
    except:
        return None
