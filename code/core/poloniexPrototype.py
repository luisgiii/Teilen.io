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

    # We convert the 99.5% BTC to the requested crypto and separate the comission from here.
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

    # Start state machine.
    teilenRunning = True
    state = 1

    while(teilenRunning == True):
        if state == 1:
            while(depositValidation == False):
                deposits = PoloniexTradingAPI("returnDepositsWithdrawals", {"start":start_timestamp, "end":end_timestamp}) #! This will be in a separate thread or file.
                print deposits
                for depositIdx in range(0, len(deposits["deposits"])):
                    if deposits["deposits"][depositIdx]["status"] == "COMPLETE":
                        print "[VALIDATED]: Deposit found and complete!"
                        depositValidation = True

            time.sleep(30) #Testing purposes only.
            state = 2

        if state == 2:
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
            state = 3
            time.sleep(10)

        if state == 3:
            # Check if buy order is still open.
            orderOpenCounter = 0
            while(orderOpen == True):
                orderOpenCounter+=1
                checkOrder = PoloniexTradingAPI("returnOpenOrders",{"currencyPair":"BTC_"+exchangeCrypto})
                print checkOrder
                if len(checkOrder) > 0:
                    for orderIdx in range(0, len(checkOrder)):
                        orderFound = False
                        if str(checkOrder[orderIdx]["orderNumber"]) == order:
                            orderFound = True

                        if orderIdx == len(checkOrder)-1:
                            if orderFound != True:
                                orderOpen = False
                else:
                    orderOpen = False
                time.sleep(10)

                if orderOpen == True and orderOpenCounter == 300:
                    # Cancel buy order.
                    cancelOrder = PoloniexTradingAPI("cancelOrder",{"orderNumber":order})
                    if cancelOrder["success"] == 1:
                        # perform a new buy
                        state = 2
            # Outside the while
            state = 4

        if state == 4:
            # Withdraw the converted amount to the exchange address provided above.
            withdrawResult = PoloniexTradingAPI("withdraw",{"currency":exchangeCrypto, "amount":availableCryptoFromBuy, "address":exchangeAddress})
            print "[DEBUG] withdrawResult: " + str(withdrawResult)
            teilenRunning = False

    print "[DEBUG] Teilen: Your exchange was successful!"

if __name__ == "__main__":
    main()
