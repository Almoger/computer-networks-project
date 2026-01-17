import socket
import threading

##---- Make sure you set SERVER_IP & SERVER_PORT to the same values defined in server.py ----##
SERVER_IP = "localhost"
SERVER_PORT = 12000

# client waits for server responses and for other clients' messages (given to him by the server)
def listen_for_messages(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf-8")
            if not msg:
                break

            if msg == "CANT_MESSAGE_SELF":
                print("[ERROR] You cannot send messages to yourself!")
            elif msg == "WRONG_USAGE":
                print(f"[SYSTEM] Usage: @name <message>")
            else:
                print(f"\r{msg}\n ", end="") # prints the incoming messages to the client
        except (ConnectionResetError, KeyboardInterrupt, ConnectionAbortedError):
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_IP, SERVER_PORT))
        print(f"[SYSTEM] Connected to {SERVER_IP}:{SERVER_PORT}")

        # input name until it is a valid name
        while True:
            name = input("Enter your one-word username: ").strip()
            client.sendall(name.encode("utf-8"))

            response = client.recv(1024).decode("utf-8")

            if response == "INVALID_NAME":
                print("[ERROR] Username is invalid. Make sure it is a single word and not empty.")
            elif response == "NAME_TAKEN":
                print("[ERROR] Username is already taken. Retry with another name.")
            elif response == "WELCOME":
                print(f"[SYSTEM] WELCOME {name}. To chat, type: @target <message>")
                break

        # start a background thread to listen for incoming messages from the server.
        # it prevents the program from getting stuck at client input (o/w the client won't receive data)
        threading.Thread(target=listen_for_messages, args=(client,)).start()

        # main thread for input
        while True:
            msg = input()
            if not msg:
                continue
            if msg.lower() == 'exit':
                client.sendall("EXIT".encode("utf-8"))
                print("\n[SYSTEM] Disconnected from server.")
                break
            client.sendall(msg.encode("utf-8"))

    except (ConnectionResetError, KeyboardInterrupt, ConnectionAbortedError):
        print("\n[SYSTEM] Lost connection to server.")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()
