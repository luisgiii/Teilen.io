# apiBridge.py
# Teilen dev May 30th, 2017.

'''
Module in charge of the interpretation of the JSON results
for an easy access from the main Teilen class.
'''

import json
import etherBlockchainAPI as ethApi

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
Function: isOpenOrder(cryptoPair, orderNumber)

Parameters:
* cryptoPair - currency Pair used for the exchange.
* orderNumber - value generated after performing a purchase.

Return:
* open order confirmation.

This function purpose is to validate if there's an open order of the previously performed buy.
'''
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

'''
Function: isDepositInPoloniex(txid)

Parameters:
* txid - This is obtained from the blockchain.

Return:
Status "COMPLETE" when the deposit is found in the data.

This function purpose is to let us know that the deposit is received, so
we can proceed with the exchange process.
'''
def isDepositInPoloniex(txid):
    try:
        with open('depositPoloniexJSON', 'r') as deposit:
            depositData = json.load(deposit)
            if "error" in depositData:
                return None
            else:
                if len(depositData["deposits"]) > 0:
                    for depositIdx in range(0, len(depositData["deposits"])):
                        if depositData["deposits"][depositIdx]["txid"] == txid:
                            return depositData["deposits"][depositIdx]["status"]
                        else:
                            return None
                else:
                    return None
    except:
        return None

'''
Function: getAmountFromDeposit(txid)

Parameters:
* txid - This is obtained from the blockchain.

Return:
* Amount of crypto that arrived to Poloniex from the deposit.

This function purpose is to extract the amount from the deposit performed
by the user.

'''
def getAmountFromDeposit(txid):
    try:
        with open('depositPoloniexJSON', 'r') as deposit:
            depositData = json.load(deposit)
            if "error" in depositData:
                return None
            else:
                for depositIdx in range(0, len(depositData["deposits"])):
                    if depositData["deposits"][depositIdx]["txid"] == txid:
                        return depositData["deposits"][depositIdx]["amount"]
                    else:
                        return None
    except:
        return None

'''
'''
def isDepositInBlockchain(txTimestamp):
    return ethApi.getTxidFromBlock(txTimestamp)
