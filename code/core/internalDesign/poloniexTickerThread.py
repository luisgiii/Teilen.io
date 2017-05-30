import json
import time
import requests
import os

def PoloniexTickerCall(JSONfile):
    response = requests.get("https://poloniex.com/public?command=returnTicker")
    if response.status_code != 403 and response.status_code != 404:
        json_data = json.loads(response.text)
        json.dump(json_data, JSONfile)

def main():
    #tickerData = open("tickerJSON", "wb")
    for repeat in range(0,2):
        tickerData = open("tickerJSON", "wb")
        PoloniexTickerCall(tickerData)
        time.sleep(3)
        tickerData.close()
if __name__ == '__main__':
    main()
