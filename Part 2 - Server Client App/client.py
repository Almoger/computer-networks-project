import socket
import threading

HOST = "YOUR_IP_ADDRESS"
PORT = 10000

def listen_for_messages(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf-8")
            if not msg:
                break

            print(f"\r{msg}\nYou: ")
        except:
            print("\n[DISCONNECTED] Lost connection to server.")
            break


def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))

        name = input("Enter your one-word username: ").strip()
        client.sendall(name.encode("utf-8"))

        threading.Thread(target=listen_for_messages, args=(client,)).start()

        print(f"--- Hello {name}! Type @name message to chat with others ---")
        while True:
            msg = input("You: ")
            if msg.lower() == 'exit':
                break
            if msg:
                client.sendall(msg.encode("utf-8"))

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()