import socket
from socket import AF_INET, SOCK_STREAM
import gradio


def initiate_client_server():
    new_client = socket.socket(AF_INET, SOCK_STREAM)

    # Connecting to stock exchange.
    stock_exchange_port = 8737
    new_client.connect((socket.gethostname(), stock_exchange_port))
    print("Connection Established with the Stock Exchange.\n")

    return new_client

def UserInterface(Operation, Stock, Quantity):
    client = initiate_client_server()
    command = Operation + " " + Stock + " " + str(Quantity)
    info_display = "(TCP Connection Established with the Stock Exchange Server)\n"

    while True:
        client.send(command.encode())
        response = client.recv(1024).decode()
        break

    return info_display + response


if __name__ == "__main__":
    gradio.Interface(
        fn=UserInterface,
        inputs=[gradio.Radio(["Buy", "Sell"]), "text", gradio.Slider(0, 25, step=1)],
        outputs="text",
    ).launch()
