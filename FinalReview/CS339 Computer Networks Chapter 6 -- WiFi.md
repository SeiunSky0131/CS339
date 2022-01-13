# CS339 Computer Networks Chapter 6 -- WiFi

### 1. Wireless Link Characteristics

1. **Decreased signal strength**: consider the decreasing of the signal strength as:
   $$
   \text{power} \sim \frac{1}{d^2}
   $$

2. **Interference from other sources**: The standard wireless frequency (2.4GHz) is shared by numerous devices.

3. **Multipath propagation**: Since the reflection of signals is common in wireless communication, duplicated packets may arrive at receiver at lightly different time.

4. **SNR**: Signal to noise ratio, this is important to wireless transmission. Together with BER (bit error rate), these two parameters defines the efficiency of a transmission method. Usually, increase the SNR will decrease the BER, however, the power consumption will increase. Also, if we want to carry more data in one signal and keep the SNR unchanged, the BER will increase dramatically. If we want to carry more data in one signal and keep the BER unchanged, the SNR will increase.

<img src="/home/haoquan/CS339/Chap-6/chap6p1.png" alt="chap6p1" style="zoom:33%;" />

### 2. Hidden Terminal Problem and Exposed Terminal Problem

##### 2.1 Hidden Terminal Problem

If two hosts are separated by walls, they cannot hear each other. If they are both talking to another node `C`, they will not be aware of interference at that node `C`.

<img src="/home/haoquan/CS339/Chap-6/chap6p2.png" alt="chap6p2" style="zoom:33%;" />

##### 2.2 Exposed Terminal Problem

Consider there are three hosts `A,C` in one region, **`A` doesn't know the existence of `D` and `C` doesn't know the existence of `B`**. Now `A` is talking to `B`, `C` wants to open a new link with `D`. Since `C` doesn't know who is talking to`A`, it will choose not to open a new link to avoid potential interference. But actually this new link is legal. **This reduces the throughput**.

<img src="/home/haoquan/CS339/Chap-6/chap6p3.png" alt="chap6p3" style="zoom:33%;" />

### 3. Connect with AP -- Passive vs. Active

##### 3.1 Passive scanning

1. The AP broadcasts the beacon frames.
2. The host sends the request to the AP.
3. The AP sends back response to the host. (Connection built)

##### 3.2 Active scanning

1. The host sends probing frame.
2. The AP responds probing frame.
3. The host sends request to the AP.
4. The AP sends the response to the host. (Connection built)

### 4. CSMA/CA

We have mentioned that the hidden terminal problem prevents terminals from detecting collision. The wireless connection **cannot perform CSMA/CD** which abandons the transmission when detecting a collision. It thus uses CSMA/CA to avoid collision. When it detects the channel is busy, it will also back off for some time just as CSMA/CD does. However, the **timer will only decrease when the channel is idle**, which is more conservative. When the timer expires, the sender begins to resend. 

### 5. RTS and CTS

Another strategy is that the sender first sends a small packet to request the right to send. Only when it hears the receiver gives a CTS (clear to send) packet, it will start transmission. Note that **the clear to send message is broadcast**, so all the other senders know that the receiver is now receiving another packet. They will not send packet in this way. 

**Problem: This method is not efficient if all the message are small. It wastes time.**

### 6. Cellular Internet Access

1. Cell: consisted of base station, mobile users and air-interface
2. MSC: mobile switching center. Connect the cells to the wire net.
3. Public telephone network: A wired network direct to everywhere.

### 7. Differentiate 2G, 3G, and 4G LTE

2G: only voice network

3G: voice + data network

4G LTE: no separation between voice and data. Thus one can call a phone while go online.

### 8. Mobility

##### 8.1 Who to Handle?

Let the routing handle the move of device is one of the choice, however, it will place too much burden on the routers if there are millions of devices in the network.

So most of the conditions require the **end systems** to handle the move of devices.

##### 8.2 Indirect Routing

**Registration: **The foreign network will tell the home network that the device is here

**Communication: **Outside terminal call the home network, the home network will direct the packets to the foreign network. The foreign network will communicate with the device and send the response **directly to the sender.**

This is also called **triangle routing**, we can see that this is inefficient. Consider the case that the sender and the receiver are in the same network, they still need to communicate with the home network, which is inefficient.

<img src="/home/haoquan/CS339/Chap-6/chap6p4.png" alt="chap6p4" style="zoom:25%;" />

##### 8.3 Direct Routing

The sender just communicates with the home network **once** to get the address of the foreign network, and then **communicate with the foreign network directly**. This solves the triangle routing problem.

<img src="/home/haoquan/CS339/Chap-6/chap6p5.png" alt="chap6p5" style="zoom:25%;" />

##### 8.4 Further Moving

If the direct routing has already built, but the device moves to another foreign network, we can view the original foreign network as **anchor foreign network**. All the later packets will go to the new foreign network through the anchor foreign network router.

<img src="/home/haoquan/CS339/Chap-6/chap6p6.png" alt="chap6p6" style="zoom:25%;" />

### Homework and Quiz Review

<img src="/home/haoquan/CS339/Chap-6/q1.png" alt="q1" style="zoom:50%;" />

**Explain: **The transport layer and application layer protocols should be designed based on the mac and physical layer. Otherwise they will not be practical. We always consider the lower layers first.

<img src="/home/haoquan/CS339/Chap-6/q2.png" alt="q1" style="zoom:50%;" />

**Explain: **The modulation with high throughput has significantly larger **BER** (bit error rate). Thus we cannot always pursue the high throughput.

<img src="/home/haoquan/CS339/Chap-6/q3.png" alt="q1" style="zoom:50%;" />

**Explain: ** We mentioned that the exposed terminal problem can cause legal links' not building. This will decrease the throughput, not increase it.

<img src="/home/haoquan/CS339/Chap-6/q4.png" alt="q1" style="zoom:50%;" />

**Explain: **Should consider different cases. For small packets transmission scenario, RTS-CTS will not increase the throughput.

<img src="/home/haoquan/CS339/Chap-6/q5.png" alt="q1" style="zoom:50%;" />

**Explain: ** We can see that the first method implements mobility in routing part, while the second method implements mobility in end system. We know the first method is not suitable for large scale network, since the router needs to remember a lot of entries in this case.