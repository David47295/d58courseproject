import csv

SYN_FLAG = 0b000000000010
RST_FLAG = 0b000000000100
FIN_FLAG = 0b000000000001
ACK_FLAG = 0b000000010000

def is_a_to_b(p1, p2):
    return (p1["ip.src"] == p2["ip.src"] and
           p1["ip.dst"] == p2["ip.dst"] and
            p1["tcp.srcport"] == p2["tcp.srcport"] and
            p1["tcp.dstport"] == p2["tcp.dstport"]
    )

def is_b_to_a(p1, p2):
    return (p1["ip.src"] == p2["ip.dst"] and
           p1["ip.dst"] == p2["ip.src"] and
            p1["tcp.srcport"] == p2["tcp.dstport"] and
            p1["tcp.dstport"] == p2["tcp.srcport"]
    )

def compute_final_state(tcpflows):
    tcp_output = open("tcp_states.csv", "w")
    tcp_writer = csv.writer(tcp_output, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    finished_count = 0
    request_count = 0
    reset_count = 0
    ongoing_count = 0

    for k, v in tcpflows.items():
        a_to_b_closed = False
        b_to_a_closed = False
        closing_ack = False
        for p in v:
            if int(p["tcp.flags"], 16) & (ACK_FLAG | FIN_FLAG) == (ACK_FLAG | FIN_FLAG):
                if is_a_to_b(p, v[0]):
                    a_to_b_closed = True
                elif is_b_to_a(p, v[0]):
                    b_to_a_closed = True

                if a_to_b_closed and b_to_a_closed:
                    if is_a_to_b(p, v[0]) and int(p["tcp.flags"], 16) & ACK_FLAG == ACK_FLAG:
                        closing_ack = True
        if a_to_b_closed and b_to_a_closed and closing_ack:
            finished_count += 1
        else:
            if len(v) == 1 and int(v[0]["tcp.flags"], 16) & SYN_FLAG == SYN_FLAG:
                # print(k)
                request_count += 1
            elif int(v[len(v) - 1]["tcp.flags"], 16) & RST_FLAG == RST_FLAG:
                # print(k, "          Reset")
                reset_count += 1
            elif int(v[len(v) - 1]["tcp.flags"], 16) & (RST_FLAG | FIN_FLAG) != FIN_FLAG or \
                int(v[len(v) - 1]["tcp.flags"], 16) & (RST_FLAG | FIN_FLAG) != RST_FLAG:
                ongoing_count += 1

    tcp_writer.writerow(["Finished", finished_count])
    tcp_writer.writerow(["Request", request_count])
    tcp_writer.writerow(["Ongoing", ongoing_count])
    tcp_writer.writerow(["Reset", reset_count])

    tcp_output.close()
