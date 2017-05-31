# apiBridge.py
# Teilen dev May 30th, 2017.

'''
Module in charge to get the transaction fee of every crypto currency.
'''

import json
import time
import requests

'''
Function name:
PoloniexCurrencyCall(file_name)

Parameters:
* file_name - File object where the JSON dump will be stored.

Makes a Public API call to Poloniex to get the fee data from it.
It transforms the response to a JSON format and dumps it in a file object.
'''
def PoloniexCurrencyCall(JSONfile):
    response = requests.get("https://poloniex.com/public?command=returnCurrencies")
    if response.status_code != 403 and response.status_code != 404:
        json_data = json.loads(response.text)
        json.dump(json_data, JSONfile)

'''
Function name:
main()

Parameters:
None

Infinite loop where the file object is created and initialized,
and the returnCurrencies API call is performed every 3600s.
'''
def main():
    while True:
        with open("feeJSON", "wb") as feeData:
            PoloniexCurrencyCall(feeData)
        time.sleep(3600)

if __name__ == '__main__':
    main()
