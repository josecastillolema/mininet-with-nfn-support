# mininet-with-nfn-support

Mininet (LANTZ; HELLER; MCKEOWN, 2010) is a network emulator, which creates a network of virtual hosts, switches, controllers, and links. Mininet hosts run standard Linux network software, and its switches support OpenFlow (MCKEOWN et al., 2008) for highly flexible custom routing and Software-Defined Networking experimentation. 
Various scripts with [CCNlite](https://github.com/cn-uofbasel/ccn-lite) and CCNlite with Named Function Networking (NFN) enabled support for Mininet, with the following topology:

             3              2     1
         s1 ------------------ s3----h4
      4/ |1\ 2               3/  \ 4
      /  |  \            10mb/    \
     h7  h1  h2            2/     5\   1
                          s2-3---3-s4--------h5
                            |      | \
                            |1    4|  \ 2
                           h3     h6   h8`

The scripts are in charge of setting up the emulation environment and initializing and configuring the *faces* (the word CCN gives to interfaces) for all the network elements involved in the named functions execution.
