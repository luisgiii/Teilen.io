# tickerDaemon.py
# Teilen dev May 30th, 2017.

'''
Module in charge of getting the Ticker data from Poloniex.
'''

import json
import time
import requests

'''
Function name:
PoloniexTickerCall(file_name)

Parameters:
* file_name - File object where the JSON dump will be stored.

Makes a Public API call to Poloniex to get the Ticker data from it.
It transforms the response to a JSON format and dumps it in a file object.
'''
def PoloniexTickerCall(JSONfile):
    response = requests.get("https://poloniex.com/public?command=returnTicker")
    if response.status_code != 403 and response.status_code != 404:
        json_data = json.loads(response.text)
        json.dump(json_data, JSONfile)

'''
Function name:
main()

Parameters:
None

Infinite loop where the file object is created and initialized,
and the Ticker API call is performed every 3s.
'''
def main():
    while True:
        whit open("tickerJSON", "wb") as tickerData:
            PoloniexTickerCall(tickerData)
        time.sleep(3)

if __name__ == '__main__':
    main()
