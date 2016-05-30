# mininet-with-nfn-support

[Mininet](http://mininet.org/) is a network emulator, which creates a network of virtual hosts, switches, controllers, and links. Mininet hosts run standard Linux network software, and its switches support [OpenFlow](http://archive.openflow.org/wp/learnmore/) for highly flexible custom routing and Software-Defined Networking experimentation. 
This repository contains various scripts with [CCNlite](https://github.com/cn-uofbasel/ccn-lite) and CCNlite with [Named Function Networking](http://named-function.net/) (NFN) enabled support for Mininet, with the following topology:

             3              2     1
         s1 ------------------ s3----h4
      4/ |1\ 2               3/  \ 4
      /  |  \            10mb/    \
     h7  h1  h2            2/     5\   1
                          s2-3---3-s4--------h5
                            |      | \
                            |1    4|  \ 2
                           h3     h6   h8`

The scripts are in charge of setting up the emulation environment and initializing and configuring the *faces* (the word [Content-Centric Networking](http://www.ccnx.org) (CCN) gives to interfaces) for all the network elements involved in the named functions execution.
