import random

def generate_dns_header(response=False, ancount=0):

    header = ""
    # ID: 16-bit random identifier
    header_id = random.randint(0, 0xFFFF)

    header += format(header_id, '016b')

    # QR (Query/Response): 1 bit, 0 for query, 1 for response
    qr = 0 if response else 1

    header += str(qr)

    # OPCODE: 4 bits (0 for standard query)
    opcode = 0

    header += format(opcode, '04b')

    # AA (Authoritative Answer): 1 bit, set to 1 for responses
    aa = 1 if response else 0

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

    return header_bytes

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
import struct

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

# Example usage:
if __name__ == "__main__":

    print(create_answer_section("uwaterloo.ca"))

    print(generate_dns_header(response=True, ancount=0))


    query_domain = "google.com"
    question_section = create_question_section(query_domain)
    print(question_section)

