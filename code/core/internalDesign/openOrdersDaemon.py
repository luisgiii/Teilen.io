# apiBridge.py
# Teilen dev May 30th, 2017.

'''
Module in charge to check the status of the open orders.
'''

import urllib
import urllib2
import json
import time
import hmac,hashlib
import settings

def PoloniexTradingAPI(JSONfile, command, req={}):
    req['command'] = command
    req['nonce'] = int(time.time()*1000)
    encoded_data = urllib.urlencode(req)

    sign = hmac.new(settings.poloniex_secret, encoded_data, hashlib.sha512).hexdigest()
    headers = {'Sign': sign, 'Key': settings.poloniex_key}

    try:
        ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', encoded_data, headers))
        json_data = json.loads(ret.read())
        json.dump(json_data, JSONfile)
    except urllib2.HTTPError as err:
        print err

def main():
    while True:
        with open("ordersJSON","wb") as ordersData:
            PoloniexTradingAPI(ordersData, "returnOpenOrders", {"currencyPair":"all"})
        time.sleep(2)

if __name__ == '__main__':
    main()
