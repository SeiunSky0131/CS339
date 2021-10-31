from re import VERBOSE
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import time

class CStopo(Topo):
   def build(self, **_opts):
       s1 = self.addSwitch('s1')
       h1 = self.addHost('h1', ip = '10.0.0.2')

       h2,h3,h4,h5,h6 = [self.addHost(h) for h in ('h2','h3','h4','h5','h6')]
       for h in [h1,h2,h3,h4,h5,h6]:
           self.addLink(h, s1, bw = 100)

def run():
    "Test linux router"
    topo = CStopo()
    net = Mininet( topo=topo,
                   waitConnected=True )  # controller is used by s1-s3
    net.start()
    start = time.time()
    h1,h2,h3,h4,h5,h6 = [net.get(h) for h in ('h1','h2','h3','h4','h5','h6')]
    h1.sendCmd('python3 TCPServer.py')
    # time.sleep(1)
    h2.sendCmd('python3 TCPClient.py')

    h2.waitOutput(verbose = True)
    finish = time.time()
    print('total time cost is %d seconds'%(finish - start))

    CLI( net )
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    run()