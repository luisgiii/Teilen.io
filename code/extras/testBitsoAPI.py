import time
import hmac
import hashlib
import requests
import json

# API credentials
bitso_key = ""
bitso_secret = ""

# Available books.
btc_book = "btc_mxn"
eth_book = "eth_mxn"

# Essential values
marketValueWhenSoldBtc = 0

def Ticker():
    nonce =  str(int(round(time.time() * 1000)))
    http_method = "GET"
    request_path = "/v3/ticker/"
    query_payload = {'book' : 'btc_mxn'}

    # Create signature
    message = nonce+http_method+request_path+str(query_payload)
    signature = hmac.new(bitso_secret.encode('utf-8'),
                                                message.encode('utf-8'),
                                                hashlib.sha256).hexdigest()

    # Build the auth header
    auth_header = 'Bitso %s:%s:%s' % (bitso_key, nonce, signature)

    # Send request
    response = requests.get("https://api.bitso.com/v3/ticker/",
    headers={"Authorization": auth_header}, params=query_payload)
    print response.text
    json_data = json.loads(response.text)

    #return json_data["success"], float(json_data["payload"]["last"])

def CurrentFundsRequester():
    nonce =  str(int(round(time.time() * 1000)))
    http_method = "GET"
    request_path = "/v3/balance/"
    json_payload = ""

    # Create signature
    message = nonce+http_method+request_path+json_payload
    signature = hmac.new(bitso_secret.encode('utf-8'),
                                                message.encode('utf-8'),
                                                hashlib.sha256).hexdigest()

    # Build the auth header
    auth_header = 'Bitso %s:%s:%s' % (bitso_key, nonce, signature)

    # Send request
    response = requests.get("https://api.bitso.com/v3/balance/",
    headers={"Authorization": auth_header})
    print response.text
    json_data = json.loads(response.text)
    return json_data["success"], json_data["payload"]["balances"][2]["available"]

def GetMethodTest():
    print "Inside GET method test."
    nonce =  str(int(round(time.time() * 1000)))
    http_method = "GET"
    request_path = "/v3/available_books/"
    json_payload = ""

    # Create signature
    message = nonce+http_method+request_path+json_payload
    #print message
    signature = hmac.new(bitso_secret.encode('utf-8'),
                                                message.encode('utf-8'),
                                                hashlib.sha256).hexdigest()

    # Build the auth header
    auth_header = 'Bitso %s:%s:%s' % (bitso_key, nonce, signature)
    # Send request
    response = requests.get("https://api.bitso.com/v3/available_books/",
    headers={"Authorization": auth_header})

    print response.text

def PostMethodTest():
    print "Inside POST method test."
    nonce =  str(int(round(time.time() * 1000)))
    http_method = "POST"
    request_path = "/v3/phone_number/"
    json_payload = {'phone_number' : '6691614615'}

    # Create signature
    message = nonce+http_method+request_path+json.dumps(json_payload)
    print message
    signature = hmac.new(bitso_secret.encode('utf-8'),
                                                message.encode('utf-8'),
                                                hashlib.sha256).hexdigest()

    # Build the auth header
    auth_header = 'Bitso %s:%s:%s' % (bitso_key, nonce, signature)
    # Send request
    response = requests.post("https://api.bitso.com/v3/phone_number/",
    headers={"Authorization": auth_header}, json=json_payload)

    print response.text

def PlaceBuyOrder(buyAmount):
    print "Placing Buying order"
    nonce =  str(int(round(time.time() * 1000)))
    http_method = "POST"
    request_path = "/v3/orders/"
    json_payload = {'book' : 'btc_mxn', 'side' : 'buy', 'type' : 'market',
                    'major' : buyAmount}

    # Create signature
    message = nonce+http_method+request_path+json.dumps(json_payload)
    print message
    signature = hmac.new(bitso_secret.encode('utf-8'),
                                                message.encode('utf-8'),
                                                hashlib.sha256).hexdigest()

    # Build the auth header
    auth_header = 'Bitso %s:%s:%s' % (bitso_key, nonce, signature)
    # Send request
    response = requests.post("https://api.bitso.com/v3/orders/",
    headers={"Authorization": auth_header}, json=json_payload)

    print response.text


def PlaceSellOrder(sellAmount):
    print "Placing Selling order"
    nonce =  str(int(round(time.time() * 1000)))
    http_method = "POST"
    request_path = "/v3/orders/"
    json_payload = {'book' : 'btc_mxn', 'side' : 'sell', 'type' : 'market',
                    'major' : sellAmount}

    # Create signature
    message = nonce+http_method+request_path+json.dumps(json_payload)
    print message
    signature = hmac.new(bitso_secret.encode('utf-8'),
                                                message.encode('utf-8'),
                                                hashlib.sha256).hexdigest()

    # Build the auth header
    auth_header = 'Bitso %s:%s:%s' % (bitso_key, nonce, signature)
    # Send request
    response = requests.post("https://api.bitso.com/v3/orders/",
    headers={"Authorization": auth_header}, json=json_payload)

    print response.text


def main():
    #Ticker()
    GetMethodTest()
    #success, ethValue = CurrentFundsRequester()
    #print

if __name__ == "__main__":
    main()
