import grpc
from concurrent import futures  # run the gRPC server with multiple threads.
import file_transfer_pb2
import file_transfer_pb2_grpc
import os  # manipulate the file system

class FileTransferService(file_transfer_pb2_grpc.FileTransferServicer):
    def UploadFile(self, request_iterator, context):
        # request_iterator (filename. data)
        # context: authentication, connection check, timeout handling will do in future 
        try:
            first_chunk = next(request_iterator) # Get the first chunk
            filepath = os.path.join("./uploaded_files", os.path.basename(first_chunk.filename))  # Create the file path and os.path.basename only the file name without needing to know the original file path on the client.
            os.makedirs(os.path.dirname(filepath), exist_ok=True)  # Create the directory

            with open(filepath, "wb") as file:
                file.write(first_chunk.data)
                for chunk in request_iterator:
                    file.write(chunk.data)

            return file_transfer_pb2.TransferStatus(message="File uploaded successfully")
        except Exception as e:
            return file_transfer_pb2.TransferStatus(message=f"Error: {e}")

def serve():    # Create and run the gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))    # Create a executor with 10 threads
    # FileTransferServicer: The server can handle RPC requests from the client by calling the methods in FileTransferService.
    file_transfer_pb2_grpc.add_FileTransferServicer_to_server(FileTransferService(), server)    # Register FileTransferServicer to the server
    server.add_insecure_port("[::]:50051")  # [::]: Ipv4, Ipv6
    server.start()
    print("Server is running on port 50051...")
    server.wait_for_termination()   # The server will continue to run until it receives a stop signal.

if __name__ == "__main__":
    serve()
