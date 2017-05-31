# apiBridge.py
# Teilen dev May 30th, 2017.

'''
Module in charge of the interpretation of the JSON results
for an easy access from the main Teilen class.
'''

import json

def getDataFromTicker(crypto, json_param):
    with open('tickerJSON', 'r') as ticker:
     cryptoData = json.load(ticker)
     print cryptoData
     return crypto[crypto][json_param]
