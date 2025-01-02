## MPI
MPI (Message Passing Interface) operates on a peer-to-peer model, where processes operate independently and communicate with each other through a message passing mechanism.

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

#### Distributed chunk tơ worker
```
dest_rank = i % (size - 1) + 1
```
- `size - 1`: The number of workers (excluding the master process with rank=0). 
- `i % (size - 1)`: Calculates which worker will receive this chunk (distributed in a round-robin manner). 
- `+ 1`: Skips rank=0 (master), as workers start from rank=1.

If there are 3 workers (rank=1, rank=2, rank=3) and 6 chunks: 
- Chunk 0 → Worker 1 (rank 1). 
- Chunk 1 → Worker 2 (rank 2). 
- Chunk 2 → Worker 3 (rank 3). 
- Chunk 3 → Worker 1 (rank 1), repeating.

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


### Pesudocode

#### Initialization
```py
Initialize MPI communication with comm = MPI.COMM_WORLD
Get process rank using rank = comm.Get_rank()
Get total number of processes using size = comm.Get_size()
```

#### Master Process

```py
FUNCTION master_process(filename):
    TRY:
        Open the file in binary read mode as file
        Initialize chunk_size = 1024 bytes
        Initialize chunks = []

        # Step 1: Read file in chunks
        WHILE chunk = file.read(chunk_size):
            Add chunk to chunks

        num_chunks = length of chunks
        Print "Chunk size: {len(chunk)} bytes"
        Print "Master: Read {num_chunks} chunks from {filename}"

        # Step 2: Distribute chunks to workers
        FOR each (index i, chunk) in chunks:
            dest_rank = (i % (size - 1)) + 1  # Assign chunks to workers in a round-robin manner
            Send (i, chunk) to dest_rank with tag=11
            Print "Master: Sent chunk {i} to process {dest_rank}"

        # Step 3: Send termination signal to workers
        FOR each worker_rank in range(1, size):
            Send None to worker_rank with tag=11

        # Step 4: Collect status from workers
        success = True
        FOR each chunk in chunks:
            Receive status from any worker with tag=22
            Print "Master: Received status {status}"
            IF status is False:
                success = False

        # Step 5: Report results
        IF success:
            Print "Master: File transfer completed successfully"
        ELSE:
            Print "Master: File transfer encountered errors"

    EXCEPT FileNotFoundError:
        Print "Master: Error - File {filename} not found"
    EXCEPT Exception as e:
        Print "Master: Error - {e}"
```

#### Worker Process

```py
FUNCTION worker_process(output_dir="./uploaded_files"):
    Create directory output_dir if it does not exist

    TRY:
        WHILE True:
            # Step 1: Receive data from master
            Receive data from master (rank 0) with tag=11
            IF data is None:
                Print "Worker {rank}: Received termination signal"
                BREAK

            # Step 2: Write chunk to file
            Extract chunk_index and chunk_data from data
            output_file = Join output_dir with "chunk_{chunk_index}.bin"
            Open output_file in binary write mode as file
            Write chunk_data to file
            Print "Worker {rank}: Wrote chunk {chunk_index} to {output_file}"

            # Step 3: Send success status back to master
            Send True to master (rank 0) with tag=22

    EXCEPT Exception as e:
        # Send failure status back to master
        Send False to master (rank 0) with tag=22
        Print "Worker {rank}: Error - {e}"
```

#### Main Program 

```py
IF rank == 0:
    # Master process handles reading and distributing file chunks
    Call master_process("test.txt")
ELSE:
    # Worker processes handle receiving and saving file chunks
    Call worker_process(output_dir="./uploaded_files")
```