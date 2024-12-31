from mpi4py import MPI
import os

comm = MPI.COMM_WORLD 
rank = comm.Get_rank()
size = comm.Get_size()

def master_process(filename):
    """ Master process: reads the file and distributes chunks. """
    try:
        with open(filename , "rb") as file:
            chunk_size = 1024
            chunks = []
            while (chunk := file.read(chunk_size)):
                chunks.append(chunk)
        
        num_chunks = len(chunks)
        print(f"Master read {num_chunks} chunks from {filename}")
        
        # Distribute chunks to workers
        for i, chunk in enumerate(chunks):
            dest_rank = i % (size - 1) + 1
            comm.send((i, chunk), dest=dest_rank, tag=11)
            print(f"Master send chunk {i} to process {dest_rank}")
            
        # Send termination signal to wokers
        for worker_rank in range(1, size):
            comm.send(None, dest=worker_rank, tag=11)
            
        # Collect status from workers
        success = True
        for _ in range(num_chunks):
            status = comm.recv(source=MPI.ANY_SOURCE, tag=22)
            print(f"Master: Received status {status}")
            if not status:
                success = False
        
        if success:
            print("Master: File trannsfer completed successfully")
        else:
            print("Master: File transfer failed")
    
    except FileNotFoundError:
        print("Master: File not found")
    except Exception as e:
        print(f"Master: Error - {e}")
        
def worker_process(output_dir="./uploaded_files"):
    """ Worker process: receives chunks and writes to file. """
    os.makedirs(output_dir, exist_ok=True)
    try:
        while True:
            data = comm.recv(source=0, tag=11)
            if data is None: # Termination signal
                print(f"Worker {rank}: Recieved termination signal.")
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
        master_process("test.txt")
    else:
        worker_process()
               