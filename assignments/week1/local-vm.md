**UTM Installation Guide for Macbook Users**

Before we begin the tutorial, let's answer a key question: What is UTM?

The typical structure of a MacBook could look like the following:

```
YOUR MAC
│
├── macOS  ← Your normal operating system
│
└── UTM
     │
     └── Virtual Machine
          │
          ├── CPU
          ├── RAM
          ├── Storage
          ├── Network
          └── Operating System
               ├── Ubuntu
               ├── Windows
               ├── Kali Linux
               └── etc.
```

The virtual machine behaves like another computer - a key aspect of UTM. For example, you could have:

```
MacBook
   ↓
 macOS
   ↓
  UTM
   ↓
Ubuntu Linux
```

This allows you to open Ubuntu in a window while continuing to use applications on your macbook.
With that being said, let's start the tutorial!


**Steps**
1. Find out what kind of Macbook you have. You can do this by going to  → About This Mac
Look for either:

*Apple Silicon*

Some examples are:
```
Chip: Apple M1
Chip: Apple M2
Chip: Apple M3
Chip: Apple M4
Chip: Apple M5
```
or

*Intel*

You'll see:

> Processor: 2.6 GHz 6-Core Intel Core i7

**Why this matters**

Apple Silicon Macs use the ARM64 architecture.

Intel Macs use x86/x64.

Whenever possible, you want the guest operating system to use the same architecture as your Mac.

For example:

M-series Mac → Ubuntu ARM64

is much better than:

M-series Mac → Ubuntu x86

because the latter requires emulation and can be significantly slower.

The UTM documentation specifically recommends ARM64 images for Apple Silicon and x64 images for Intel Macs.

3. Install UTM

There are 2 primary ways to install UTM. The first way is through the Apple Store (cost $$$) or download directly
from their website (free). The only difference between the paid and free version is that the paid version allows
for automatic updates versus having to update manually.

*Link to Apple Store: https://apps.apple.com/us/app/utm-virtual-machines/id1538878817?mt=12*

*Link to direct download: https://mac.getutm.app/*

4. Once installed, open UTM on your macbook. At first, you will have no virtual machines, and your screen should look something like this:

```
┌──────────────────────────────────┐
│ UTM                         +    │
├──────────────────────────────────┤
│                                  │
│       No Virtual Machines        │
│                                  │
│                                  │
└──────────────────────────────────┘
```

To create a virtual machine, press the + button on the top right hand corner.

5. Create your first VM
Once you click the + button, you will be prompted to either virtualize or emulate your VM.
Virtualization allows your mac to efficiently run the guest operating system using compatible CPU architecture.

As an example:

**Virtualize**

```
M-series Mac
     ↓
    UTM
     ↓
Ubuntu ARM64
```

This is fast.

**Emulate**

Emulation allows you to pretend your computer has completely different hardware.

For example:

```
M-series Mac
     ↓
    UTM
     ↓
Intel x86 Windows
```

This is much more computationally expensive.

*Rule of thumb:*

*If you can virtualize it, virtualize it.*

6. Installing your VM - Example Walkthrough

Let's do an example walkthrough of installing Ubuntu as your preferred VM. Since I am on a Apple Silicon Mac,
I'd select:

Ubuntu ARM64

Not:

Ubuntu x86_64 <-- Use this if you have an Intel Mac 

Go to Ubuntu's official website and download an appropriate ARM64 desktop image if you have an Apple Silicon Mac.

If you have an Intel Mac, download the AMD64/x86_64 version.

You will end up with something like:

ubuntu-24.04-desktop-arm64.iso

or:

ubuntu-24.04-desktop-amd64.iso

The exact filename will vary by Ubuntu release.

8. Create the VM

Back in UTM:

```
+ → Virtualize → Linux
```

You will then be asked for the installation media.

Select:

Browse and choose your Ubuntu ISO.

9. Configure your virtual machine

This is where things can get confusing, so let's keep it simple.

You'll see settings for things such as:

RAM

CPU cores

Storage

Network

Display



RAM

If your Mac has:

8 GB RAM

Give Ubuntu roughly:

4 GB

16 GB RAM

Give Ubuntu:

6–8 GB

32 GB RAM

Give Ubuntu:

8–12 GB

Don't give the VM all your RAM.

For example:

16 GB Mac

macOS
████████████ 8 GB

Ubuntu
████████ 6 GB

Available
██ 2 GB

You want macOS to remain responsive.

10. CPU

You may see something like:

CPU Cores: 4

For a normal Linux development VM, 4 cores is a perfectly reasonable starting point.

If your Mac has plenty of CPU resources, you can increase it later.

Don't immediately allocate everything.

For example:

Mac: 10 CPU cores

Mac gets: 6
VM gets: 4

11. Storage

This is the virtual hard drive.

You might see:

Storage: 64 GB

That's generally plenty for a basic Ubuntu development VM.

Remember:

This doesn't necessarily mean Ubuntu immediately consumes 64 GB of physical storage.

Depending on the disk configuration, the virtual disk can grow as you use it.

For a development environment, start around:

64–80 GB

If you plan to install lots of software, Docker images, databases, etc., consider:

100–150 GB

12. Network

You generally want networking enabled.

UTM supports shared and bridged networking.

For your first VM, you can usually leave the default networking configuration alone.

Ubuntu should be able to access the internet.

13. Save the VM

Give it a useful name:

Ubuntu Development

Click:

Save

14. Start Ubuntu

Your VM should now appear in UTM.

Something like:

UTM

┌──────────────────────────┐
│ Ubuntu Development       │
│                          │
│ ARM64                    │
│ 8 GB RAM                 │
│ 4 CPU                    │
└──────────────────────────┘

Select it.

Click:

▶ Run

You'll see the virtual computer boot.

Eventually Ubuntu's installer should appear.

15. Install Ubuntu

The Ubuntu installation process is basically the same conceptually as installing Ubuntu on a physical computer.

You'll choose:

Language

Keyboard layout

Network

User account

Password

Time zone

Disk configuration

When Ubuntu asks about the disk, don't worry about destroying your Mac's actual disk.

You're installing Ubuntu onto the virtual disk you created in UTM.

Think of it as:

Mac's actual SSD
│
├── macOS
│
└── Ubuntu VM disk
      │
      └── Ubuntu

Ubuntu isn't replacing macOS.

16. Finish the installation

Once Ubuntu finishes installing, you'll probably be asked to restart.

Let it restart.

If UTM asks you to remove the installation media, you may need to eject the ISO from the VM's virtual CD/DVD drive.

Then start Ubuntu again.

You should eventually reach:

Ubuntu Desktop

🎉 You now have a Linux computer running inside your Mac.



**Official Resources**

UTM official website: https://mac.getutm.app/

UTM installation documentation: https://docs.getutm.app/installation/macos/

UTM documentation: https://docs.getutm.app/

UTM VM basics: UTM VM basics

UTM gallery of prebuilt VMs: https://mac.getutm.app/gallery/





