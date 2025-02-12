import time
import hmac
import hashlib
import json
import requests

def getEndpoint(theEndpoint):
    bitso_key = ""
    bitso_secret = ""

    nonce =  str(int(round(time.time() * 1000)))
    http_method = "GET"
    request_path = "/v3/"+theEndpoint+"/"
    json_payload = ""

    #Create signature
    message= nonce+http_method+request_path+json_payload
    signature = hmac.new(bitso_secret.encode('utf-8'), message.encode('utf-8'),hashlib.sha256).hexdigest()

    #Build the auth header
    auth_header = 'Bitso %s:%s:%s' % (bitso_key, nonce, signature)

    # Send request
    response = requests.get("https://api.bitso.com/v3/"+theEndpoint+"/", headers={"Authorization": auth_header})#

    json_data = json.loads(response.text)

    return json_data

def putOrder(m_book, m_side, m_type, m_major, m_price):
    print "placing buy order"
    bitso_key = ""
    bitso_secret = ""

    nonce =  str(int(round(time.time() * 1000)))
    http_method = "POST"
    request_path = "/v3/orders/"
    json_payload = {'book' : m_book, 
                    'side' : m_side, 
                    'type' : m_type, 
                    'major' : m_major, 
                    'price' : m_price}

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
    x=0
    btc = 0
    eth = 0
    putOrder("eth_mxn","sell","limit",1,15000)
    while (0):
        bal = getEndpoint("ticker")
        if bal["success"] == True: 
            btcTmp = bal["payload"][0]["last"]
            ethTmp = bal["payload"][1]["last"]

            if btcTmp <> btc:    
                #print btc
                print bal["payload"][0]["created_at"]+"\t \t"+ bal["payload"][0]["book"],bal["payload"][0]["last"]
                btc = btcTmp
            if ethTmp <> eth:
                #print eth
                print bal["payload"][1]["created_at"], bal["payload"][1]["book"],bal["payload"][1]["last"]
                eth = ethTmp

            time.sleep(2)

if __name__ == "__main__":
    main()