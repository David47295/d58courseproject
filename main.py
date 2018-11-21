from scapy.all import *
import csv
# from util import *
TCP_FILE_PATH = "/home/radiantwings/PycharmProjects/d58courseproject/univ1_pt3_tcp.csv"
UDP_FILE_PATH = "/home/radiantwings/PycharmProjects/d58courseproject/univ1_pt3_udp.csv"


if __name__ == "__main__":
    tcp_file = open(TCP_FILE_PATH, 'r')
    # tcp_reader = csv.reader(tcp_file, delimiter=',', quotechar='|')
    tcp_reader = csv.DictReader(tcp_file)

    # pcap = PcapReader(PATH)

    tcpflows = {}
    udpflows = {}
    i = 0

    for row in tcp_reader:

        a_to_b = row["ip.src"] + ":" + row["tcp.srcport"] + " -> " + row["ip.dst"] + ":" + row["tcp.dstport"]
        b_to_a = row["ip.dst"] + ":" + row["tcp.dstport"] + " -> " + row["ip.src"] + ":" + row["tcp.srcport"]

        is_recorded = a_to_b in tcpflows
        is_inverse_recorded = b_to_a in tcpflows

        if not is_recorded and not is_inverse_recorded:
            tcpflows[a_to_b] = []
        if is_recorded:
            tcpflows[a_to_b].append(row)
        elif is_inverse_recorded:
            tcpflows[b_to_a].append(row)

        if (i > 200):
            for k, v in tcpflows.items():
                print(k,v)
            quit(1)
        i += 1


    output = open("tcp_flow_durations.csv", "w")
    tcp_writer = csv.writer(output, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    udp_output = open("udp_flow_durations.csv", "w")
    udp_writer = csv.writer(udp_output, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for k, v in tcpflows.items():
        print(k, v)
        tcp_writer.writerow([k, v[len(v) - 1].time - v[0].time])

    for k, v in udpflows.items():
        # print(k, v)
        udp_writer.writerow([k, v[len(v) - 1].time - v[0].time])

    output.close()
    udp_output.close()

    # tcp_output = open("tcp_flow_sizes_packets.csv", "w")
    # tcp_writer = csv.writer(output, delimiter=',',
    #                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #
    # udp_output = open("udp_flow_sizes_packets.csv", "w")
    # udp_writer = csv.writer(udp_output, delimiter=',',
    #                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #
    # for k, v in tcpflows.items():
    #     print(k, v)
    #     tcp_writer.writerow([k, len(v)])