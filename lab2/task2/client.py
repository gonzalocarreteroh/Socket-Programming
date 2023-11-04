import socket
import util

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server address and port
server_address = ("127.0.0.1", 12001)

while True:
    domain_name = input("> Enter Domain Name: ")

    if domain_name == "end":
        print("Session ended")
        break

    query_message = util.generate_dns_header(True, 0) + "-" + util.create_question_section(domain_name)
    # Send the DNS query to the server
    client_socket.sendto(query_message.encode(), server_address)

    # Receive the DNS response from the server
    response, _ = client_socket.recvfrom(1024)
    response = response.decode()
    print("Output:")
    print(response)

