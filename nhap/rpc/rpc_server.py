import grpc 
from concurrent import futures
import file_transfer_pb2
import file_transder_pb2_grpc
import os

class FileTransferService(file_transfer_pb2_grpc.FileTransferServicer):
    def UploadFile(self, request_iterator, context):
        # request_iterator (filename, data)
        try:
            first_chunk = next(request_iterator)
            filepath = os.path.join("./uploaded_files", os.path.basename(first_chunk.filename))
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, "wb") as file:
                file.write(first_chunk.data)
                for chunk in request_iterator:
                    file.write(chunk.data)
            
            return file_transfer_pb2.TransferStatus(message="File upload successfully")
        except Exception as e:
            return file_transfer_pb2.TransferStatus(message=f"Error: {e}")
        
def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_wokers=10))
    file_transfer_pb2_grpc.add_FileTransferServivcer_to_server(FileTransferServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server is running on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    server()
    