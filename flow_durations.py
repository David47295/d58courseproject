from scapy.all import *
import csv
from util import *


if __name__ == "__main__":
    fuck = process_pcap()
    tcpflows = fuck[0]
    udpflows = fuck[1]

    output = open("tcp_flow_durations.csv", "w")
    tcp_writer = csv.writer(output, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    udp_output = open("udp_flow_durations.csv", "w")
    udp_writer = csv.writer(udp_output, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for k, v in tcpflows.items():
        # print(k, v)
        tcp_writer.writerow([k, v[len(v) - 1] - v[0]])

    print("============================UDP FLOWS============================")
    for k, v in udpflows.items():
        print(k, v)
        udp_writer.writerow([k, v[len(v) - 1] - v[0]])

    output.close()
    udp_output.close()

