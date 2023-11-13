import socket
import util

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the server socket to a specific address and port
server_address = ("127.0.0.1", 12001)
server_socket.bind(server_address)

while True:
    # Wait for a DNS query from the client
    data, client_address = server_socket.recvfrom(2048)
    query = data.decode()

    domain = util.extract_domain(query)

    response_data = ""
    if domain in util.dns_records.keys():
        # Create a DNS response
        response_data = "Header " + util.generate_dns_header(response=True, ancount=len(
            util.dns_records[domain][3:]), query_id=int(query[7:9] + query[10:12], 16)) + "\nQuestion " + util.create_question_section(domain) + "\nAnswer " + util.create_answer_section(
            domain)
    else:
        response_data = "Domain not found"

    print("Request:")
    print(query)
    print("Response:")
    print(response_data)

    server_socket.sendto(response_data.encode(), client_address)
