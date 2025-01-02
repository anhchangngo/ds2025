
### 1. In parallel computing, what does the term Amdahl’s Law describe?

Select one:

- A. The theoretical maximum speedup achievable by parallelizing a task.
- B. The method of fault tolerance in distributed systems.
- C. The approach of sharing tasks dynamically across processors.
- D. The technique of dividing memory evenly among processors.

-> A: Amdahl’s Law is used to predict the maximum possible improvement in performance of a system when only part of the task can be parallelized. It shows that the speedup gained by parallelizing a portion of the task is limited by the non-parallelizable part.

### 2. What is the primary characteristic of UMA?

Select one:
- A. Memory access times vary depending on the processor.
- B. Each processor has equal access time to all memory locations.
- C. Each processor has its own dedicated memory module.
- D. Processors do not share memory.

-> B: In a Uniform Memory Access (UMA) architecture, all processors have equal access time to all memory locations, meaning that the memory is shared and the access time does not depend on which processor is accessing it.

### 3. What is the primary purpose of an RPC mechanism?

Select one:
- A. To enable a program to execute code on a remote system as if it were local.
- B. To encrypt com·mu·ni·cation between servers.
- C. To provide real-time synchronization between two processes.
- D. To transfer files between two systems.

-> A: RPC (Remote Procedure Call) allows a program to call a procedure (function) on a remote system, as if it were executing locally, abstracting the complexity of network communication. This makes it easier to design distributed systems.

### 4. Which scenario best demonstrates the use of SIMD architecture?

Select one:
- A. A convolution operation in image processing, where the same filter is applied to different parts of an image.
- B. A distributed system running separate instances of a program on distinct datasets.
- C. A multi-threaded web server handling requests from multiple users.
- D. A task where a single CPU executes different instructions on the same data point.

-> A: SIMD (Single Instruction, Multiple Data) architecture allows the same operation to be performed simultaneously on multiple pieces of data. In the case of image processing, the same filter (or operation) can be applied to different parts of the image concurrently, which is a perfect use case for SIMD.

### 5. What does the acronym NUMA stand for?

Select one:
- A. Non-Uniform Memory Access
- B. Non-Unified Memory Access
- C. Non-Unified Memory Architecture
- D. Non-Uniform Memory Architecture

-> A: NUMA refers to a memory architecture where memory access times depend on the memory location relative to the processor. In NUMA systems, each processor has its own local memory, and access to remote memory (from another processor) is slower than accessing local memory.

### 6. Which layer of the OSI model is responsible for error detection and correction?

Select one:
- A. Physical Layer
- B. Data Link Layer
- C. Network Layer
- D. Application Layer

-> B: The Data Link Layer (Layer 2) of the OSI model is responsible for error detection and correction. It ensures that data is correctly transmitted between two devices on the same network by detecting and sometimes correcting errors that may occur during transmission.

### 7. What type of tasks are most suitable for MPI?

Select one:
- A. Tasks focused on optimizing single-threaded algorithms.
- B. Tasks requiring synchronous com·mu·ni·cation between devices.
- C. Tasks involving distributed parallel computation with message-based com·mu·ni·cation.
- D. Tasks needing shared memory access for high-speed performance.

-> C: MPI (Message Passing Interface) is designed for parallel computing tasks where processes need to communicate with each other in a distributed system. It is ideal for scenarios where tasks are running on different nodes, and message-based communication is used to exchange data between those nodes.

### 8. In which scenario is RPC most suitable for executing databases' stored procedures?

Select one:
- A. When an analytics engine reads logs stored in a distributed file system without modifying the data.
- B. When multiple nodes of a distributed system independently perform calculations on local datasets.
- C. When a remote database server is used to compute aggregate values based on input provided by a client application.
- D. When a local script directly queries a database and processes the results in memory.

-> C: RPC (Remote Procedure Call) is suitable in this scenario because it allows a client application to invoke a stored procedure on a remote database server, enabling the computation of aggregate values or other database operations without having to transfer large amounts of data back and forth. This is efficient and abstracts the complexity of distributed communication.

### 9. Which of the following examples highlights the use of RPC with stored procedures in Advanced Databases?

Select one:
- A. A client application invokes a remote stored procedure to verify user credentials and retrieve associated profile data from the database.
- B. A database management system performs an automatic backup to an attached storage device.
- C. A distributed queue system processes tasks asynchronously across multiple worker nodes.
- D. A microservice runs an in-memory cache lookup to reduce query latency.

-> A

### 10. Which of the following does NOT belong to the abstraction of distribution in Distributed Systems?

Select one:
- A. Computation
- B. Network
- C. Com·mu·ni·ca·tion
- D. Storage

-> B

### 11. What does SIMD stand for in computer architecture?

Select one:
- A. Single Instruction, Multiple Data.
- B. Simultaneous Input, Multiple Data.

-> A

### 12. Which architecture is most suitable for parallel computing involving shared memory?

Select one:
- A. Distributed memory systems such as MPI clusters.
- B. Systems using GPUs for large-scale matrix operations.
- C. Peer-to-peer systems where nodes communicate directly.
- D. Symmetric Multiprocessing (SMP), where multiple processors access the same memory.

-> D: In Symmetric Multiprocessing (SMP) systems, multiple processors share the same memory, which makes it ideal for parallel computing where processors need to access and modify shared data quickly. This architecture supports shared memory, where all processors can read from and write to the same memory space, facilitating efficient parallel processing.

### 13. Which of the following scenarios best demonstrates the use of RPC in the context of stored procedures (Advanced Databases)?

Select one:
- A. A distributed system transmitting files between nodes using a custom protocol.
- B. A local script iterating over a dataset stored in an in-memory database.
- C. A NoSQL database performing local aggregation queries without external interaction.
- D. A web application triggering a stored procedure on a remote database server to calculate the total sales for a given month.

-> D: This scenario demonstrates the use of RPC (Remote Procedure Call) because the web application is invoking a stored procedure on a remote database. The stored procedure on the database server performs the calculation (in this case, the total sales for a given month), and the result is returned to the web application. RPC abstracts the communication between the application and the remote procedure, making it appear as though the procedure is being executed locally.

### 14. Which of the following is a key feature of MPI?

Select one:
- A. Automatic load balancing in distributed systems.
- B. Shared memory for inter-process com·mu·ni·cation.
- C. Support for only single-threaded programs.
- D. Standardized com·mu·ni·cation protocols for parallel computing.

-> D

### 15. Which of the following scenarios best utilizes MPI?

Select one:
- A. A single-threaded process generating reports from a local database.
- B. A real-time messaging app that delivers chat messages to multiple users.
- C. An online multiplayer game server synchronizing player actions across multiple clients.
- D. A weather simulation where large-scale data is divided among processors to compute results collaboratively.

### 16.

### 17.

### 18.

### 19.

### 20.


