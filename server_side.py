import socket 
import pickle
import random as rd
from socket import AF_INET, SOCK_STREAM



def initialize_server(port: int):
    server_socket = socket.socket(AF_INET,  SOCK_STREAM)
    server_socket.bind((socket.gethostname(), port))
    server_socket.listen(1)

    return server_socket

def get_client_bal():
    with open("ClientBal.txt", "r") as f:
        bal = int(f.read())
    
    return bal

def overwrite_client_bal(new_bal:int):
    with open("ClientBal.txt", "w") as f:
        f.write(str(new_bal))

def write_to_db(new_db):
    with open("ClientStockDB.pk", "wb") as handle:
        pickle.dump(new_db, handle, protocol=pickle.HIGHEST_PROTOCOL)

def trade(operation, stock_name, qty):
    with open("ClientStockDB.pk", "rb") as db:
        load_db:dict = pickle.load(db)

    client_balance = get_client_bal()
    stock_price = rd.randint(0, 1000)
    qty = int(qty)

    if (operation.lower() == "buy"):
        buy_value = stock_price * qty
        if load_db.get(stock_name) is None:
            load_db[stock_name] = qty
        else : load_db[stock_name] += qty

        client_balance -= stock_price * qty
        write_to_db(load_db)
        overwrite_client_bal(client_balance)
        return f"Successfully Bought {qty} shares of {stock_name} for ${buy_value}. \nClient Balance : ${client_balance}"
    
    elif (operation.lower() == "sell"):
        if load_db.get(stock_name) is None:
            return f"You do not currently own any {stock_name} stocks!"
        elif (load_db[stock_name] - qty < 0):
            return f"You do not own enough {stock_name} stocks!"
        
        sell_value = stock_price * qty
        client_balance += sell_value
        
        load_db[stock_name] -= qty
        if (load_db[stock_name] == 0) : del load_db[stock_name]
        
        write_to_db(load_db)
        overwrite_client_bal(client_balance)
        return f"Successfully Sold {qty} shares of {stock_name} for ${sell_value}. \nClient Balance : ${client_balance}"

    return f"Trade couldn't be locked due to insufficient balance or the unavailability of stocks. \nClient Balance : ${get_client_bal()}"


def execute_command(data):
    command:list = data.decode().split()
    # command example : buy/sell stock_name stock_qty
    return trade(*command)


def main():
    server = initialize_server(port=8737)
    while True:
        try:
            connection_socket, addr = server.accept()
            data = connection_socket.recv(1024)
            trade_res = execute_command(data)
            connection_socket.send(trade_res.encode())

        except KeyboardInterrupt:
            # Terminating Server-Client Connection
            connection_socket.close()
            break

if __name__ == "__main__":
    main()