import socket  # handles communication over TCP/IP
import os      # handles file handling or file checks

# Constants
HOST = "0.0.0.0"  # Listen on all available interfaces
PORT = 8080
BUFFER_SIZE = 1024
OUTPUT_FILE = "test2.txt"

def start_server():
    try:
        # Create a socket (IPv4, TCP)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Reuse address without waiting for the operating system's timeout when restarting the server.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        # backlog queue of 5 pending connections
        server_socket.listen(5)
        print(f"[+] Server is listening on port {PORT}")
    except Exception as e:
        print(f"[-] Error creating/binding socket: {e}")
        return

    while True:
        try:
            # Wait for client connection
            conn, addr = server_socket.accept()
            print(f"[+] Connection accepted from {addr}") # IP or port

            with open(OUTPUT_FILE, "wb") as file:
                while (data := conn.recv(BUFFER_SIZE)): 
                    file.write(data)
            print("[+] File received successfully")
        except Exception as e:
            print(f"[-] Error receiving file: {e}")
        finally:
            conn.close()
            print("[+] Connection closed")

if __name__ == "__main__":
    start_server()
