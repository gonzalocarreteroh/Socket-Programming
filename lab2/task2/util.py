import random

def generate_dns_header(response=False, ancount=0, query_id=0):

    header = ""
    # ID: 16-bit random identifier
    header_id = random.randint(0, 0xFFFF)
    if response:
        header_id = query_id

    header += format(header_id, '016b')

    # QR (Query/Response): 1 bit, 0 for query, 1 for response
    qr = 1 if response else 0

    header += str(qr)

    # OPCODE: 4 bits (0 for standard query)
    opcode = 0

    header += format(opcode, '04b')

    # AA (Authoritative Answer)
    aa = 1

    header += str(aa)

    # TC (TrunCation): 1 bit, set to 0 for this lab
    tc = 0

    header += str(tc)

    # RD (Recursion Desired): 1 bit, set to 0 for this lab
    rd = 0

    header += str(rd)

    # RA (Recursion Available): 1 bit, set to 0 for this lab
    ra = 0

    header += str(ra)

    # Z: 3 bits, set to 0
    z = 0

    header += format(z, '03b')

    # RCODE (Response Code): 4 bits, set to 0
    rcode = 0

    header += format(rcode, '04b')

    # QDCOUNT: 16-bit, number of entries in the question section (always 1 for this lab)
    qdcount = 1

    header += format(qdcount, '016b')

    # ANCOUNT: 16-bit, number of resource records in the answer section
    # Set based on the provided argument
    ancount = ancount

    header += format(ancount, '016b')

    # NSCOUNT: 16-bit, number of name server resource records in the authority records section (always 0 for this lab)
    nscount = 0

    header += format(nscount, '016b')

    # ARCOUNT: 16-bit, number of resource records in the additional records section (always 0 for this lab)
    arcount = 0

    header += format(arcount, '016b')

    header = hex(int(header,2))

    header_bytes = ""
    count = 0
    for hexx in str(header[2:]):
        header_bytes += hexx
        count += 1
        if count == 2:
            header_bytes += " "
            count = 0

    return header_bytes[:-1]

def create_question_section(query_domain):
    qname = ""
    for part in query_domain.split("."):
        qname += format(len(part), "02x")
        qname += " "
        for char in part:
            qname += format(ord(char), "02x")
            qname += " "

    qname += format(0, "02x")

    qtype = format(1, "04x")  # TYPE A
    qtype = qtype[:2] + " " + qtype[2:]

    qclass = format(1, "04x")  # CLASS IN (Internet)
    qclass = qclass[:2] + " " + qclass[2:]

    return qname + " " + qtype + " " + qclass


import socket

def create_answer_section(domain_name):
    answer = ""

    if domain_name in dns_records:
        for ip in dns_records[domain_name][3:]:
            name = "C00C"  # Pointer to domain name in Question section
            answer += format(int(name, 16), "04x")
            rtype = 1  # TYPE A
            answer += format(rtype, "04x")
            rclass = 1 # CLASS IN
            answer += format(rclass, "04x")
            ttl = dns_records[domain_name][2]  # TTL for this example
            answer += format(ttl, "08x")
            rdlength = 4  # Length of RDATA (4 bytes)
            answer += format(rdlength, "04x")
            rdata = socket.inet_aton(ip)
            if (len(rdata.hex()) % 2 != 0):
                rdata = rdata.hex() + "0"
            answer += rdata.hex()

        final_answer = ""
        count = 0
        for hex in answer:
            final_answer += hex
            count += 1
            if count == 2:
                final_answer += " "
                count = 0

        return final_answer
    else:
        return answer  # Empty answer section for non-existent domains

dns_records = {
    "google.com": ["A", "IN", 260, "192.165.1.1", "192.165.1.10"],
    "youtube.com": ["A", "IN", 160, "192.165.1.2"],
    "uwaterloo.ca": ["A", "IN", 160, "192.165.1.3"],
    "wikipedia.org": ["A", "IN", 160, "192.165.1.4"],
    "amazon.ca": ["A", "IN", 160, "192.165.1.5"],
}


def extract_answer_section(query):

    l = []

    ind = query.index("Answer ")
    query = query[ind + 7:]

    octet_pair = list(query.split(" "))

    i = 0
    while i < len(octet_pair)-1:

        ans = {}

        ans["name"] = octet_pair[i] + octet_pair[i+1]

        ans["type"] = octet_pair[i+2] + octet_pair[i+3]

        if int(ans["type"], 16) == 1:
            ans["type"] = "A"

        ans["class"] = octet_pair[i+4] + octet_pair[i+5]

        if int(ans["class"], 16) == 1:
            ans["class"] = "IN"

        ans["ttl"] = octet_pair[i+6] + octet_pair[i+7] + octet_pair[i+8] + octet_pair[i+9]

        ans["ttl"] = int(ans["ttl"], 16)

        ans["rdlength"] = octet_pair[i+10] + octet_pair[i+11]

        ans["rdlength"] = int(ans["rdlength"], 16)

        #print(i+13)
        ans["rdata"] = [octet_pair[i+12], octet_pair[i+13], octet_pair[i+14], octet_pair[i+15]]

        for j in range(len(ans["rdata"])):
            ans["rdata"][j] = str(int(ans["rdata"][j], 16))

        ans["rdata"] = ".".join(ans["rdata"])
        i += 16

        l.append(ans)

    return l


def extract_domain(query):
    start_i = query.index("Question ")
    domain = ""
    start_i += 8
    start = start_i + 4
    for i in range(int(query[start_i + 1:start_i + 3], 16)):
        char = query[start:start + 2]
        domain += chr(int(char, 16))
        start += 3
    domain += "."
    start_2 = start + 3
    for i in range(int(query[start:start + 2], 16)):
        char = query[start_2:start_2 + 2]
        domain += chr(int(char, 16))
        start_2 += 3
    return domain

# Example usage:
if __name__ == "__main__":

    print(create_answer_section("uwaterloo.ca"))

    print(generate_dns_header(response=True, ancount=0))


    query_domain = "google.com"
    question_section = create_question_section(query_domain)
    print(question_section)

