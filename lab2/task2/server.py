import socket
import util

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the server socket to a specific address and port
server_address = ("127.0.0.1", 12001)
server_socket.bind(server_address)

def extract_domain(query):
    start_i = query.index("-")
    domain = ""
    start = start_i + 4
    for i in range(int(query[start_i + 1:start_i + 3], 16)):
        char = query[start:start + 2]
        print(char)
        domain += chr(int(char, 16))
        start += 3
    domain += "."
    start_2 = start + 3
    for i in range(int(query[start:start + 2], 16)):
        char = query[start_2:start_2 + 2]
        domain += chr(int(char, 16))
        start_2 += 3
    return domain

while True:
    # Wait for a DNS query from the client
    data, client_address = server_socket.recvfrom(1024)
    query = data.decode()

    domain = extract_domain(query)

    # Create a DNS response
    response_data = util.generate_dns_header(False, len(util.dns_records[domain][3:])) + "-" + util.create_question_section(domain) + "-" + util.create_answer_section(domain)

    server_socket.sendto(response_data.encode(), client_address)