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
poloniex_key = "4U0NBBCU-XQPKQGZ5-L0O6V9KE-VHU643TY"
poloniex_secret = "fecf934a7db901f70e8afc8b877c886cb4ecf97e2426cd53103d10cd335b797f7a7d2145534dad6923fc7ca514d01ff71b72feb054be0925c979cc8d5d1f352b"

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
