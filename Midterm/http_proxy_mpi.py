from http.server import BaseHTTPRequestHandler, HTTPServer
from mpi4py import MPI
import requests

comm = MPI.COMM_WORLD
rank = comm.Get_rank()


# -------------------------------
# Master Process (Rank 0)
# -------------------------------
class ProxyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if rank == 0:
            # Read the POST request body
            content_length = int(self.headers['Content-Length'])  # Get body size
            post_data = self.rfile.read(content_length)  # Read the file content

            # Pack the HTTP POST request with file content
            request_data = {
                "method": "POST",
                "path": self.path,
                "headers": dict(self.headers),
                "body": post_data,  # Include the file data
            }

            # Send the request to a worker (Rank > 0)
            comm.send(request_data, dest=1, tag=0)

            # Receive the response from the worker
            response_data = comm.recv(source=1, tag=1)

            # Send the response back to the client
            self.send_response(response_data["status"])
            for key, value in response_data["headers"].items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response_data["body"])

    def do_GET(self):
        if rank == 0:
            # Pack the HTTP GET request
            request_data = {
                "method": "GET",
                "path": self.path,
                "headers": dict(self.headers),
            }
            # Send the request to a worker (Rank > 0)
            comm.send(request_data, dest=1, tag=0)

            # Receive the response from the worker
            response_data = comm.recv(source=1, tag=1)

            # Send the response back to the client
            self.send_response(response_data["status"])
            for key, value in response_data["headers"].items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response_data["body"])


def run_master():
    server_address = ('', 8080)  # Listen on port 8080
    httpd = HTTPServer(server_address, ProxyHandler)
    print("Master proxy is running on port 8080...")
    httpd.serve_forever()


# -------------------------------
# Worker Process (Rank > 0)
# -------------------------------
def run_worker():
    while True:
        # Receive the HTTP request from the master
        request_data = comm.recv(source=0, tag=0)

        # Forward the request to the target server
        target_url = "http://localhost:5000" + request_data["path"]
        print(f"Worker forwarding {request_data['method']} request to: {target_url}")

        try:
            if request_data["method"] == "POST":
                # Forward POST request with file content
                response = requests.post(
                    target_url,
                    headers=request_data["headers"],
                    data=request_data["body"],  # Send file data
                )
            elif request_data["method"] == "GET":
                # Handle GET request
                response = requests.get(target_url, headers=request_data["headers"])
            else:
                raise ValueError(f"Unsupported method: {request_data['method']}")

            # Pack the HTTP response
            response_data = {
                "status": response.status_code,
                "headers": dict(response.headers),
                "body": response.content,
            }
        except Exception as e:
            print(f"Error forwarding request: {e}")
            response_data = {
                "status": 500,
                "headers": {"Content-Type": "text/plain"},
                "body": b"Internal Server Error",
            }

        # Send the response back to the master
        comm.send(response_data, dest=0, tag=1)


# -------------------------------
# Run Program
# -------------------------------
if rank == 0:
    run_master()
else:
    run_worker()
