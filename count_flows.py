from scapy.all import *
PATH = "/home/radiantwings/Documents/univ1_trace/univ1_pt3"

def is_same_src(pkt1, pkt2, type):
    if IP in pkt1 and IP in pkt2:
        return (pkt1[IP].src == pkt2[IP].src and
                pkt1[type].sport == pkt2[type].sport
        )

def is_same_dst(pkt1, pkt2, type):
    if IP in pkt1 and IP in pkt2:
        return ((pkt1[IP].dst == pkt2[IP].dst and
                pkt1[type].dport == pkt2[type].dport)
        )

def is_within_arrival_timeframe(pkt1, pkt2):
    return (
        pkt1.time - pkt2.time < 540000
    )

def is_b_to_a(pkt1, pkt2, type):
    if IP in pkt1 and IP in pkt2 and type in pkt1 and type in pkt2:
        return (
            pkt1[IP].src == pkt2[IP].dst and
            pkt1[type].sport == pkt2[type].dport and
            pkt2[IP].src == pkt1[IP].dst and
            pkt2[type].sport == pkt1[type].dport
        )

def is_part_of_flow(pkt1, pkt2, type):
    if type in pkt1 and type in pkt2:
       return (is_same_src(pkt1, pkt2, type) and
               is_same_dst(pkt1, pkt2, type) and
               is_within_arrival_timeframe(pkt1, pkt2)
       )
    return False


if __name__ == "__main__":
    pcap = PcapReader(PATH)

    prev = None

    tcp_flows = 0
    udp_flows = 0
    i=0

    for p in pcap:
        i += 1
        # print(i)
        if (i >= 87):
            print(i)
            print(p.summary())
            if UDP in p:
                if (not is_part_of_flow(p, prev, UDP) and not is_b_to_a(p, prev, UDP)):
                    udp_flows += 1
            elif TCP in p:
                if (not is_part_of_flow(p, prev, TCP) and not is_b_to_a(p, prev, TCP)):
                    tcp_flows += 1

        prev = p
        if (i >= 124):
            print(tcp_flows, udp_flows)
            quit(1)



    print(tcp_flows, udp_flows)