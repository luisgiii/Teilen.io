import poloniexKeys
import urllib
import urllib2
import json
import time
import hmac,hashlib
import requests

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

    sign = hmac.new(poloniexKeys.poloniex_secret, encoded_data, hashlib.sha512).hexdigest()
    headers = {'Sign': sign, 'Key': poloniexKeys.poloniex_key}

    try:
        ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', encoded_data, headers))
        jsonRet = json.loads(ret.read())
        return jsonRet
    except urllib2.HTTPError as err:
        print err

def calculateExchangeApproximate(amount, crypto):
    requiredCriptoValue = PoloniexTickerQuery("BTC_"+crypto) #! This will be in a separate thread or file.
    if requiredCriptoValue != None:
        return maxAmount = round(amount / float(requiredCriptoValue), 8)
    else:
        return None
def main():
    # User sets amount of BTC he wants to exchange.
    print "Enter the amount of BTC you want to exchange:"
    btcAmount = raw_input()
    # User sets which crypto currency wants in exchange.
    print "What crypto asset would you like to get?:"
    exchangeCrypto = raw_input()

    # We convert the 99% BTC to the requested crypto and separate the comission from here.
    comission = float(float(btcAmount)*0.01)
    convertedAmount = calculateExchangeApproximate(float(btcAmount)*0.99, exchangeCrypto) 
    print "You will get approximately: " + convertedAmount + exchangeCrypto
    
    # Perform a deposit to Teilen account.
    
    
if __name__ == "__main__":
    main()
