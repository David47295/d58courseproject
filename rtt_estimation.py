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

class HostPairing():
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        self.count = 1

    def __lt__(self, other):
        return self.count < other.count

    def __eq__(self, other):
        return self.src == other.src and self.dst == other.dst

    def __str__(self):
        return self.src + " and " + self.dst + " with count " + str(self.count)

def rtt_estimation_packet_size(tcpflows):

    for i in range(len(TOP_THREE_PACKET_SIZE)):
        output = open("top3_packet_" + str(i) + ".csv", 'w')
        csv_writer = csv.writer(output, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["Flow", "RTT", "Estimated RTT"])
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
        # print(srtt)
        output.close()



def rtt_estimation_bytes_size(tcpflows):
    for i in range(len(TOP_THREE_BYTE_SIZE)):
        output = open("top3_bytes" + str(i) + ".csv", 'w')
        csv_writer = csv.writer(output, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["Flow", "RTT", "Estimated RTT"])
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
        output.close()



def rtt_estimation_duration(tcpflows):
    for i in range(len(TOP_THREE_LONGEST)):
        output = open("top3_longest" + str(i) + ".csv", 'w')
        csv_writer = csv.writer(output, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["Flow", "RTT", "Estimated RTT"])
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
        output.close()

def get_representative_rtt(flow):
    srtt = 0
    srtt_list = []

    for p in flow:
        if p["tcp.analysis.ack_rtt"] != '' and p["tcp.analysis.retransmission"] != '1':
            rtt = float(p["tcp.analysis.ack_rtt"])
            if srtt == 0:
                srtt = rtt
            else:
                srtt = (1 - ALPHA) * srtt + ALPHA * rtt

            srtt_list.append(srtt)
    srtt_list.sort()
    return srtt_list[len(srtt_list) // 2]

def rtt_estimation_most_connections(tcpflows):
    connections = []
    for k,v in tcpflows.items():
        src = v[0]["ip.src"]
        dst = v[0]["ip.dst"]
        curr_pair = HostPairing(src, dst)

        if curr_pair not in connections:
            connections.append(curr_pair)
        else:
            connections[connections.index(curr_pair)].count += 1

    connections.sort(reverse=True)
    top3 = connections[0:3]
    i = 0

    for top_pair in top3:
        estimated_rtt_list = []
        for k, flow in tcpflows.items():
            src = flow[0]["ip.src"]
            dst = flow[0]["ip.dst"]
            if src == top_pair.src and dst == top_pair.dst:
                estimated_rtt_list.append({'estimated_rtt': get_representative_rtt(flow), 'time_epoch' : flow[0]['frame.time_epoch']})

        new_estimated_rtt_list = sorted(estimated_rtt_list, key=lambda r:float(r['time_epoch']))
        output = open("most_connections" + str(i) + ".csv", 'w')
        csv_writer = csv.writer(output, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for ertt in new_estimated_rtt_list:
            csv_writer.writerow([ertt['estimated_rtt']])
        i += 1
        output.close()


