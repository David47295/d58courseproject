import csv

def get_flow_size_in_packets(tcpflows, udpflows):
    tcp_output = open("tcp_flow_size_packets.csv", "w")
    tcp_writer = csv.writer(tcp_output, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    udp_output = open("udp_flow_size_packet.csv", "w")
    udp_writer = csv.writer(udp_output, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for k,v in tcpflows.items():
        tcp_writer.writerow([k, len(v)])

    for k,v in udpflows.items():
        udp_writer.writerow([k, len(v)])

    tcp_output.close()
    udp_output.close()

def get_flow_size_in_bytes(tcpflows, udpflows):
    tcp_output = open("tcp_flow_size_bytes.csv", "w")
    tcp_writer = csv.writer(tcp_output, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    udp_output = open("udp_flow_size_bytes.csv", "w")
    udp_writer = csv.writer(udp_output, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)



    for k, v in tcpflows.items():
        size = 0
        # print(k, " : ", v)
        for i in v:
            if i['tcp.len'].isdigit():
                size += int(i["tcp.len"])
        tcp_writer.writerow([k, len(v)])

    for k, v in udpflows.items():
        size = 0
        for i in v:
            size += int(i["udp.length"])
        udp_writer.writerow([k, size])

    tcp_output.close()
    udp_output.close()