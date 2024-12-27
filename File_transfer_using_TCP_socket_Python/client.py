import socket

# Constants
HOST = "127.0.0.1"  # Change to the server's IP if needed
PORT = 8080
BUFFER_SIZE = 1024  # size of data chunk

def send_file(filename):
    try:
        # Create a socket (IPv4, TCP)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        print("[+] Connected to the server successfully")
    except Exception as e:
        print(f"[-] Error creating/connecting socket: {e}")
        return

    try:
        with open(filename, "rb") as file:
            while (data := file.read(BUFFER_SIZE)):
                client_socket.sendall(data)     # Sends the chunk of data to the server
        print("[+] File sent successfully")
    except Exception as e:
        print(f"[-] Error reading or sending file: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    send_file("test.txt")
