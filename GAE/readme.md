# Cloud Computing

Cloud computing is a model for enabling popular, convenient, on-demand network access to a shared pool of configurable computing resources (e.g., networks, servers, storage, applications, and services) that can be rapidly provisioned and released with minimal management effort or service provider interaction.

Externalize computing infrastructure
- Customer: Business
- Provider: Infrastructure management

Connect the customer needs with the provider's services

## Model

### IaaS
- Virtual machines
    - Primitive form of resources: <b>computing, memory, network, storage</b>
    - Load balancer
- Customer take care of
    - OS
    - Application
- EC2, GCE, Azure

### PaaS
- Virtualized execution platform
<b>
    - API
    - Libraries
    - Services
    - Tools
</b>
- Customer creates apps on top of platform
- GAE, Elastic Beanstalk

### SaaS
- Provides software
    - Accessible with thin client interface
    - Web browser
- Customer uses the app
- Google Apps, MS Office 365

## Benefit: Dedication
- Customer 
    - Unlimitted resources
    - Scalability
    - Pay as you go
- Provider
    - Resource sharing
    - Only pay for initial investment

# Virtualization
- Software and/or hardware-based solution
- Building and running many operating systems simultaneously
- Separate physical hardware and the executing operating systems
- eg: VMware Workstation, VirtualBox, ...

## Hypervisor
- Virtual Machine Monitor
- Responsible for hardware emulation and communication
    - CPU
    - Memory
    - Storage
    - Network
    - ...
- Share its hardware resources to Guest OS

