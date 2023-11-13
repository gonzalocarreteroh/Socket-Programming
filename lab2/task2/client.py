import socket
import util

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server address and port
server_address = ("127.0.0.1", 12001)

while True:
    print("Input from the User:")
    domain_name = input("> Enter Domain Name: ")
    domain_name = domain_name.lower()

    if domain_name == "end":
        print("Session ended")
        client_socket.close()
        break

    query_message = "Header " + util.generate_dns_header(response=False, ancount=0) + "\nQuestion " + util.create_question_section(
        domain_name)
    # Send the DNS query to the server
    client_socket.sendto(query_message.encode(), server_address)

    # Receive the DNS response from the server
    response, _ = client_socket.recvfrom(2048)
    response = response.decode()
    if response == "Domain not found":
        print(response)
        continue
    print("Output:")
    response_object = util.extract_answer_section(response)

    for ans in response_object:
        print(
            domain_name + ": " + "type " + ans["type"] + ", class " + ans["class"] + ", ttl " + str(ans["ttl"]) + " (" +
            str(ans["rdlength"]) + ") " + ans["rdata"])
