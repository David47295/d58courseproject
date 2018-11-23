import csv

def calculate_packet_interarrival(tcpflows, udpflows):
    tcp_output = open("tcp_interpacket.csv", "w")
    tcp_writer = csv.writer(tcp_output, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    udp_output = open("udp_interpacket.csv", "w")
    udp_writer = csv.writer(udp_output, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for k, flow in tcpflows.items():
        for i in range(1,len(flow)):
            time = float(flow[i]["frame.time_epoch"]) - float(flow[i-1]["frame.time_epoch"])
            tcp_writer.writerow([time])

    for k, flow in udpflows.items():
        for i in range(1,len(flow)):
            time = float(flow[i]["frame.time_epoch"]) - float(flow[i-1]["frame.time_epoch"])
            udp_writer.writerow([time])

    tcp_output.close()
    udp_output.close()