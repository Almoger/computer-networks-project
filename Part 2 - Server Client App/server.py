import socket
import threading

SERVER_IP = "SERVER_IP"
PORT = 10000
BUFFER_SIZE = 1024

active_clients = {}
clients_lock = threading.Lock()

def handle_client(client_socket, addr):
    username = None
    try:
        username = client_socket.recv(1024).decode('utf-8').strip()

        with clients_lock:
            if not username or username in active_clients:
                client_socket.sendall("ERROR: Username taken or invalid.".encode('utf-8'))
                client_socket.close()
                return

            active_clients[username] = {
                "socket": client_socket,
                "address": addr
            }

            print(f"[SERVER] Client {addr} has successfully registered as {username}.")
            client_socket.sendall(f"WELCOME {username}. To chat, type: @target_name <message>".encode('utf-8'))

        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            if data == "exit":
                break

            if data.startswith("@") and " " in data:
                # cut by 1st space: first word is the name, second word is the msg
                parts = data[1:].split(" ", 1)
                target_name = parts[0]
                message_content = parts[1]

                with clients_lock:
                    if target_name == username:
                        client_socket.sendall(f"SYSTEM: Cannot send messages to yourself.".encode("utf-8"))
                    elif target_name in active_clients:
                        target_socket = active_clients[target_name]["socket"]
                        target_ip = active_clients[target_name]["address"]

                        target_socket.sendall(f"Message from {username}: {message_content}".encode("utf-8"))
                        print(f"[LOG] {username} ({addr}) -> {target_name} ({target_ip}): {message_content}")
                    else:
                        client_socket.sendall(f"SYSTEM: User '{target_name}' not found.".encode("utf-8"))
            else:
                client_socket.sendall("SYSTEM: Use @name message format.".encode("utf-8"))

    except Exception as e:
        print(f"[ERROR] {e} (issued by {username})")
    finally:
        with clients_lock:
            if username in active_clients:
                active_clients.pop(username, None)

        client_socket.close()
        print(f"[SERVER] {username} left.")

def start_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((SERVER_IP, PORT))
        server_socket.listen()

        print(f"[SERVER] Listening on {SERVER_IP}:{PORT}...")
        print("[SERVER] Press Ctrl+C to shut down.")

        while True:
            client_sock, client_addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_sock, client_addr))
            client_thread.start()

            print(f"[STATUS] Active clients connected: {len(active_clients)}")

    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")


if __name__ == "__main__":
    start_server()