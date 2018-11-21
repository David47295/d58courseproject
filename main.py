from scapy.all import *
import csv
from utils import *
from flow_size import *
from flow_duration import get_flow_durations


if __name__ == "__main__":
    tcp_file = open(TCP_FILE_PATH, 'r')
    # tcp_reader = csv.reader(tcp_file, delimiter=',', quotechar='|')
    tcp_reader = csv.DictReader(tcp_file)

    tcpflows = {}
    udpflows = {}

    for row in tcp_reader:

        a_to_b = row["ip.src"] + ":" + row["tcp.srcport"] + " -> " + row["ip.dst"] + ":" + row["tcp.dstport"]
        b_to_a = row["ip.dst"] + ":" + row["tcp.dstport"] + " -> " + row["ip.src"] + ":" + row["tcp.srcport"]

        is_recorded = a_to_b in tcpflows
        is_inverse_recorded = b_to_a in tcpflows

        if not is_recorded and not is_inverse_recorded:
            tcpflows[a_to_b] = [row]
        elif is_recorded:
            tcpflows[a_to_b].append(row)
        elif is_inverse_recorded:
            tcpflows[b_to_a].append(row)

    tcp_file.close()

    udp_file = open(UDP_FILE_PATH, 'r')
    # tcp_reader = csv.reader(tcp_file, delimiter=',', quotechar='|')
    udp_reader = csv.DictReader(udp_file)

    for row in udp_reader:

        a_to_b = row["ip.src"] + ":" + row["udp.srcport"] + " -> " + row["ip.dst"] + ":" + row["udp.dstport"]
        b_to_a = row["ip.dst"] + ":" + row["udp.dstport"] + " -> " + row["ip.src"] + ":" + row["udp.srcport"]

        is_recorded = a_to_b in udpflows
        is_inverse_recorded = b_to_a in udpflows

        if not is_recorded and not is_inverse_recorded:
            udpflows[a_to_b] = [row]
        elif is_recorded:
            udpflows[a_to_b].append(row)
        elif is_inverse_recorded:
            udpflows[b_to_a].append(row)

    udp_file.close()

    print("================RESULTS================")

    # get_flow_durations(tcpflows, udpflows)

    # get_flow_size_in_packets(tcpflows, udpflows)

    get_flow_size_in_bytes(tcpflows, udpflows)
