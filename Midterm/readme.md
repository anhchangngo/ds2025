
# HTTP-over-MPI Proxy

This project implements an **HTTP Proxy** using the **Message Passing Interface (MPI)**. It facilitates HTTP communication by forwarding requests from a client through an MPI network and returning responses. This setup is useful for distributed systems where MPI is the primary communication protocol.

---

## **Overview**
The system consists of:

1. **HTTP Client**: Sends HTTP requests to the proxy.
2. **HTTP-over-MPI Proxy**:
   - **Master (Rank 0)**: Listens for HTTP requests, forwards them to workers, and sends back responses to the client.
   - **Workers (Rank > 0)**: Process HTTP requests by forwarding them to the target HTTP server and returning the responses to the master.
3. **Target HTTP Server**: Processes requests and returns HTTP responses.

---

## **Components**

### **1. Master (Rank 0)**
- Listens for HTTP requests on a specified port (e.g., 8080).
- Sends the request details (method, headers, path) to a worker via MPI.
- Receives the response from the worker and sends it back to the HTTP client.

### **2. Worker (Rank > 0)**
- Receives HTTP request details from the master.
- Forwards the request to the target HTTP server (e.g., `http://localhost:5000`).
- Captures the server’s response and sends it back to the master.

### **3. Target HTTP Server**
- This is the actual HTTP server that processes the request (e.g., a Flask or Django server running locally or remotely).

---

## **Workflow**

1. **Client sends request**:
   - An HTTP client (e.g., cURL, Postman) sends a request to the proxy running on `http://localhost:8080`.

2. **Master forwards request**:
   - The master (Rank 0) receives the request and forwards it to a worker (Rank > 0) via MPI.

3. **Worker processes request**:
   - The worker receives the request, forwards it to the target HTTP server (e.g., `http://localhost:5000`), and receives the response.

4. **Worker sends response**:
   - The worker sends the response back to the master using MPI.

5. **Master responds to client**:
   - The master receives the response and sends it back to the HTTP client.

---

## **Code Structure**

### **1. Master (Rank 0)**
- Listens on port `8080`.
- Uses Python’s `http.server` to parse incoming HTTP requests.
- Sends request data to a worker using MPI.
- Receives the response from the worker and sends it back to the client.

### **2. Worker (Rank > 0)**
- Waits for requests from the master via MPI.
- Forwards the request to the target server using the `requests` library.
- Sends the response data back to the master using MPI.

---

## **Setup and Execution**

### **1. Prerequisites**
- Python 3
- Required libraries:
  ```bash
  pip install mpi4py requests
  ```
- MPI runtime environment (e.g., `mpich` or `openmpi`)

### **2. Target HTTP Server**
Run a local HTTP server at `http://localhost:5000`. Example using Flask:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to localhost:5000!"

@app.route('/test')
def test():
    return "This is a test route!"

if __name__ == "__main__":
    app.run(port=5000)
```

Save the file as `local_server.py` and run it:
```bash
python local_server.py
```

### **3. HTTP-over-MPI Proxy**
Save the provided code as `http_over_mpi_master_worker.py`.

Run the proxy using `mpiexec` with two processes (1 master and 1 worker):
```bash
mpiexec -n 2 python http_over_mpi_master_worker.py
```

### **4. Sending Requests**
Use `curl` to send requests to the proxy:

- Request the root path:
  ```bash
  curl http://localhost:8080/
  ```
- Request a test route:
  ```bash
  curl http://localhost:8080/test
  ```

---

## **Expected Output**

1. **Logs**:
   - Master log example:
     ```
     Master proxy is running on port 8080...
     127.0.0.1 - - [31/Dec/2024 18:32:13] "GET / HTTP/1.1" 200 -
     ```
   - Worker log example:
     ```
     Worker forwarding request to: http://localhost:5000/
     ```

2. **Client Response**:
   - For `/` route:
     ```
     Welcome to localhost:5000!
     ```
   - For `/test` route:
     ```
     This is a test route!
     ```

---

## **Scaling the System**
You can increase the number of workers to handle multiple requests concurrently:
```bash
mpiexec -n 4 python http_over_mpi_master_worker.py
```
- Rank 0: Master
- Rank 1, 2, 3: Workers

---

## **Error Handling**
- If a route does not exist on the target server, the proxy will return a `404 Not Found` error.
- If the worker fails to connect to the target server, it returns a `500 Internal Server Error`.

---

## **Future Improvements**
- Add support for other HTTP methods (e.g., POST, PUT, DELETE).
- Implement load balancing among multiple workers.
- Enhance error handling and logging.
- Optimize for high concurrency.
