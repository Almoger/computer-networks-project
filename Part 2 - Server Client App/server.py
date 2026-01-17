import socket
import threading

##-------- Set SERVER_IP to the private IP address of the computer that will run the server --------##
##-------- Set PORT to any available port that isnt in use by another service --------##
SERVER_IP = "localhost"
SERVER_PORT = 12000

online_clients = {}
clients_lock = threading.Lock()

def handle_client_input(client_socket, addr):

    formatted_addr = f"{addr[0]}:{addr[1]}"
    username = None

    while True:
        try:
            username = client_socket.recv(1024).decode('utf-8').strip()

            with clients_lock:
                if not username or (" " in username):
                    client_socket.sendall("INVALID_NAME".encode('utf-8'))
                elif username in online_clients:
                    client_socket.sendall("NAME_TAKEN".encode('utf-8'))
                else:
                    online_clients[username] = {"socket": client_socket, "address": formatted_addr}
                    break # break the loop when name is finally valid

        except (ConnectionResetError, ConnectionAbortedError):
            print(f"[SERVER] Unexpected disconnect from client {formatted_addr} (username: '{username}').")
            client_socket.close()
            return

    print(f"[SERVER] Client {formatted_addr} has successfully registered as '{username}'.")

    try:
        client_socket.sendall("WELCOME".encode('utf-8'))

        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data or data == "EXIT":
                break

            if data.startswith("@") and " " in data:
                # 1st character of data is @, so skip it with data[1:]
                # cut by 1st space so the 1st word = name, after 1st word - msg
                parts = data[1:].split(" ", maxsplit=1)
                target_name = parts[0]
                message_content = parts[1]

                if target_name == username:
                    client_socket.sendall(f"CANT_MESSAGE_SELF".encode("utf-8"))
                    continue

                with clients_lock:

                    if not target_name in online_clients:
                        client_socket.sendall(f"[SYSTEM]: User '{target_name}' was not found.".encode("utf-8"))
                        continue

                    target_socket = online_clients[target_name]["socket"]
                    target_ip = online_clients[target_name]["address"]

                    target_socket.sendall(f"Message from {username}: {message_content}".encode("utf-8"))
                    print(f"[LOG] {username} ({formatted_addr}) -> {target_name} ({target_ip}): {message_content}")
            else:
                client_socket.sendall("WRONG_USAGE".encode("utf-8"))

    except (ConnectionResetError, ConnectionAbortedError):
        print(f"[SERVER] Unexpected disconnect from client {formatted_addr} (username: '{username}').")

    finally:
        with clients_lock:
            if username in online_clients:
                online_clients.pop(username, None)

        # print this whether the client disconnected willingly or not
        print(f"[SERVER] Client {formatted_addr} (username: '{username}') has disconnected from server.")
        client_socket.close()

def start_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((SERVER_IP, SERVER_PORT))
        server_socket.listen()

        print(f"[SERVER] Server ONLINE. Listening on {SERVER_IP}:{SERVER_PORT}...")

        while True:
            # whenever a new client connects, accept his connection
            client_sock, client_addr = server_socket.accept()

            # create new client thread to allow the server to handle multiple clients at once.
            # without the new thread, the server would be stuck with one user and wouldn't be able to accept new connections from others
            client_thread = threading.Thread(target=handle_client_input, args=(client_sock, client_addr))
            client_thread.start()

            print(f"[SERVER] Online users count: {threading.active_count() - 1}")

    except socket.gaierror:
        print(f"[SERVER] Hostname '{SERVER_IP}' is invalid. Restart program with different address/hostname.")

    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")


if __name__ == "__main__":
    start_server()
