import socket
import threading

# set host ip and port to your desired values
SERVER_IP = "localhost"
PORT = 10000

active_clients = {}
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
                elif username in active_clients:
                    client_socket.sendall("NAME_TAKEN".encode('utf-8'))
                else:
                    active_clients[username] = {"socket": client_socket, "address": formatted_addr}
                    break # break the loop since name is finally valid

        except Exception as e:
            print(f"[ERROR] Handshake failed: {e}")
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
                parts = data[1:].split(" ", 1) # cut by 1st space: first word is the name, second word is the msg
                target_name = parts[0]
                message_content = parts[1]

                if target_name == username:
                    client_socket.sendall(f"CANT_MESSAGE_SELF".encode("utf-8")) # SYSTEM: Cannot send messages to yourself.
                    continue

                with clients_lock:

                    if not target_name in active_clients:
                        client_socket.sendall(f"SYSTEM: User '{target_name}' not found.".encode("utf-8"))
                        continue

                    target_socket = active_clients[target_name]["socket"]
                    target_ip = active_clients[target_name]["address"]

                    target_socket.sendall(f"Message from {username}: {message_content}".encode("utf-8"))
                    print(f"[LOG] {username} ({formatted_addr}) -> {target_name} ({target_ip}): {message_content}")
            else:
                client_socket.sendall("WRONG_USAGE".encode("utf-8"))

    except ConnectionResetError:
        print(f"[SERVER] Unexpected disconnect from client {formatted_addr} (username: '{username}').")

    finally:
        with clients_lock:
            if username in active_clients:
                active_clients.pop(username, None)

        # print this whether the client disconnected willingly or not
        print(f"[SERVER] Client {formatted_addr} (username: '{username}') has disconnected from server.")
        client_socket.close()

def start_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((SERVER_IP, PORT))
        server_socket.listen()

        print(f"[SERVER] Server ONLINE. Listening on {SERVER_IP}:{PORT}...")
        print("[SERVER] Press Ctrl+C to shut down.")

        while True:
            client_sock, client_addr = server_socket.accept() # whenever a new client connects, it accepts the connection
            client_thread = threading.Thread(target=handle_client_input, args=(client_sock, client_addr))
            client_thread.start()

            print(f"[SERVER] Online users count: {threading.active_count() - 1}")

    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")


if __name__ == "__main__":
    start_server()