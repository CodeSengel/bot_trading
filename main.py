#bibliothèque à importer
from binance.client import Client
import time

# Clés à récupérer de ton compte (µAttention , à ne pas montrer !!!!)

API_KEY = "VOTRE cle API"
API_SECRET = "VOTRE cle secrete"

# Connexion à ton compte 
client = Client(API_KEY,API_SECRET,testnet = True)

# initialisation des variables : 

balance = client.get_account() # récupérer la liste des actifs : ton portefeuille 
symbol = 'BTCUSDT'             # paire à trader
buy_price_threshold = 68250    # seuil de prix d'achat 
sell_price_threshold = 68290   # seuil de prix de vente 
trade_quantity = 0.001         # quantité à trader


# fonction qui sert à mettre à jour le fichier log.txt dans la racine (pour avoir tout l'historique des mouvement et des ordres placés
def udapte_file(filename,update,log):
    with open(filename,update) as file:
        file.write(log)

# récupérer le prix actuel de la paire à trader 
def get_current_price(symbol):
    ticker = client.get_symbol_ticker(symbol = symbol)
    return float(ticker['price'])

#placer un order d'achat
def place_buy_order(symbol,quantity):
    order = client.order_market_buy(symbol = symbol , quantity = quantity)
    print(f"buy order done : {order}")
    return order
# placer un ordre de vente 
def place_sell_order(symbol,quantity):
    order = client.order_market_sell(symbol = symbol , quantity = quantity)
    print(f"sell order done : {order}")
    return order

# fonction principale pour lancer le bot 
def trading_bot():
    in_position = False # condition 
    while True : 
        current_price = get_current_price(symbol) # récupérer le prix actuel de la paire à trader 
       
        print(f"current price of {symbol} :  {current_price}") # afficher le prix 
      

        if not in_position: # si une position d'achat n'a pas été initiée
            if current_price < buy_price_threshold: # si le prix est sous le seuil d'achat 
                print(f"Price is below {buy_price_threshold}. Placing buy order.")
                order = place_buy_order(symbol,trade_quantity) # placer l'ordre d"achat 
                udapte_file("log.txt",'a',f"buy order \n {order} \n"  ) # mettre à jour le fichier log.txt
                in_position= True # fermer la position
        else: # si une position de vente  n'a pas été initiée
            if current_price > sell_price_threshold: # si le prix est audessus le seuil de vente 
                print(f"Price is above {sell_price_threshold}. Placing sell order.")
                order = place_sell_order(symbol,trade_quantity) # placer l'ordre de vente 
                udapte_file("log.txt",'a',f"sell order \n {order} \n"  ) # mettre à jour le fichier log.txt
                in_position= False # fermer la position

        time.sleep(3) # rafraichir toutes les 3 secondes 



if __name__ == "__main__":
    trading_bot()
