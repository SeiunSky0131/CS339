from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSBridge
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import quietRun, dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from sys import argv
from threading import Thread
import time

class simpleTopo (Topo):
    def build( self ):
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        switch3 = self.addSwitch('s3')
        switch4 = self.addSwitch('s4')
        host1 = self.addHost('h1', cpu = .25)
        host2 = self.addHost('h2', cpu = .25)
        host3 = self.addHost('h3', cpu = .25)
        host4 = self.addHost('h4', cpu = .25)
        host5 = self.addHost('h5', cpu = .25)
        self.addLink(host1, switch1, bw = 100, delay = '5ms', loss = 0, use_htb = True)
        self.addLink(host2, switch2, bw = 200, delay = '5ms', loss = 0, use_htb = True)
        self.addLink(host3, switch2, bw = 100, delay = '5ms', loss = 0, use_htb = True)
        self.addLink(host4, switch4, bw = 100, delay = '5ms', loss = 0, use_htb = True)
        self.addLink(host5, switch4, bw = 200, delay = '5ms', loss = 0, use_htb = True)
        self.addLink(switch1, switch3, bw = 100, delay = '5ms', loss = 0, use_htb = True)
        self.addLink(switch2, switch3, bw = 200, delay = '5ms', loss = 0, use_htb = True)
        self.addLink(switch3, switch4, bw = 250, delay = '5ms', loss = 0, use_htb = True)

def myiperf(hostname1, hostname2, tcp, net):
    info("Testing bandwidth between " + hostname1 + " and " + hostname2 + " under TCP " + tcp + "\n" )
    h1, h2 = net.getNodeByName(hostname1, hostname2)
    net.iperf( [ h1, h2 ] )

def Test (tcp):
    topo = simpleTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, autoStaticArp=False)
    net.start()
    info( "Dumping host connections\n" )
    dumpNodeConnections(net.hosts)
    output = quietRun( 'sysctl -w net.ipv4.tcp_congestion_control=' + tcp )
    assert tcp in output
    t1 = Thread(target = myiperf, args = ('h1','h4',tcp, net))
    t2 = Thread(target = myiperf, args = ('h2','h5',tcp, net))
    #t3 = Thread(target = myiperf, args = ('h3','h5',tcp, net))
    t1.start();t2.start();#t3.start()

    t1.join();t2.join();#t3.join()
    net.stop()

if __name__ == '__main__':

  setLogLevel('info')
  
  # pick a congestion control algorithm, for example, 'reno', 'cubic', 'bbr', 'vegas', 'hybla', etc.
  tcp = 'bbr'

  Test(tcp)