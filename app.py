import yfinance as yf
import redis

red = redis.Redis(host='localhost', port=6379, db=0)

def curr_price(symbol):
    ticker = yf.Ticker(symbol)
    price = ticker.info['regularMarketPrice']
    return price

s1 = "^GSPC"
s2 = "^DJI"
s3 = "^IXIC"

p1 = curr_price(s1)
red.set(s1,p1)
print(p1)

p2 = curr_price(s2)
red.set(s2,p2)
print(p2)

p3 = curr_price(s3)
red.set(s3,p3)
print(p3)
