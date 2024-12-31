import grpc
import file_transfer_pb2
import file_transfer_pb2_grpc

def upload_file(filename):
    channel = grpc_insecure_channel("localhost:50051")
    stub = file_transfer_pb2_grpc.FileTransferStub(channel)
    
    def generate_chunks():
        try:
            with open(filename, "rb") as file:
                while (chunk := file.read(1024)):
                    yield file_transfer_pb2.FileChunk(filename = filename, data = chunk)
        except FileNotFoundError:
            print("Error file not found")
            return
    # Call the RPC method UploadFile on the server.
    response = stub.UploadFile(generate_chunks())
    print(response.message)
    
if __name__ == "__main__":
    upload_file("test.txt")