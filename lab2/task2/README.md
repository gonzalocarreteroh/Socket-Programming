Task 1 consists of a dirctory with a python file called webserver.py, an html file called HelloWorld.html and another directory containing nested html files, in this case nested.html.

The webserver has a socket that receives connection requests from users using the TCP protocol. The webserver can handle GET and HEAD requests from the users requesting files inside the webserver directory or subdirectory.

To execute the program, run webserver.py and then make GET or HEAD request using Postman or a web browser. The port number associated with the webserver is 11000 and the IP address is 127.0.0.1. An example of a valid HTTP request could be http://127.0.0.1:11000/HelloWorld.html
To terminate the program click on the terminal running the code and press the keys ctrl + c in your keyboard.


This repository contains three Python files that together create a simple DNS resolver system using UDP sockets. The system consists of a server (server.py), a client (client.py), and a utility module (util.py) with functions for generating DNS headers, creating question and answer sections, and extracting domain information from DNS queries.

To execute the program, run client.py and server.py on separate terminals. The client will prompt the user for a domain name and a DNS server address. The client will then send a DNS query to the server, which will respond with a DNS response. The client will then print the response to the terminal.
