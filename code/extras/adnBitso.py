import time
import hmac
import hashlib
import json
import requests

def signIt(theRequest):
    bitso_key = ""
    bitso_secret = ""
    print "Signing..."
    nonce =  str(int(round(time.time() * 1000)))
    http_method = "GET"
    request_path = "/v3/"+theRequest+"/"
    json_payload = ""

    #Create signature
    message= nonce+http_method+request_path+json_payload
    signature = hmac.new(bitso_secret.encode('utf-8'), message.encode('utf-8'),hashlib.sha256).hexdigest()

    #Build the auth header
    auth_header = 'Bitso %s:%s:%s' % (bitso_key, nonce, signature)

    # Send request
    response = requests.get("https://api.bitso.com/v3/"+theRequest+"/", headers={"Authorization": auth_header})#

    json_data = json.loads(response.text)

    print json_data["success"], json_data["payload"]["balances"][3]["total"]

  #  print response.content

def asd():
    print ""

def main():
    signIt("balance")

if __name__ == "__main__":
    main()