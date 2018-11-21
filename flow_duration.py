import csv

def get_flow_durations(tcpflows, udpflows):
    tcp_output = open("tcp_flow_durations.csv", "w")
    tcp_writer = csv.writer(tcp_output, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    udp_output = open("udp_flow_durations.csv", "w")
    udp_writer = csv.writer(udp_output, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for k, v in tcpflows.items():
        duration = float(v[len(v)-1]["frame.time_epoch"]) - float(v[0]["frame.time_epoch"])
        tcp_writer.writerow([k, duration])

    for k, v in udpflows.items():
        duration = float(v[len(v) - 1]["frame.time_epoch"]) - float(v[0]["frame.time_epoch"])
        udp_writer.writerow([k, duration])

    tcp_output.close()
    udp_output.close()