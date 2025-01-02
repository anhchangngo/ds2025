from mpi4py import MPI

# Initialize the MPI environment
comm = MPI.COMM_WORLD

# Get the number of processes
world_size = comm.Get_size()

# Get the rank of the process
world_rank = comm.Get_rank()

# Get the name of the processor
processor_name = MPI.Get_processor_name()

# Print off a hello world message
print(f"Hello world from processor {processor_name}, rank {world_rank} out of {world_size} processors")

# Finalize the MPI environment (handled automatically in mpi4py but good practice to include)
MPI.Finalize()


# mpirun -n 4 python3 hello_mpi.py
