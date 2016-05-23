# mininet-with-nfn-support

Various scripts with [CCNlite](https://github.com/cn-uofbasel/ccn-lite) and CCNlite with NFN enabled support for Mininet, with the following topology:

`         3              2     1
     s1 ------------------ s3----h4
  4/ |1\ 2               3/  \ 4
  /  |  \            10mb/    \
 h7  h1  h2            2/     5\   1
                      s2-3---3-s4--------h5
                        |      | \
                        |1    4|  \ 2
                       h3     h6   h8`
