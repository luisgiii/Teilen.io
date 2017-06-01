# etherBlockchainAPI.py
# Teilen dev June 1st, 2017.

'''
Module in charge of getting the Ethereum blockchain data.
'''

import json
import time, datetime
import requests
import settings

def getLatestBlocks():
    response = requests.get("https://etherchain.org/api/blocks/0/10")
    if response.status_code != 403 and response.status_code != 404:
        json_data = json.loads(response.text)
        return json_data

def getBlockTx(blockNumber):
    response = requests.get("https://etherchain.org/api/block/"+str(blockNumber)+"/tx")
    if response.status_code != 403 and response.status_code != 404:
        json_data = json.loads(response.text)
        return json_data

def convertDate2Timestamp(date):
    GMTcorrection = 18000
    dateEncoded = str(date)
    calendar, hours = dateEncoded.split("T")
    hour, minutes, secs = hours.split(":")
    secA, secB = secs.split(".")
    unixDate = calendar+" "+hour+":"+minutes+":"+secA
    timestamp = int(time.mktime(datetime.datetime.strptime(unixDate, \
                  "%Y-%m-%d %H:%M:%S").timetuple()))
    return timestamp - GMTcorrection #!GMT timestamp

def getTxidFromBlock(txTimestamp):
    blockData = getLatestBlocks()
    for block in range(0, len(blockData["data"])):
        blockNumber = blockData["data"][block]["number"]
        txFromBlock = getBlockTx(blockNumber)
        for tx in range(0, len(txFromBlock["data"])):
            if txFromBlock["data"][tx]["recipient"] == settings.eth_address:
               timestamp = convertDate2Timestamp(txFromBlock["data"][tx]["time"])
               if timestamp >= txTimestamp:
                   return txFromBlock["data"][tx]["hash"]
               else:
                   return None
