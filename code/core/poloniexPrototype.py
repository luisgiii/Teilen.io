import teilenCryptoAddresses
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
        return requiredCriptoValue, round(amount / float(requiredCriptoValue), 8)
    else:
        return None

def main():
    # User sets amount of BTC he wants to exchange.
    print "Enter the amount of BTC you want to exchange:"
    btcAmount = raw_input()
    # User sets which crypto currency wants in exchange.
    print "What crypto asset would you like to get?:"
    exchangeCrypto = raw_input()

    # We convert the 99.75% BTC to the requested crypto and separate the comission from here.
    comission = float(float(btcAmount)*0.005)
    lowestAsk, convertedAmount = calculateExchangeApproximate(float(btcAmount)*0.995, exchangeCrypto)
    print "You will get approximately: " + str(convertedAmount) + " " + exchangeCrypto

    # Provide a valid address to deposit exchange.
    print "Provide a valid address to deposit your " + exchangeCrypto + "exchange:"
    exchangeAddress = raw_input()

    # Perform a deposit to Teilen account.
    start_timestamp = int(time.time())
    print "Please perform the deposit to the BTC Teilen address: "
    depositValidation = False
    print teilenCryptoAddresses.teilenAddresses["BTC"]
    end_timestamp = start_timestamp + 5 * 60 * 60

    #availableCryptoFromBuy = round(float(convertedAmount)*.9925, 8)
    #print availableCryptoFromBuy
    # Withdraw the converted amount to the exchange address provided above.
    #withdrawResult = PoloniexTradingAPI("withdraw",{"currency":exchangeCrypto, "amount":availableCryptoFromBuy, "address":exchangeAddress})
    #print "[DEBUG] withdrawResult: " + str(withdrawResult)

    while(depositValidation == False):
        deposits = PoloniexTradingAPI("returnDepositsWithdrawals", {"start":start_timestamp, "end":end_timestamp}) #! This will be in a separate thread or file.
        print deposits
        for depositIdx in range(0, len(deposits["deposits"])):
            if deposits["deposits"][depositIdx]["status"] == "COMPLETE":
                print "[VALIDATED]: Deposit found and complete!"
                depositValidation = True

        time.sleep(30) #Testing purposes only.

    buyDone = False
    # Buy the requested amount minus our commission.
    while(buyDone == False):
        buyResult = PoloniexTradingAPI("buy",{"currencyPair":"BTC_"+exchangeCrypto, "rate":lowestAsk, "amount":convertedAmount})
        print buyResult
        if buyResult != None:
            buyDone = True
        time.sleep(2)

    availableCryptoFromBuy = round(float(convertedAmount)*.99, 8)
    order = str(buyResult["orderNumber"])
    orderOpen = True
    print "[DEBUG] order: " + order

    time.sleep(10)

    # Check if buy order is still open.
    while(orderOpen == True):
        checkOrder = PoloniexTradingAPI("returnOpenOrders",{"currencyPair":"BTC_"+exchangeCrypto})
        print checkOrder
        if len(checkOrder) > 0:
            for orderIdx in range(0, len(checkOrder)):
                orderFound = False
                if str(checkOrder[orderIdx]["orderNumber"]) == order:
                    orderFound = True

                if orderIdx == len(checkOrder):
                    if orderFound != True:
                        orderOpen = False
        else:
            orderOpen = False

        time.sleep(10)

    # Withdraw the converted amount to the exchange address provided above.
    withdrawResult = PoloniexTradingAPI("withdraw",{"currency":exchangeCrypto, "amount":availableCryptoFromBuy, "address":exchangeAddress})
    print "[DEBUG] withdrawResult: " + str(withdrawResult)

if __name__ == "__main__":
    main()
