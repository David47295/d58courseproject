PATH = "/home/radiantwings/Documents/univ1_trace/univ1_pt3"

def process_pcap():
    pcap = PcapReader(PATH)



    tcpflows = {}
    udpflows = {}
    i = 0

    for p in pcap:
        # print(i)
        if IP in p:
            if TCP in p:
                a_to_b = p[IP].src + ":" + str(p[TCP].sport) + " -> " + p[IP].dst + ":" + str(p[TCP].dport)
                b_to_a = p[IP].dst + ":" + str(p[TCP].dport) + " -> " + p[IP].src + ":" + str(p[TCP].sport)
                # if a_to_b in flows or b_to_a in flows:
                #     flows[a_to_b].append(p)
                # else:
                if a_to_b not in tcpflows and b_to_a not in tcpflows:
                    tcpflows[a_to_b] = []
                if a_to_b in tcpflows:
                    tcpflows[a_to_b].append(p.time)
                elif b_to_a in tcpflows:
                    tcpflows[b_to_a].append(p.time)
            elif UDP in p:
                # print("UDP found")
                a_to_b = p[IP].src + ":" + str(p[UDP].sport) + " -> " + p[IP].dst + ":" + str(p[UDP].dport)
                b_to_a = p[IP].dst + ":" + str(p[UDP].dport) + " -> " + p[IP].src + ":" + str(p[UDP].sport)
                # if a_to_b in flows or b_to_a in flows:
                #     flows[a_to_b].append(p)
                # else:
                if a_to_b not in udpflows and b_to_a not in udpflows:
                    udpflows[a_to_b] = []
                if a_to_b in udpflows:
                    udpflows[a_to_b].append(p.time)
                elif b_to_a in udpflows:
                    udpflows[b_to_a].append(p.time)
            # if (i > 200):
            #
            #     for k, v in flows.items():
            #         print(k, v)
            #     quit(1)
            i += 1

    return [tcpflows, udpflows]