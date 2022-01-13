# CS339 Computer Networks Chapter 5 -- Data Link Layer

### 1. Link Layer Protocols

Link Layer Protocols include `Ethernet, HDLC, PPP`, they are usually implemented in NIC. Note that `HDLC` **implements reliable data transfer**, while `Ethernet and PPP` are **unreliable**.

### 2. Broadcast Links Vs. Point-to-point Links

Broadcast Link: `Ethernet`

Point to Point Link: `PPP`, `HDLC`

### 3. Framing Techniques:

##### 3.1 Character Count

This is easy, the frame contains a character that counts how many characters there are in a frame.

##### 3.2 Stuffing

Note that the minimum data size transferred in link layer is **46 bytes**. So when the data transferred by the link layer is less than this number, the link layer has to fill up the gap. There are two kinds of stuffing techniques:

**Byte Stuffing: **Use `01111110` as a stuffing byte. The sender will add another `01111110` byte if it encounters a `01111110` in the original byte. When the receiver finds two duplicated `01111110` byte, it will discard the later one. If the receiver finds one `01111110` byte, it is a flag indicating the end of frame.

**Bit Stuffing: **When the sender encounters five consecutive `1`, it adds one `0` after the fifth `1`. When the receiver find five consecutive `1`, it will removes the `0` after them.

### 4. HDLC and PPP

`HDLC` is a protocol allows congestion control and error detection, it uses `CRC` to check the potential error.

`PPP` is based on `HDLC`, but it drops the congestion control and error detection part.

### 5. Three Classes of MAC Protocols

##### 5.1 Channel Partition

Traditional channel partition rules like TDM, FDM, CDM

##### 5.2 Random Access

The senders can randomly access the channel. Collisions may happen, but the senders have the ability to recover from collison.

##### 5.3 Taking Turns

Nodes take turns to send data.

### 6. Random Access MAC Protocols

Random access will make node transmit at full channel data rate `R` if it has something to send. If there is collision, it is protocols responsibility to detect it and recover from collision. The examples are:

1. ALOHA, slotted ALOHA
2. CSMA, CSMA/CD, CSMA/CA

##### 6.1 Pure ALOHA

Pure ALOHA will require that when the packet is transmitting at time `t0`, no other node is transmitting in the interval `[t0-1,t0+1]`. If it detects collision, it will wait for a random time and retry.

The efficiency of pure ALOHA can be calculated as
$$
P  = P(\text{node transmits}) \times P(\text{no other node transmits in [$t_{0}-1, t_{0}$]}) \times P(\text{no other node transmits in $[t_{0},t_{0}+1]$}) \approx 0.18
$$

##### 6.2 Slotted ALOHA

Slotted ALOHA divides the time into different slots, each slot allows one node to transmit. This avoids the case that one node's transmitting ruins two slots, the efficiency doubles.

**Problem of ALOHA: **a node's transmission decision is independent of other node's activities.

##### 6.3 CSMA

Nodes will detect the channel before it transmits. Only if the channel is idle, it begins transmission. If it detects the channel is busy:

1. 1-persistent. Keep detecting the channel, retransmit as soon as the channel is idle.
2. non-persistent. Wait a random time and then retransmit.
3. p-persistent. When the channel is idle, it will begin transmission with possibility `p`. It will wait to the next slot and begin transmission with possibility `1-p`.

**Problem of CSMA: **There is possibility that the collision happens while the packet is transmitting, but it is unable to be detected when the slot began. Or one can think the collision detection takes time.

##### 6.4 CSMA/CD

Based on CSMA, when the collision is detected, abort the colliding transmission.

**CSMA/CD with Exponential Backoff: **When collision detected for the `m`th time, abort the transmission and wait for
$$
rand[0,2^m-1] \times 2\tau
$$
time and then retransmit. The idea is that when the collision is frequent, do backoff more.

### 7. Minimum Frame Length

To avoid the condition that the **packet has totally been sent to the channel, and there is a collision**, which makes the sender wrongly assume the packet is sent successfully, the frame length should be long enough. To calculate:
$$
F_{min} = 2\times B \times \frac{l}{v}
$$

$$
l \text{ is the length of the wire and } v \text{ is the propagation speed in the wire } B \text{ is the bandwidth}
$$

### 8. Taking Turns

Both Channel Partition and Random Access have their shortcoming. The channel partition is good at high load but not efficient in low load. The random access is good at low load but not efficient in high load. Taking turns is collision free and looks for the best among the above two. 

Taking turns have different ways, like:

1. Binary Countdown. Use binary numbers and compare them digit by digit. The host with the biggest number transmits first.
2. Polling. Master node invites slave nodes to transmit in turn
3. Token passing. Passing token between hosts. Only host with token has the right to transmit.

### 9. MAC Address

A MAC address has 48 bits. MAC address and IP address are serving for their layers in order to keep layers independent. Otherwise the network layer will be very busy if there is no link layer. Also, the link layer not only serves IP protocols. 

### 10. Ethernet Efficiency

$$
efficiency = \frac{1}{1+5\frac{t_{prop}}{t_{trans}}}
$$

From that we can know that Ethernet or CSMA/CD is not efficient for high speed and long distance network, for the propagation time is long/transmission time is short, which decreases the efficiency.

### 11. Devices Connecting Networks

##### 11.1 Hub

Hub is a simple repeater, it will just repeat the information going in from one link through all the links.

##### 11.2 Switch (2-layer switch)

Switch is smarter than the hub, it knows which output link is when a frame comes from one of the link. However, if the frame's destination is unknown, namely, not in the forwarding table, the switch will also **broadcast** the frame to all the links as hub does. 

##### 11.3 Router

Router will not broadcast, other properties are just the same as switch.

##### 11.4 Broadcasting Region and Collision Region

**Switch can reduce the collision region**, since the collision will happen with in one of the its links. The switch itself will not be included in the collision region. **Router can reduce the broadcasting region**, since the router will not broadcast the frame, the router itself will not be included in the broadcasting region.

<img src="/home/haoquan/CS339/Chap-5/chap5p1.png" alt="chap5p1" style="zoom:33%;" />

### 12. VLAN

**Problem of LAN based on switch: ** As we have seen that the broadcasting region of switch connected network is still the whole network. This has huge privacy issue. Also, it is not convenient to move a device from one LAN to another LAN, but keeping the connection with original LAN.

The **idea** of `VLAN` is viewing one physical switch as several **virtual switches**. These **virtual switches** are not connected with each other. In this way, the broadcasting region is reduced to the region within a **virtual switch**. The communication between different broadcasting regions need **a router overhead or a 3-layer switch**.

Also, we can use trunk ports to connect several physical switches, these physical switches can be divided into several `VLAN` **as a whole**.

<img src="/home/haoquan/CS339/Chap-5/chap5p2.png" alt="chap5p2" style="zoom:33%;" />

### 13. Data Center

![chap5p3](/home/haoquan/CS339/Chap-5/chap5p3.png)

### 14. A Day in the Life of a Web Request

1. `DHCP` gets the gateway router `IP` and the `IP` of this host, as well as the `IP` of DNS server.
2. `ARP` gets the MAC of gateway router
3. `DNS` gets the `IP` of the website
4. `TCP` connection established
5. `HTTP` protocols will load the content of the website.

### Homework and Quiz Review

<img src="/home/haoquan/CS339/Chap-5/q1.png" alt="q1" style="zoom:50%;" />

**Explain: **Here we must distinguish the reliable data transfer in link layer and the reliable data transfer in transport layer. The link layer is reliable if the frame can be transmit identically between two hops/hosts (e.g. Two neighboring routers). But it cannot rule out the possibility that the frame **gets lost when queuing in the router due to congestion**. In other word, the link layer does not know what happens in the routers. This is the responsibility of transport layer.

<img src="/home/haoquan/CS339/Chap-5/q2.png" alt="q1" style="zoom:50%;" />

**Explain: **Bit stuffing requires the sender to add `0` after 5 consecutive `1`, which is indeed the case here.

<img src="/home/haoquan/CS339/Chap-5/q3.png" alt="q1" style="zoom:50%;" />

**Explain: ** One of the shortcomings of ALOHA is that the nodes do not know the action of other nodes. CSMA/CD solves this problem by sensing the channel before transmission.

<img src="/home/haoquan/CS339/Chap-5/q4.png" alt="q1" style="zoom:50%;" />

**Explain: **Note that the collision only happens when both hosts can transmit at the same time. Both half-duplex and full-duplex links will not have collision problem. Then it will not require CSMA/CD definitely.

<img src="/home/haoquan/CS339/Chap-5/q5.png" alt="q1" style="zoom:50%;" />

**Explain: **Note that A and B are not in the same subnet. This means that they have to communicate through the gateway router. It becomes the gateway router's responsibility to get the MAC address of B. A will just send the IP address of B to the gateway router.

<img src="/home/haoquan/CS339/Chap-5/q6.png" alt="q1" style="zoom:50%;" />

**Explain: ** Switch reduces collision region, router reduces broadcasting region.

<img src="/home/haoquan/CS339/Chap-5/q7.png" alt="q1" style="zoom:50%;" />

**Explain: **As discussed in definition of `VLAN`, since the virtual switches cannot directly talk to each other, they need a router or 3-layer switch.

<img src="/home/haoquan/CS339/Chap-5/q8.png" alt="q1" style="zoom:50%;" />

**Explain: **L3 switches runs in network layer, which means it needs configure the `IP` address. Recall we configured the router in our dorm when we entered SJTU.

<img src="/home/haoquan/CS339/Chap-5/q9.png" alt="q1" style="zoom:50%;" />

**Explain: **The network always has cycles. Cannot "因噎废食".

<img src="/home/haoquan/CS339/Chap-5/q10.png" alt="q1" style="zoom:50%;" />

**Explain: **RDMA has transport layer protocols implemented in NIC.
