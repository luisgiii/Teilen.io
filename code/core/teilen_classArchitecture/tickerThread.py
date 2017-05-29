import urllib
import urllib2
import json
import time
import hmac,hashlib
import requests

json_data = list()

def start():
    global json_data
    response = requests.get("https://poloniex.com/public?command=returnTicker")
    if response.status_code != 403 and response.status_code != 404:
        json_data = json.loads(response.text)
    else:
        json_data = None

def getTickerResponse():
    return json_data

def main():
    print 'Poloniex Ticker is running...'
    while(1):
        start()
        time.sleep(3)

if __name__ == '__main__':
    main()
