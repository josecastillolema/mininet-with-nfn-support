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
    #switches = net.getNodeByName('s1', 's2', 's3', 's4')
    h1 = net.getNodeByName('h1')
    h2 = net.getNodeByName('h2')
    #for i in switches:
        #cmd = 'touch DOCTOR'
        #i.cmdPrint(cmd+i.__str__())
        #i.cmd(cmd)   
                
    print '*** cleaning:'
    h1.cmdPrint('killall -9 ccn-nfn-relay >/dev/null 2>&1')
    h1.cmdPrint('killall -9 ccn-nfn-proxy.py >/dev/null 2>&1')
    h1.cmdPrint('rm -f /tmp/mgmt1.sock /tmp/mgmt2.sock')
    h1.cmdPrint('rm -f /tmp/nfn0.log /tmp/nfn1.log /tmp/nfn2.log')

    print '*** initializing servers:'    
    h1.cmdPrint('/home/user/ccn-lite/bin/ccn-nfn-relay -s ndn2013 -u 9000 -x /tmp/mgmt1.sock -v debug >/tmp/nfn0.log 2>&1 &')
    h2.cmdPrint('/home/user/ccn-lite/bin/ccn-nfn-relay -s ndn2013 -u 9001 -x /tmp/mgmt2.sock -v debug >/tmp/nfn1.log 2>&1 &')
    h2.cmdPrint('/home/user/ccn-lite/src/py/ccn-nfn-proxy.py -u 127.0.0.1/9001 9002 >/tmp/nfn2.log 2>&1 &')

    print '*** waiting for servers to wake up ...'
    
    #Connect mgmt1 with mgmt2
    time.sleep(5)
    h1.cmdPrint('/home/user/ccn-lite/bin/ccn-lite-ctrl -x /tmp/mgmt1.sock newUDPface any 10.0.0.2 9001 | /home/user/ccn-lite/bin/ccn-lite-ccnb2xml | grep ACTION')
    h1.cmdPrint('/home/user/ccn-lite/bin/ccn-lite-ctrl -x /tmp/mgmt1.sock prefixreg /pynfn 2 | /home/user/ccn-lite/bin/ccn-lite-ccnb2xml | grep ACTION')

    #Connect mgmt2 with proxy (=computeserver)
    h2.cmdPrint('/home/user/ccn-lite/bin/ccn-lite-ctrl -x /tmp/mgmt2.sock newUDPface any 127.0.0.1 9002 | /home/user/ccn-lite/bin/ccn-lite-ccnb2xml | grep ACTION')
    h2.cmdPrint('/home/user/ccn-lite/bin/ccn-lite-ctrl -x /tmp/mgmt2.sock prefixreg /pynfn 2 | /home/user/ccn-lite/bin/ccn-lite-ccnb2xml | grep ACTION')

    #Add content to mgmt2, register it
    h2.cmdPrint('/home/user/ccn-lite/bin/ccn-lite-ctrl -x /tmp/mgmt2.sock addContentToCache /home/user/ccn-lite/test/py/computation_content.ndntlv | /home/user/ccn-lite/bin/ccn-lite-ccnb2xml | grep ACTION')
    h1.cmdPrint('/home/user/ccn-lite/bin/ccn-lite-ctrl -x /tmp/mgmt1.sock prefixreg /test 2 | /home/user/ccn-lite/bin/ccn-lite-ccnb2xml | grep ACTION')
    
    #Execute tests
    print '*** executing NFN tests ...'
    h1.cmdPrint('/home/user/ccn-lite/test/py/nfnproxy-test3B.py')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    inicializaRed()
