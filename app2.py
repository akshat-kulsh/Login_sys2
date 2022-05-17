import requests
import redis
import time
import json

red = redis.Redis(host='localhost', port=6379, db=0)

URL = "https://www.bitmex.com/api/v1/instrument"

crypto1 = "XBT"
crypto2 = "ETHUSD"



while(True):
    def fetch_price(symb_name):
        PARAMS = {'symbol':symb_name}
        r=requests.get(url=URL, params=PARAMS)
        data = r.json()
        return data[0]["lastPrice"]

    def dict_update(symb_name, price):
        global res
        res = {"symbol":"", "price":""}
        res.update({'symbol':symb_name, 'price': price})
        res = json.dumps(res)
        return res

    priceXBT = fetch_price(crypto1)
    pubXBT = dict_update(crypto1, priceXBT)
    red.publish('pricingData', pubXBT)

    priceETHUSD =  fetch_price(crypto2)
    pubETHUSD = dict_update(crypto2, priceETHUSD)
    #red.set(crypto2, priceETHUSD)
    red.publish('pricingData', pubETHUSD)
    time.sleep(20)