### Pseudocode

### client
```py
FUNCTION send_file(filename):
    TRY:
        # Create a TCP socket
        Create client_socket = socket(AF_INET, SOCK_STREAM)

        # Connect to the server using HOST and PORT
        Connect client_socket to (HOST, PORT)

        Print "[+] Connected to the server successfully"

    EXCEPT Exception as e:
        Print "[-] Error creating/connecting socket:", e
        RETURN

    TRY:
        # Open the file in binary read mode
        Open the file with filename as file

        # Loop until the entire file is read
        WHILE data := file.read(BUFFER_SIZE):
            # Send the chunk of data to the server
            client_socket.sendall(data)

        Print "[+] File sent successfully"

    EXCEPT Exception as e:
        Print "[-] Error reading or sending file:", e

    FINALLY:
        # Close the socket
        client_socket.close()

# Main entry point
IF __name__ == "__main__":
    Call send_file("test.txt")
```

### server

```py
FUNCTION start_server():
    TRY:
        # Create a TCP socket
        Create server_socket = socket(AF_INET, SOCK_STREAM)

        # Set socket options to reuse address
        Set server_socket option (SO_REUSEADDR) to 1

        # Bind the socket to HOST and PORT
        Bind server_socket to (HOST, PORT)

        # Start listening for connections (backlog of 5)
        Listen on server_socket with a backlog queue of 5

        Print "[+] Server is listening on port {PORT}"

    EXCEPT Exception as e:
        Print "[-] Error creating/binding socket:", e
        RETURN

    WHILE True:
        TRY:
            # Wait for client connection
            Accept connection from client as (conn, addr)

            Print "[+] Connection accepted from {addr}"

            # Open the output file for writing in binary mode
            Open OUTPUT_FILE in binary write mode as file

            # Receive data in chunks until the client finishes
            WHILE data := conn.recv(BUFFER_SIZE):
                Write data to file

            Print "[+] File received successfully"

        EXCEPT Exception as e:
            Print "[-] Error receiving file:", e

        FINALLY:
            # Close the connection
            Close conn
            Print "[+] Connection closed"

# Main entry point
IF __name__ == "__main__":
    Call start_server()
```