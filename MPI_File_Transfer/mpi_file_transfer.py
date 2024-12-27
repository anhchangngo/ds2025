from mpi4py import MPI
import os

comm = MPI.COMM_WORLD   # The default communicator includes all processes participating in the program.
rank = comm.Get_rank()  # Current process rank
size = comm.Get_size()  # Total number of processes

def master_process(filename):
    """Master process: reads the file and distributes chunks."""
    try:
        with open(filename, "rb") as file:
            chunk_size = 1024  # 1 KB per chunk
            chunks = []
            while (chunk := file.read(chunk_size)): # Read data from the file in chunks (1 KB at a time) until all data is read.
                chunks.append(chunk)
        
        num_chunks = len(chunks)
        print(f"Master: Read {num_chunks} chunks from '{filename}'.")

        # Distribute chunks to workers
        for i, chunk in enumerate(chunks):
            dest_rank = i % (size - 1) + 1  # Distribute among workers
            comm.send((i, chunk), dest=dest_rank, tag=11)  # tag 11 : mark the message as chunk data.
            print(f"Master: Sent chunk {i} to process {dest_rank}.")

        # Send termination signal to workers
        for worker_rank in range(1, size):
            comm.send(None, dest=worker_rank, tag=11)

        # Collect status from workers
        success = True
        for _ in range(num_chunks):
            status = comm.recv(source=MPI.ANY_SOURCE, tag=22) # tag 22 : mark the message as status(success/failure).
            print(f"Master: Received status {status}.")
            if not status:
                success = False

        if success:
            print("Master: File transfer completed successfully.")
        else:
            print("Master: File transfer encountered errors.")

    except FileNotFoundError:
        print(f"Master: Error - File '{filename}' not found.")
    except Exception as e:
        print(f"Master: Error - {e}")

def worker_process(output_dir="./uploaded_files"):
    """Worker process: receives chunks and writes to file."""
    os.makedirs(output_dir, exist_ok=True)
    try:
        while True:
            data = comm.recv(source=0, tag=11)
            if data is None:  # Termination signal
                print(f"Worker {rank}: Received termination signal.")
                break

            chunk_index, chunk_data = data
            output_file = os.path.join(output_dir, f"chunk_{chunk_index}.bin")
            with open(output_file, "wb") as file:
                file.write(chunk_data)
                print(f"Worker {rank}: Wrote chunk {chunk_index} to '{output_file}'.")

            # Send status back to master
            comm.send(True, dest=0, tag=22)
    except Exception as e:
        comm.send(False, dest=0, tag=22)
        print(f"Worker {rank}: Error - {e}")

if __name__ == "__main__":
    if rank == 0:
        # Master process
        master_process("test.txt")
    else:
        # Worker processes
        worker_process()
