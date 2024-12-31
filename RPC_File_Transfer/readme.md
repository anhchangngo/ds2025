## RPC
RPC (Remote Procedure Call) is a network technical model, a communication protocol between software (or processes) that allows a program to request a service from another program located on a different computer/server, or simply put, it is a method of calling a function from a remote computer to retrieve a result.

RPC use model client-sever. 

RPC is used when the client and server are not on the same system.

## gRPC
gRPC is an open-source RPC framework that is modern, high-performance, and can run in any environment.

Implementing gRPC is also very simple. On the server side, it will provide function calls and run a gRPC server to handle the function calls provided by the client. On the client side, there is a gRPC Stub (referred to as the gRPC client corresponding to the language of that service) that provides functions similar to those on the server side.

### file_transfer.proto
"contract" between client and server in the gRPC system.

```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. file_transfer.proto
```
- file_transfer_pb2.py: Defines the messages (FileChunk, TransferStatus). 
- file_transfer_pb2_grpc.py: Contains the FileTransferStub class for the client and FileTransferServicer for the server implementation.

Client: 
- The client calls the UploadFile method and sends FileChunks. 
- The .proto file ensures that the client packages the data in the correct structure (filename, data). 

Server: 
- The server receives the stream of FileChunks from the client and processes each chunk. 
- The .proto file ensures that the server correctly understands the structure of the received data.


### rpc_client.py
- Connect to the gRPC server.
- Read the content of the file to be transmitted and split it into chunks.
- Send these chunks to the server via the RPC method UploadFile.
- Receive feedback from the server about the status of the file transfer process.

Channel is the bridge between the client and server in the gRPC system. 

It: 
- Creates a logical connection to the server. 
- Manages communication over the network. 
- Serves as the foundation for executing RPC calls.

Yield:
``yield file_transfer_pb2.FileChunk(filename = filename, data = chunk)``

create and send a FileChunk object to the server in each call of the generator.

test.txt ``Hello, this is a test file for RPC.``
- Iteration 1: ``yield FileChunk(filename="test.txt", data="Hello, thi")``
- Iteration 2: ``yield FileChunk(filename="test.txt", data="s is a te")``
- Iteration 3: ``yield FileChunk(filename="test.txt", data="st file f")``
- Iteration 4: ``yield FileChunk(filename="test.txt", data="or RPC.")``


```
dat@LAPTOP-4BOGORQ8:/ds2025/RPC_File_Transfer$ python3 rpc_server.py
Server is running on port 50051...
```

```
dat@LAPTOP-4BOGORQ8:/ds2025/RPC_File_Transfer$ python3 rpc_client.py
File uploaded successfully
```

### Pesudocode

file_transfer.proto

```
syntax = "proto3";

service FileTransfer {
    rpc UploadFile (stream FileChunk) returns (TransferStatus);
}

// stream FileChunk : client will send multiple packets (chunks) consecutively instead of a single large packet.

message FileChunk {
    string filename = 1; // Tên file đang được truyền
    bytes data = 2;     // Dữ liệu nhị phân của file
}

// message : data structure that the client and server exchange.

message TransferStatus {
    string message = 1;     // Upload status notification (e.g., "Success" or "Error")
}
```

rpc_client
```py
FUNCTION upload_file(filename):
    TRY:
        # Step 1: Create a gRPC connection channel to the server
        Create channel = grpc.insecure_channel("localhost:50051")

        # Step 2: Create a stub for calling server RPC methods
        Create stub = FileTransferStub(channel)

        # Step 3: Define a generator function to split file into chunks
        FUNCTION generate_chunks():
            TRY:
                Open the file in binary read mode (filename) as file
                WHILE (chunk = file.read(1024)):  # Read 1024 bytes at a time
                    # Yield each chunk along with the filename
                    Yield FileChunk(filename=filename, data=chunk)

            EXCEPT FileNotFoundError:
                Print "Error: File not found"
                RETURN
        END FUNCTION

        # Step 4: Call the server's UploadFile RPC method using the chunk generator
        Call stub.UploadFile(generate_chunks())

        # Step 5: Print the server's response message
        Print "File upload response: ", response.message

    EXCEPT Exception as e:
        Print "Error: ", e
END FUNCTION

# Main entry point
IF __name__ == "__main__":
    Call upload_file("test.txt")
```

rpc_server
```py
CLASS FileTransferService(FileTransferServicer):
    FUNCTION UploadFile(request_iterator, context):
        TRY:
            # Step 1: Get the first chunk to determine the file name
            first_chunk = Get the first element from request_iterator

            # Step 2: Construct the file path (e.g., './uploaded_files/test.txt')
            filepath = Join "./uploaded_files" with the base name of first_chunk.filename

            # Step 3: Create the output directory if it doesn't exist
            Create directory at filepath if not exists

            # Step 4: Write the chunks to the output file
            Open filepath in binary write mode as file
            Write first_chunk.data to file
            FOR each chunk in request_iterator:
                Write chunk.data to file

            # Step 5: Return success status
            RETURN TransferStatus(message="File uploaded successfully")

        EXCEPT Exception as e:
            # Step 6: Return error status in case of failure
            RETURN TransferStatus(message=f"Error: {e}")
    END FUNCTION
END CLASS

FUNCTION serve():
    # Step 1: Create a gRPC server with 10 worker threads
    Create server = grpc.server(ThreadPoolExecutor(max_workers=10))

    # Step 2: Register the FileTransferService to the server
    Register FileTransferService to the server

    # Step 3: Bind the server to port 50051
    Bind server to "[::]:50051" (IPv4 and IPv6)

    # Step 4: Start the server
    Start server

    Print "Server is running on port 50051..."

    # Step 5: Keep the server running
    Wait for server termination
END FUNCTION

# Main entry point
IF __name__ == "__main__":
    Call serve()
```