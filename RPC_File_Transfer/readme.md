## RPC
RPC (Remote Procedure Call) is a network technical model, a communication protocol between software (or processes) that allows a program to request a service from another program located on a different computer/server, or simply put, it is a method of calling a function from a remote computer to retrieve a result.

RPC use model client-sever. 

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