
### File System
- System that permanently stores data
- Files ∈ directories
- Directories ∈ volume
- Directories ∈ Directories
- Addressable with "Path"

### Metadata 
- Includes details like the file's name, size, creation date, permissions, etc.
- Filedata and metadata stored separately
- File descriptors + metadata are stored in inodes
- Largetreeortables
- Filecontent lookups
- Replicable

### Journaling
Log changes to a "journal" before it is commited
- Change to file content: slow. twice
- Change to file metadata: fast. prone to corruption

### RAID 
Redundancy Array of Inexpensive/Independent Disks
- RAID0: Striped, Performance
- RAID1: Mirrored, Reliability
- RAID5: Striped + Parity,
- RAID6: Striped + Dual Parity
- RAID10: Striped + Mirrors

### Snapshot
- Copy of a set of files and directories
- A certain point in time

### Distributed File System
- Access to files on remote servers
- Consistency
- Locking
- Support for local caching and replication

### Network File System (NFS)
- Purpose: Simple and widely-used distributed file system for <b>sharing files over a network</b>.
- Key Features:
    - Stateless protocol.
    - Compatible across platforms.
    - Supports concurrent file sharing.
- Advantages: Easy setup and use.
- Disadvantages: Limited scalability and performance issues on large networks.

### Andrew File System (AFS)
- Purpose: Distributed file system for <b>large-scale networks</b> with a focus on <b>scalability</b> and <b>security</b>.
- Key Features:
    - Extensive local caching.
    - Kerberos-based authentication.
    - Replication for fault tolerance.
- Advantages: High performance, scalability, and strong security.
- Disadvantages: Complex setup and maintenance.

### GlusterFS
- Purpose: Scalable distributed file system for <b>modern</b>, <b>data-intensive environments</b>.
- Key Features:
    - No metadata server (avoids single points of failure).
    - Elastic scalability for large clusters.
    - Supports replication and striping.
    - Advantages: Highly scalable and fault-tolerant.
- Disadvantages: Steeper learning curve and higher latency in large clusters.

### GlusterFS trusted pool
A GlusterFS trusted pool is a group of servers (also called nodes or peers) that are interconnected and authorized to collaborate in a GlusterFS distributed file system. These servers trust each other for file storage and management operations.
- Peer Relationship
- Shared State
- Authorization
- Volume Management

[?] 
A pool refers to a group or collection of resources that are managed and utilized collectively to achieve share goals or provide servives.
