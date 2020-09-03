# Layer 2 - Datalink

## Purpose of this layer

This layer gets frames to the correct network node. It users MAC addresses to determine where to forward traffic.

## Common protocols used

Address Resolution Protocol (ARP): for resolving MAC addresses on a subnet. Some uses:

- To send a packet over a local network, device A needs an ethernet address. ARP is a way for that device to ask every device on the network what MAC has an IP address, and that device will respond with the MAC and IP.
- To determine if a device can use a given IP address, it will send an ARP probe to determine if the address is already in use.
- ARP announcement/gratuitous ARP: Lets other devices know about any changes to MAC/IP for a device.

## Common attacks at this layer
### CAM overflow
#### The attack
Switches have a table that associates MAC addresses with the port to forward the frame to (called context-addressable memory, or CAM table). Obviously this table has a limited size, so an attacker can abuse this by filling it full of bogus entries. Once the table is full, the switch becomes a hub (forwards all traffic to all devices). The attacker can then inspect the traffic of all nodes of the local network.

#### The defense
Defense implementations vary from switch to switch. One good method is to restrict the number of addresses that can be associated with a port. Another is to enforce some sort of rate limiting on new CAM entries.

### ARP spoofing
#### The attack
Because there is no form of authentication with ARP, an attacker can send a gratuitous ARP for an address that isn't theirs: i.e. `attacker MAC` now lives at `victim IP`. Devices on the network will then update their ARP cache entries for the IP and route all new traffic to the attacker, allowing for DoS or MitM.

#### The defense
The most reliable defense is to have static ARP entries for important servers on the LAN. These can't be overwritten, an attacker can't spoof them. Network segmentation can help with this as well.

### VLAN hopping
#### Some definitions
A VLAN is a logical segmentation of networks (rather than physical). In other words, VLANs allow for multiple switches to isolate devices to different networks without the devices having to be on physically different switches. Switches share traffic via port connections called "trunks" - this allows traffic from any VLAN to get sent to this port. Generally, hosts are connected via ports that are associated with a specific VLAN.

#### The attack
If switch ports are not properly configured, the attacker can pretend to be a switch by sending a DTP message, and all vlan traffic will get routed to the attacker. This allows for packet sniffing, as well as the ability to communicate with devices on VLANs that perhaps that attacker wasn't meant to see.

#### The defense
Don't configure switch ports to `dynamic desirable`, `dynamic auto`, or `trunk`, unless you know that the device on the other side is legit.

### DHCP starvation
#### The attack
The purpose of this attack is to bring down a DHCP so an attacker can set up a rogue one and MitM all traffic on the network. The attacker simply needs to fill up the entire address pool of the DHCP server and then start a new DHCP server to do all sorts of nasty things.
A second way to abuse this is to abuse how DHCP determines if an address is in use - i.e. the server will send out ICMP/ARP requests to see if the IP is already in use before assigning an IP address to the requester, but an attacker can respond to these by impersonating a device that doesn't exist - therefore the DHCP server continuously thinks that there is no available IP address. At this point, an attacker can set up a rogue DHCP server and perform DNS poisoning, MitM, etc.

#### The defense
Port security, really - a single device shouldn't be able to claim hundreds of IP addresses. In addition, the network should own every DHCP response, so any DHCP responses coming from random devices should be blocked.


## Resources
<https://www.sans.org/reading-room/whitepapers/detection/detecting-responding-data-link-layer-attacks-33513>
<https://cybersecurity.att.com/blogs/security-essentials/vlan-hopping-and-mitigation>
<https://medium.com/bugbountywriteup/dhcp-starvation-attack-without-making-any-dhcp-requests-bef0022133c9>