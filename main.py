from scapy.all import *
import csv
# from util import *
TCP_FILE_PATH = "/home/radiantwings/PycharmProjects/d58courseproject/univ1_pt3_tcp.csv"
UDP_FILE_PATH = "/home/radiantwings/PycharmProjects/d58courseproject/univ1_pt3_udp.csv"


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

    print("Writing to file")

    tcp_output = open("tcp_flow_durations.csv", "w")
    tcp_writer = csv.writer(tcp_output, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    udp_output = open("udp_flow_durations.csv", "w")
    udp_writer = csv.writer(udp_output, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for k, v in tcpflows.items():
        duration = 0
        for p in v:
            duration += float(p["tcp.time_delta"])
        tcp_writer.writerow([k, duration])

    for k, v in udpflows.items():

        udp_writer.writerow([k, float(v[len(v) - 1]["frame.time_epoch"]) - float(v[0]["frame.time_epoch"])])

    tcp_output.close()
    udp_output.close()

