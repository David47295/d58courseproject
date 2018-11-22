import csv

TOP_THREE_PACKET_SIZE = ["244.3.160.248:52750 -> 41.177.26.193:80",
                         "41.177.3.224:52544 -> 244.3.176.149:8752",
                         "41.177.3.224:38186 -> 41.177.117.184:1618"]

TOP_THREE_BYTE_SIZE = ["244.3.160.248:52750 -> 41.177.26.193:80",
                         "41.177.3.224:52544 -> 244.3.176.149:8752",
                         "244.3.160.248:52444 -> 41.177.26.193:80"]

TOP_THREE_LONGEST = ["210.197.167.105:3237 -> 41.177.26.15:80",
                     "193.135.161.57:62747 -> 41.177.26.46:80",
                     "244.3.210.254:5900 -> 41.177.244.185:51175"]
ALPHA = 1/8

BETA = 1/4

G = 1

K = 4

def rtt_estimation_packet_size(tcpflows):
    output = open("rtt_estimation_top3_packet.csv", 'w')
    csv_writer = csv.writer(output, delimiter=',',
                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(["Flow", "RTT", "Estimated RTT"])

    for i in range(len(TOP_THREE_PACKET_SIZE)):
        srtt = 0
        rttvar = 0
        # rto = 0
        flow = tcpflows[TOP_THREE_PACKET_SIZE[i]]
        for p in range(len(flow)):
            if flow[p]["tcp.analysis.ack_rtt"] != '' and flow[p]["tcp.analysis.retransmission"] != '1':
                rtt = float(flow[p]["tcp.analysis.ack_rtt"])
                if srtt == 0:
                    srtt = rtt
                    rttvar = rtt/2
                else:
                    rttvar = (1 - BETA) * rttvar + BETA * abs(srtt - rtt)
                    srtt = (1 - ALPHA) * srtt + ALPHA * rtt
                # rto = srtt + max(G, K * rttvar)
                csv_writer.writerow([TOP_THREE_PACKET_SIZE[i], rtt, srtt])
                # if (rto < 1):
                #     rto = 1
                # elif (rto > 60):
                #     rto = 60
        print(srtt)

    output.close()

def rtt_estimation_bytes_size(tcpflows):
    output = open("rtt_estimation_top3_bytes.csv", 'w')
    csv_writer = csv.writer(output, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(["Flow", "RTT", "Estimated RTT"])

    for i in range(len(TOP_THREE_BYTE_SIZE)):
        srtt = 0
        rttvar = 0
        # rto = 0
        flow = tcpflows[TOP_THREE_BYTE_SIZE[i]]
        for p in range(len(flow)):
            if flow[p]["tcp.analysis.ack_rtt"] != '' and flow[p]["tcp.analysis.retransmission"] != '1':
                rtt = float(flow[p]["tcp.analysis.ack_rtt"])
                if srtt == 0:
                    srtt = rtt
                    rttvar = rtt / 2
                else:
                    rttvar = (1 - BETA) * rttvar + BETA * abs(srtt - rtt)
                    srtt = (1 - ALPHA) * srtt + ALPHA * rtt
                # rto = srtt + max(G, K * rttvar)
                csv_writer.writerow([TOP_THREE_BYTE_SIZE[i], rtt, srtt])
                # if (rto < 1):
                #     rto = 1
                # elif (rto > 60):
                #     rto = 60
        print(srtt)

    output.close()

def rtt_estimation_duration(tcpflows):
    output = open("rtt_estimation_top3_longest.csv", 'w')
    csv_writer = csv.writer(output, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(["Flow", "RTT", "Estimated RTT"])

    for i in range(len(TOP_THREE_LONGEST)):
        srtt = 0
        rttvar = 0
        # rto = 0
        flow = tcpflows[TOP_THREE_LONGEST[i]]
        for p in range(len(flow)):
            if flow[p]["tcp.analysis.ack_rtt"] != '' and flow[p]["tcp.analysis.retransmission"] != '1':
                rtt = float(flow[p]["tcp.analysis.ack_rtt"])
                if srtt == 0:
                    srtt = rtt
                    rttvar = rtt / 2
                else:
                    rttvar = (1 - BETA) * rttvar + BETA * abs(srtt - rtt)
                    srtt = (1 - ALPHA) * srtt + ALPHA * rtt
                # rto = srtt + max(G, K * rttvar)
                csv_writer.writerow([TOP_THREE_LONGEST[i], rtt, srtt])
                # if (rto < 1):
                #     rto = 1
                # elif (rto > 60):
                #     rto = 60
        print(srtt)

    output.close()
