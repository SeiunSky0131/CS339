

# CS339 Computer Networks Chapter 1 -- Introduction

### 1. What is computer network?

A collection of autonomous computers interconnected by a single technology.

### 2. Classification

1. Media: Wired network, Wireless Network
2. Transmission Technology: Broadcast Network, Point-to-Point Network
3. Topology: Bus, Star, Ring, Tree
4. Scale: Personal Network, LAN, Metropolitan Network, WAN, Internet

### 3. Layering

<img src="/home/haoquan/CS339/Chap-1/pic1.png" alt="pic1" style="zoom:30%;" />

We use layering to describe a structure of Internet. It should obey following rules:

1. Lower layer provides **service** to the layer above it.
2. Peers talk with each other using **protocols**.
3. The information exchanged between layers using **interfaces**.

##### 3.1 TCP/IP Model

Apart from ISO 7-layer Model, TCP/IP Model is the most popular one due to its simplicity. There are 4 layers from top to bottom:

1. Application Layer
2. Transport Layer
3. Network Layer
4. Link Layer

##### 3.2 Hybrid Model in This Course

Extract the physical layer from the link layer and the model becomes:

1. Application Layer
2. Transport Layer
3. Network Layer
4. Link Layer
5. Physical Layer

### 4. Definition of Bandwidth

The definition of **Bandwidth** in CS is defined as the information carrying capacity, with the unit of **bits/sec**.

### 5. Baud Rate and Bit Rate

The **Baud Rate** is the number of samples or symbols **per second** sent by channel.

The **Bit Rate** is the total number of bits **per second** sent by channel.

Based on this, the transformation formula is
$$
\text{Bit Rate}= \text{Baud Rate} \times \text{bits per sample/symbol (Sample Rate)}
$$
For example, the telephone network we see usually has the **Sample Rate** of `8 bits/sample`, and the **Baud Rate** of `8000 samples/sec`, then we can calculate the **Bit Rate** as:
$$
\text{Bit Rate} = 8000 \times 8 = 64 \ \text{kbps}
$$

### 6. Shannon's Theorem

The **maximum data rate** in a noise channel with **signal-to-noise ratio** `S/N` (**with unit not in dB**) is:
$$
\text{maximum data rate} = H\log_{2}(1+S/N)
$$
where 
$$
H = \text{Bandwidth of the channel}
$$
and
$$
S/N \ \text{in dB} = 10\log_{10}(S/N)
$$

### 7. Throughput Vs. Bandwidth

**Throughput** is the real data rate in  the channel. And due to the limitation of bottleneck link, the throughput is usually smaller the bandwidth of the channel.

### 8. Data Encoding

**Purpose:** encode the data using 0 and 1 so that it can be transmitted using digital signal. Two popular examples are **Unicode** and **ASCII**. 

Three classes of transmission:

1. Analog signals Transmission for digital data: `QPSK` (popular)
2. Digital signals Transmission for digital data: Manchester encoding
3. Digital signals Transmission for analog data: Pulse Code Modulation

##### 8.1 `QPSK`

​	`QPSK` has 4 states dividing the whole range of signal, it can thus transmit 2 bits of data using one sample.

​	`QAM-16` has 16 states dividing the whole range of signal, it can thus transmit 4 bits of data using one sample.

​	`QAM-64` has 64 states dividing the whole range of signal, it can thus transmit 6 bits of data using one sample.

Conclusion: The number of valid states determine the number of bits per symbol.

<img src="/home/haoquan/CS339/Chap-1/pic2.png" alt="pic2" style="zoom:33%;" />

##### 8.2 Manchester Encoding

​                                                                    <img src="/home/haoquan/CS339/Chap-1/pic3.png" alt="pic3" style="zoom:33%;" />            	

Manchester encoding is easy to understand, it just inverse the signal at `negedge`. For differential Manchester, it use transition or not to indicate `0` or `1`.

### 9. Types of Links

1. Simplex: Just **one** direction from sender to receiver.
2. Half Duplex: Can switch the role of sender and receiver, but there can only be **one sender** at a given time.
3. Full Duplex: Both directions can send and receive information.

### 10. Communication Mode

There are two kinds of connection between devices, **parallel connection** containing several links and **serial connection** having all the connections transmitting through one line.

### 11. Multiplexing

Since there might be several connections sending data at the same time, **Multiplexing** is introduced. There are three major kinds of multiplexing:

1. TDM: Divide the time block into several slots and each user uses one of them to transmit. During transmission, one can use the **whole bandwidth**. The shortcoming is that there might be slots occupied by user but the user sends nothing. **ATDM** will get rid of these slots by asynchronously calling users that have data to transmit.
2. FDM: Divide the frequency spectrum into different blocks and each user sends in a specific frequency range. During transmission, one can only use **part of the bandwidth**.
3. CDMA: Use **Walsh matrix** to encode the transferred data, then use the same matrix to get back the original data. The short coming of CDMA is the hardness of keeping all the sending vectors orthogonal. Also, if there are less users than the dimension of matrix, a channel will be wasted.

### 12. Switching

Switching describes how messages are switched in the network structure, there are three kinds of switching:

1. Circuit Switching
2. Message Switching
3. Packet Switching

##### 12.1 Circuit Switching

The basic idea for circuit switching is that a **connection channel** or a **complete path** is built before the call, and the user can use the whole channel.

###### Advantages

The connection is stable, and **in-time**. It will enjoy dedicated resources.

###### Disadvantages

The channel is wasted if the user is idle and transmits no message.

###### Example

Telephone circuit.

##### 12.2 Packet Switching

The basic idea for packet switching is that the message is divided into packets. Packets are sent by switches/routers using **store-and-forward** approach. The **store-and-forward** approach means that the switch/router will wait until the whole packet has been received, and then send the packet to next hop.

###### Advantages

Resources shared according to demands, no resources are wasted.

###### Disadvantages

Cannot guarantee the bandwidth, congestion will happen if there are too many users sending at the same time.

###### Example

Internet

###### VC Circuit

VC circuit acts like a circuit switching network, but the underlying structure is packet switching. It assigns connection between two users a **VC number at the start of a session** and all the packets will follow the same route defined by the VC number. Thus, it will behave just like a circuit switching network.

###### Packet Loss

When buffer in the switch/router is full, the packet is dropped.

### 13. Router Nodal Delay & End-to-End Delay

$$
d_{nodal} = d_{proc}+d_{queue}+d_{trans}+d_{prop}
$$

$$
d_{proc} \  \text{is the time used to process the data into packet. For router, it needs time to check header, error and output link}
$$

$$
d_{queue} \ \text{is the time needed for a packet to wait to be transmitted in a queue}
$$

$$
d_{trans} \ \text{is the time needed to upload the packet from buffer to the wire/link by the router/host}
$$

$$
d_{prop} \ \text{is the time used for the wire/link to transmit the packet to the destination}
$$

**Note 1: Use the train going over a bridge model to solve this kind of question. (这种问题实际上就是一个火车过桥问题). Be aware that it also takes time for a router/receiver to download the packet from the wire. That is:**
$$
D_{end-to-end} = \sum d_{nodal} + \sum_{i = 2}^{n} d_{trans\_i} \qquad \text{（所有包上传的时间 +一个包在线上传输的时间）}
$$
Note 2: For Circuit switching, the total delay is
$$
D_{end-to-end} = D_{call-setup} +D_{trans} +D_{prop}
$$

### 14. Network Edge

Two kinds of models:

1. Client-server Model
2. Peer-to-peer Model

### 15. Network Core

Two kinds of transferring mode:

1. Circuit Switching
2. Packet Switching

The core consisted of several levels of ISPs (Internet Service Provider). From top to the bottom are:

1. Tier-1 ISP, like ChinaNet
2. Tier-2 ISP
3. Tier-3 ISP
4. Local ISP

### Homework and Quiz Review

![q1](/home/haoquan/CS339/Chap-1/q1.png)

**Explain: ** Use "火车过桥问题". This is false.

![q2](/home/haoquan/CS339/Chap-1/q2.png)

**Explain:** Use Shannon's Theorem:

First calculate the `S/N` not in dB:
$$
S/N \ \text{in dB} = 10\log_{10}(S/N) \Rightarrow S/N = 10^{3}
$$
Then calculate the maximum data rate use the `S/N` not in dB:
$$
\text{maximum data rate} = H\log_{2}(1+S/N) = 3\times 10^{3} \log_{2}(1+10^{3}) \approx 3 \times 10^{3} \times 10 = 30 \ \text{kbps}
$$
![](/home/haoquan/CS339/Chap-1/q3.png)

**Explain: ** Single technology means the same technology, not only the protocol layering, but also other technologies as a whole.

![q4](/home/haoquan/CS339/Chap-1/q4.png)

**Explain: **In most of the cases, the routers implement layer 1,2,3. Layer 4 and 5 are usually implemented in end systems.

![q5](/home/haoquan/CS339/Chap-1/q5.png)

**Explain:** Just consider the features of Circuit switching and Packet Switching, we find that they are corresponding to the features of TDM and ATDM. And thus we can conclude that TDM is suitable for Circuit switching and ATDM is suitable for Packet Switching.

![q6](/home/haoquan/CS339/Chap-1/q6.png)

**Explain: **Although physical bandwidth is the upper limit of the capacity, there might be other factors limiting the capacity. For example, the Baidu Yun.

![q7](/home/haoquan/CS339/Chap-1/q7.png)

**Explain: ** WAN and LAN also have different protocols.

![q8](/home/haoquan/CS339/Chap-1/q8.png)

**Explain: **It takes more space to encapsulate data using headers from different layers. If we only have one layer, we will have a unique header for a certain protocol, which takes less space.

![q59](/home/haoquan/CS339/Chap-1/q9.png)

**Explain: **Layer 1,2,3 protocols are usually implemented in hardware like NIC.

![q10](/home/haoquan/CS339/Chap-1/q10.png)

**Explain: **This is one of the advantage of the protocol layering. And it also obeys the spirit of encapsulating.
