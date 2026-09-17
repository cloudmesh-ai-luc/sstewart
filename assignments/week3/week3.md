# Week 3.4 — VM Comparison

## Objective

The objective of this assignment was to compare the experience of starting and using a virtual machine locally with using cloud-based VM infrastructure, specifically with Jetstream and Chameleon Cloud.

## 1. Local Virtual Machine vs. Cloud VMs

| Category | Local Virtual Machine (UTM)| Jetstream | Chameleon Cloud |
| :--- | :--- | :--- | :--- |
| **Setup** | Relatively simple once virtualization software and an OS image are available. All resources needed for the VM need to be installed and configured on the virtual machine. | Requires portal configuration, VM configuration, SSH keys, networking, and a floating IP. | Requires portal configuration, SSH keys, resource selection, a reservation, networking, and VM launch. |
| **Resources** | Limited by the local computer hardware and operating system. | Uses remotely allocated cloud resources. | Uses remote computing resources reserved for the instance. |
| **Access** | Accessed directly from the host computer via UTM app. | Requires remote SSH access. | Requires remote SSH access. |
| **Networking** | Usually simple to set up on the VM. | Required a floating IP and security-group configuration. | Required a floating IP to provide external SSH access. |
| **Resource management** | Uses resources belonging to the local computer such as RAM, storage, and CPU. | VM resources must be deleted when no longer needed. | VM, floating IP, and lease must be released after use. |
| **Availability** | Available whenever the local computer is available. | Depends on available cloud resources and software stability (sometimes there are outages that affect ability to access VMs). | Depends on available resources and reservations. |
| **Flexibility** | Easy to start, stop, and recreate locally. | Provides access to remote cloud infrastructure. | Provides access to remote computing hardware through reservations.

## 2. Experience Using UTM (Local Virtual Machine)

Starting a VM locally was relatively straightforward because the resources were directly available on the computer. There was no need to wait for a cloud reservation or configure a floating IP for basic access.

The main limitation was the hardware available on the local computer. UTM shares the host's CPU, memory, storage, and network resources. Giving the UTM VM more resources affects the performance of the host system.

The local VM environment was convenient for testing software and experimenting with configurations without depending on cloud availability.

## 3. Experience Using Jetstream

For Jetstream, the basic VM creation process was straightforward, but it can be difficult to get SSH access to the VM, depending on the software's status at the time.

One Ubuntu instance was successfully created and received a floating IP address, but SSH connection timed out. Upon waiting for a day or so, the connection finally worked. The instance was previously unavailable due to an mismatch in the security group configuration not having the `remotelogin` group. 

A dedicated SSH key pair was eventually created through the Jetstream/OpenStack portal and used with the `remotelogin` security group. The VM was also deleted and re-created in order to avoid any other issues. The final VM successfully accepted an SSH connection.

The successful Jetstream VM used the `m3.tiny` flavor with 1 vCPU and 3 GB of RAM. Compared with UTM, Jetstream provided a useful introduction to managing remote infrastructure, floating IP addresses, security groups, and SSH authentication.

The Jetstream experience demonstrated that successfully creating a VM does not necessarily mean that remote access will work immediately. Networking, security groups, and SSH keys also have to be configured correctly.

## 4. Experience Using Chameleon Cloud

The Chameleon Cloud experience required more planning and exploration than both UTM and the basic Jetstream deployment.

The Chameleon portal was explored first, noting the several different configurations that needed to be selected before the VM could be launched. The preferred time zone was configured, an SSH key was prepared, a reservation was created, and a flavor was selected. The Ubuntu 24.04 image was used as the basis for the VM.

The interface showed baremetal as the only available flavor for the selected Ubuntu 24.04 image, so baremetal was selected as the available option.

A one-hour host lease was created before the VM was launched. The lease initially entered a `PENDING` state and later became `ACTIVE`. After the VM was launched, a floating IP had to be associated with the instance before SSH access could be established.

Once networking was configured, SSH access worked successfully from the host computer (MacOS). The Chameleon VM provided substantially more CPU and memory than the small Jetstream VM, demonstrating the advantage of having access to larger remote computing resources.

## 5. Advantages and Disadvantages

### Local Virtual Machine

**Advantages:**
- Simple and convenient for experimentation.
- Direct access from the host computer.
- No cloud reservation is required.
- Easy to start, stop, and recreate.

**Disadvantages:**
- Limited by the host computer's hardware.
- VMs can consume significant RAM and storage.
- Performance depends on the local machine.
- External networking can require additional configuration.

### Jetstream

**Advantages:**
- Provides access to remote cloud computing resources.
- Relatively simple VM creation process.
- Supports floating IPs and security groups.
- Provides practical experience with remote SSH access.

**Disadvantages:**
- Requires internet connectivity.
- SSH and networking configuration can require troubleshooting.
- Cloud resources must be cleaned up after use.
- VM availability depends on cloud resources.
- Can be difficult to enable SSH access due to potential outages. 

### Chameleon Cloud

**Advantages:**
- Provides access to powerful remote computing resources.
- Supports different cloud sites, images, and hardware configurations.
- Provides practical experience with cloud infrastructure.
- Supports remote access through SSH.
- Demonstrates resource reservations, networking, and resource cleanup.

**Disadvantages:**
- Requires more preparation before launching a VM.
- Depends on network connectivity.
- Requires SSH key and network configuration.
- Resources may initially be pending or unavailable.
- Reservations and allocated resources must be managed carefully.

## 6. Overall Experience

The local VM was the easiest to use because the computing resources were immediately available and no external reservation was required. The only requirement was to download the application from the internet and the process was straightforward in order to create, start, and stop the VM.

Jetstream introduced the additional complexity of cloud networking, floating IP addresses, security groups, and remote SSH access. The initial SSH timeouts also demonstrated the need for potential troubleshooting when working with cloud infrastructure.

Chameleon required the most planning because a lease, SSH keys, and floating IPs had to be created and activated before the VM could be launched. However, it provided access to substantially more computing resources and demonstrated a more structured resource-allocation process.

