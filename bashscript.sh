#bin/bash

echo "Generating univ1_pt3_tcp.csv"

tshark -r univ1_pt3 -n -T fields -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport -e tcp.stream -Y tcp -E header=y -E occurrence=f -E separator=, > univ1_pt3_tcp.csv

echo "Generating univ1_pt3_udp.csv"

tshark -r univ1_pt3 -n -T fields -e ip.src -e udp.srcport -e ip.dst -e udp.dstport -e udp.stream -Y udp -E header=y -E occurrence=f -E separator=, > univ1_pt3_udp.csv

