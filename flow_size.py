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
            size += int(i["frame.len"])
        tcp_writer.writerow([k, size])

    for k, v in udpflows.items():
        size = 0
        for i in v:
            size += int(i["frame.len"])
        udp_writer.writerow([k, size])

    tcp_output.close()
    udp_output.close()

def get_flow_header_overhead(tcpflows):
    tcp_output = open("tcp_flow_overhead_ratio.csv", "w")
    tcp_writer = csv.writer(tcp_output, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for k, v in tcpflows.items():
        total_headers_size = 0
        total_data_sent = 0
        for i in v:
            tcp_header_len = int(i["tcp.hdr_len"])
            if i["tcp.len"].isdigit():
                tcp_payload_len = int(i["tcp.len"])
            else:
                tcp_payload_len = 0
            ip_header_len = int(i["ip.hdr_len"])
            frame_len = int(i["frame.len"])

            ip_packet_size = tcp_header_len + tcp_payload_len + ip_header_len
            total_headers_size += tcp_header_len + ip_header_len + (frame_len - ip_packet_size)
            total_data_sent += tcp_payload_len

        if (total_data_sent == 0):
            tcp_writer.writerow([k, 9999])
        else:
            tcp_writer.writerow([k, float(total_headers_size / total_data_sent)])

    tcp_output.close()
