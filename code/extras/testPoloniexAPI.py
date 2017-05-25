'''
Documentation available in:
https://poloniex.com/support/api/

Already existent Python wrappers:
https://github.com/s4w3d0ff/python-poloniex
'''

import urllib
import urllib2
import json
import time
import hmac,hashlib
import requests

# API credentials
poloniex_key = ""
poloniex_secret = ""

availableCriptoArray = ["BTC_ETH","BTC_LSK"]

def PoloniexTickerQuery(criptoAsset):
    response = requests.get("https://poloniex.com/public?command=returnTicker")
    if response.status_code != 403 and response.status_code != 404:
        print (response)
        json_data = json.loads(response.text)
        return json_data[criptoAsset]["last"]

def PoloniexTradingAPI():
    print 'space holder'

def main():
    requiredCriptoValue = PoloniexTickerQuery(availableCriptoArray[0])
    if requiredCriptoValue != None:
        print float(requiredCriptoValue)

if __name__ == "__main__":
    main()
