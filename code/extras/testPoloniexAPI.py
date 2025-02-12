'''
Documentation available in:
https://poloniex.com/support/api/

Already existent Python wrappers:
https://github.com/s4w3d0ff/python-poloniex

!# Known issue 1:
    Does not work with IPs from Mexico.
    Solution: Use AWS EC2 Instance.
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
        return json_data[criptoAsset]["lowestAsk"]
    else:
        print response

def PoloniexTradingAPI(command, req={}):
    req['command'] = command
    req['nonce'] = int(time.time()*1000)
    encoded_data = urllib.urlencode(req)

    sign = hmac.new(poloniex_secret, encoded_data, hashlib.sha512).hexdigest()
    headers = {'Sign': sign, 'Key': poloniex_key}

    try:
        ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', encoded_data, headers))
        jsonRet = json.loads(ret.read())
        return jsonRet
    except urllib2.HTTPError as err:
        print err

def main():
    requiredCriptoValue = PoloniexTickerQuery(availableCriptoArray[1])
    if requiredCriptoValue != None:
        print float(requiredCriptoValue)

    goldData = PoloniexTradingAPI("returnBalances")
    print float(goldData["BTC"])

    # Max amount you can get from all the asset you choosed.
    maxAmount = round(float(goldData["BTC"]) / float(requiredCriptoValue), 8)
    print maxAmount

    #WARNING: Buy some LSK using ALL your available BTCs
    PoloniexTradingAPI("buy",{"currencyPair":availableCriptoArray[1], "rate":requiredCriptoValue, "amount":maxAmount})

if __name__ == "__main__":
    main()
