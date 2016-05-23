#!/usr/bin/python

# Author: Jose Castillo Lema <josecastillolema@gmail.com>

"""
         3              2     1
     s1 ------------------ s3----h4
  4/ |1\ 2               3/  \ 4
  /  |  \            10mb/    \
 h7  h1  h2            2/     5\   1
                      s2-3---3-s4--------h5
                        |      | \
                        |1    4|  \ 2
                       h3     h6   h8
""" 

import re
import time
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController
from mininet.cli import CLI

def toID(mac):
    return '0000' + re.sub('[:]', '', mac)

class MyTopo (Topo):
    def __init__(self, n=2, **opts):
        Topo.__init__(self, **opts)
	# Add hosts and switches
	h1 = self.addHost('h1')
	h2 = self.addHost('h2')
	h3 = self.addHost('h3')
	h4 = self.addHost('h4')
	h5 = self.addHost('h5')
	h6 = self.addHost('h6')
	h7 = self.addHost('h7')
	h8 = self.addHost('h8')
	s1 = self.addSwitch('s1', dpid=toID('00:00:00:00:00:01'))
	s2 = self.addSwitch('s2', dpid=toID('00:00:00:00:00:02'))
	s3 = self.addSwitch('s3', dpid=toID('00:00:00:00:00:03'))
	s4 = self.addSwitch('s4', dpid=toID('00:00:00:00:00:04'))

	# links Add
	self.addLink(s1, h1, 1, 1)
	self.addLink(s1, h2, 2, 1)
	self.addLink(s1, h7, 4, 1)
	self.addLink(s2, h3, 1, 1)
	self.addLink(s3, h4, 1, 1)
	self.addLink(s4, h5, 1, 1)
	self.addLink(s4, h8, 2, 1)
	self.addLink(s4, h6, 4, 1)
	self.addLink(s1, s3, 3, 2)
	self.addLink(s2, s3, 2, 3, bw=10, delay='200ms', jitter='2ms', loss=10, max_queue_size=1000, use_htb=True)
	self.addLink(s3, s4, 4, 5)
	self.addLink(s2, s4, 3, 3)

def inicializaRed():
    "Create network and run simple performance test"
    topo = MyTopo()
    #net = Mininet(topo=topo, link=TCLink, controller=RemoteController)
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    h1 = net.getNodeByName('h1')
    h2 = net.getNodeByName('h2')
                
    print '*** cleaning'
    h1.cmdPrint('killall -9 ccn-lite-relay >/dev/null 2>&1')
    h1.cmdPrint('killall -9 ccn-lite-crtl >/dev/null 2>&1')
    h1.cmdPrint('killall -9 ccn-lite-ccnb2x >/dev/null 2>&1')
    h1.cmdPrint('rm -f /tmp/ccnlite1.log /tmp/ccnlite2.sock')
    h1.cmdPrint('rm -f /tmp/mgnt-relay-a.sock /tmp/mgmt-relay-b.sock.sock')

    print '*** initializing servers:'
    h1.cmdPrint('/home/user/ccn-lite/bin/ccn-lite-relay -v trace -s ndn2013 -u 9998 -x /tmp/mgmt-relay-a.sock -v debug >/tmp/ccnlite1.log 2>&1 &')
    h2.cmdPrint('/home/user/ccn-lite/bin/ccn-lite-relay -v trace -s ndn2013 -u 9999 -x /tmp/mgmt-relay-b.sock -d /home/user/ccn-lite/test/ndntlv -v debug >/tmp/ccnlite2.log 2>&1 &')

    print '*** waiting for servers to wake up ...'

    #Connect mgntA with mgntB
    time.sleep(5)
    h1.cmdPrint("""export FACEID=`/home/user/ccn-lite/bin/ccn-lite-ctrl -x /tmp/mgmt-relay-a.sock newUDPface any 10.0.0.2 9999 | /home/user/ccn-lite/bin/ccn-lite-ccnb2xml | grep FACEID | sed -e 's/^[^0-9]*\\([0-9]\\+\\).*/\\1/'`""")
    h1.cmdPrint('/home/user/ccn-lite/bin/ccn-lite-ctrl -x /tmp/mgmt-relay-a.sock prefixreg /ndn $FACEID ndn2013 | /home/user/ccn-lite/bin/ccn-lite-ccnb2xml')

    #Execute tests
    print '*** executing NFN tests ...'
    h1.cmdPrint('/home/user/ccn-lite/bin/ccn-lite-peek -s ndn2013 -u 127.0.0.1/9998 "/ndn/test/mycontent" | /home/user/ccn-lite/bin/ccn-lite-pktdump -f 2')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    inicializaRed()
