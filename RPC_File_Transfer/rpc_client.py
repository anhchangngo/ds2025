import grpc
import file_transfer_pb2
import file_transfer_pb2_grpc

def upload_file(filename):
    channel = grpc.insecure_channel("localhost:50051")      # Create a connection channel
    stub = file_transfer_pb2_grpc.FileTransferStub(channel) # Allows the client to call the RPC methods of the server (here is UploadFile).

    def generate_chunks():
        try:
            with open(filename, "rb") as file:
                while (chunk := file.read(1024)):  # An empty string (b'') if the end of the file (EOF) has been reached.
                    # yield helps the function operate like a generator, producing data in chunks as needed
                    yield file_transfer_pb2.FileChunk(filename=filename, data=chunk)
        except FileNotFoundError:
            print(f"[-] Error: File '{filename}' not found.")
            return
    # Call the RPC method UploadFile on the server.
    response = stub.UploadFile(generate_chunks())
    print(response.message)

if __name__ == "__main__":
    upload_file("test.txt")
