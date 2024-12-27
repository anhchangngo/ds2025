## MPI
MPI operates on a peer-to-peer model, where processes operate independently and communicate with each other through a message passing mechanism.

| **Feature**          | **Client-Server**                                    | **MPI**                                                |
|-----------------------|-----------------------------------------------------|-------------------------------------------------------|
| **Architecture**      | A centralized server where clients connect to it.  | Multiple peer-to-peer processes, no central server.   |
| **Communication**     | Clients send requests; server processes and responds. | Processes exchange data directly with each other.     |
| **Roles**             | Server plays the main role; clients act as secondary. | All processes can communicate and perform computations. |
| **Use Cases**         | Suitable for centralized systems (e.g., gRPC, HTTP). | Suitable for parallel computing and distributed systems. |


```
dat@LAPTOP-4BOGORQ8:/mnt/c/Users/LOQ/Desktop/ds2025/MPI_File_Transfer$ mpirun -n 4 python3 mpi_file_transfer.py
Master: Read 1 chunks from 'test.txt'.
Master: Sent chunk 0 to process 1.
Worker 3: Received termination signal.
Worker 2: Received termination signal.
Worker 1: Wrote chunk 0 to './uploaded_files/chunk_0.bin'.
Master: Received status True.
Master: File transfer completed successfully.
Worker 1: Received termination signal.
```

Master Process (Rank 0):  
- Reads the file, divides it into small data parts (chunks), distributes the chunks to the worker processes. 
- Receives feedback from the worker to confirm whether the processing was successful or failed.

Worker Processes (Ranks 1, 2, ...): 
- Receives chunks from the master, writes them into their own files, and sends the status back to the master.

#### Master Process
The master_process() function handles the main tasks: 
- Reading the file and splitting it into chunks. 
- Distributing the chunks to workers. 
- Receiving feedback from the workers.

#### Worker Process
The worker_process() function handles: 
- Receiving chunks from the master. 
- Writing chunk data to a file. 
- Sending status feedback to the master.