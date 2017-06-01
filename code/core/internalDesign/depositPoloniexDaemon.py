# depositValidationDemon.py
# Teilen dev May 30th, 2017.

'''
Module in charge to check the deposits of the day.
'''

import urllib
import urllib2
import json
import time, datetime
import hmac,hashlib
import settings

def PoloniexTradingAPI(JSONfile, command, req={}):
    req['command'] = command
    req['nonce'] = int(time.time()*1000)
    encoded_data = urllib.urlencode(req)

    sign = hmac.new(settings.poloniex_secret, \
                    encoded_data, hashlib.sha512).hexdigest()
    headers = {'Sign': sign, 'Key': settings.poloniex_key}

    try:
        ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', \
                              encoded_data, headers))
        json_data = json.loads(ret.read())
        json.dump(json_data, JSONfile)
    except urllib2.HTTPError as err:
        print err

def main():
    GMTcorrection = 18000
    errorGap = 5
    epochDay = (24*60*60)
    while True:
        actualDate = time.strftime("%d/%m/%Y")
        startTimestamp = (int(time.mktime(datetime.datetime.strptime(actualDate, \
                      "%d/%m/%Y").timetuple())) - GMTcorrection) - errorGap

        endTimestamp = startTimestamp + epochDay + (errorGap*2)

        with open("depositPoloniexJSON","wb") as depositData:
            PoloniexTradingAPI(depositData, "returnDepositsWithdrawals", \
                               {"start":startTimestamp, "end":endTimestamp})
        time.sleep(30)

if __name__ == '__main__':
    main()
