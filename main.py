from binance.client import Client
import time

API_KEY = 'Bp1PsgpLKqjHUYKdLUjrqueqPUHp8l2XxO7xeJM8dnTYtreq68FzclQWzlF9k9UP'
API_SECRET = '6h3FbmXSzgtvCjN3BMjsM0CnKr3FOPrpEHKShJU6Hp2bCFgrF9LIvkIqY7H1QnGr'

client = Client(API_KEY,API_SECRET,testnet = True)

balance = client.get_account()
symbol = 'BTCUSDT'
buy_price_threshold = 68250
sell_price_threshold = 68290
trade_quantity = 0.001


def udapte_file(filename,update,log):
    with open(filename,update) as file:
        file.write(log)

def get_current_price(symbol):
    ticker = client.get_symbol_ticker(symbol = symbol)
    return float(ticker['price'])

def place_buy_order(symbol,quantity):
    order = client.order_market_buy(symbol = symbol , quantity = quantity)
    print(f"buy order done : {order}")
    return order

def place_sell_order(symbol,quantity):
    order = client.order_market_sell(symbol = symbol , quantity = quantity)
    print(f"sell order done : {order}")
    return order

def trading_bot():
    in_position = False
    

    while True : 
        current_price = get_current_price(symbol)
       
        print(f"current price of {symbol} :  {current_price}")
      

        if not in_position:
            if current_price < buy_price_threshold:
                print(f"Price is below {buy_price_threshold}. Placing buy order.")
                order = place_buy_order(symbol,trade_quantity)
                udapte_file("log.txt",'a',f"buy order \n {order} \n"  )
                in_position= True
        else:
            if current_price > sell_price_threshold:
                print(f"Price is above {sell_price_threshold}. Placing sell order.")
                order = place_sell_order(symbol,trade_quantity)
                udapte_file("log.txt",'a',f"sell order \n {order} \n"  )
                in_position= False

        time.sleep(3)



if __name__ == "__main__":
    trading_bot()