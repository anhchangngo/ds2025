from http.server import BaseHTTPRequestHandler, HTTPServer
from mpi4py import MPI
import requests

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# -------------------------------
# Xử lý tại Master (Rank 0)
# -------------------------------
class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if rank == 0:
            # Gói yêu cầu HTTP
            request_data = {
                "method": "GET",
                "path": self.path,
                "headers": dict(self.headers)
            }
            # Gửi yêu cầu tới Worker (rank 1)
            comm.send(request_data, dest=1, tag=0)
            
            # Nhận phản hồi từ Worker
            response_data = comm.recv(source=1, tag=1)
            
            # Gửi phản hồi về client
            self.send_response(response_data['status'])
            for key, value in response_data['headers'].items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response_data['body'])

def run_master():
    server_address = ('', 8080)  # Lắng nghe cổng 8080
    httpd = HTTPServer(server_address, ProxyHandler)
    print("Master proxy đang chạy trên cổng 8080...")
    httpd.serve_forever()

# -------------------------------
# Xử lý tại Worker (Rank > 0)
# -------------------------------
def run_worker():
    while True:
        # Nhận yêu cầu từ Master
        request_data = comm.recv(source=0, tag=0)
        
        # Chuyển tiếp yêu cầu tới server mục tiêu
        target_url = "http://localhost:5000" + request_data["path"]
        print(f"Worker forwarding request to: {target_url}")
        
        try:
            response = requests.get(target_url, headers=request_data["headers"])
            # Gói phản hồi
            response_data = {
                "status": response.status_code,
                "headers": dict(response.headers),
                "body": response.content
            }
        except Exception as e:
            print(f"Error forwarding request: {e}")
            response_data = {
                "status": 500,
                "headers": {"Content-Type": "text/plain"},
                "body": b"Internal Server Error"
            }

        # Gửi phản hồi lại cho Master
        comm.send(response_data, dest=0, tag=1)

# -------------------------------
# Chạy chương trình
# -------------------------------
if rank == 0:
    run_master()
else:
    run_worker()
