# VXLAN
### About
First note that: 
1. layer 2 network = Link layer
2. layer 3 network = Network layer


`VXLAN` is a new technological trend that tends to replace `LAN`. The basic idea is overlaying the layer 2 network on the layer 3 network.

It encapsulates (tunnels) Ethernet frames in a VXLAN packet that includes IP addresses so that any two nodes in the layer 3 network that is originally connected physically, can be viewed two nodes directly connected in layer 2 network
