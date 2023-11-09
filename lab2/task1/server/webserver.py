from socket import *
import time
import datetime
import os

def format_date(date):
    # Date format is Weekday, DD Month YYYY HH:MM:SS (Time Zone)
    # Get the weekday
    weekday = date.strftime("%a")
    # Get the day
    day = date.strftime("%d")
    # Get the month
    month = date.strftime("%b")
    # Get the year
    year = date.strftime("%Y")
    # Get the time
    cur_time = date.strftime("%H:%M:%S")
    # Get the time zone
    time_zone = time.tzname[0]
    # Get the date
    date = f"{weekday}, {day} {month} {year} {cur_time} {time_zone}"
    return date

def get_current_date():
    # Get the current date
    cur_date = datetime.datetime.now()
    # Return format of the current date
    return format_date(cur_date)

def get_modified_date(file_name):
    # Get the last modified date of the file
    # Get the last modified time
    last_modified_time = os.path.getmtime(file_name)
    # Convert the last modified time to datetime
    last_modified_time = datetime.datetime.fromtimestamp(last_modified_time)
    # Return format of the last modified time
    return format_date(last_modified_time)

def create_response(request_type, status_code, content_type, data, file_name):
    # Headers: Connection, Date, Server, Last-Modified, Content-Length and Content-Type
    response = f"HTTP/1.1 {status_code}\n"
    response += "Connection: keep-alive\n"
    # Get current date
    date = get_current_date()
    response += f"Date: {date}\n"
    response += "Server: Python/3.8\n"
    if status_code == "404 Not Found":
        # End header if status code is 404
        response += "\n"
    if status_code == "200 OK":
        response += f"Last-Modified: {get_modified_date(file_name[1:])}\n"
        response += f"Content-Length: {len(data)}\n"
        response += f"Content-Type: {content_type}\n\n"
    response = response.encode('utf-8') 
    # Only add the file data if the request type is GET and not HEAD
    if request_type == "GET" and status_code == "200 OK":
        response += data
    return response

def handle_request(client_socket):
    # Receive request from client
    request = client_socket.recv(1024)
    # Split the request from client
    request_split = request.decode().splitlines()
    # Get the request type, file name, http type from the first line
    request_type, file_name, http_type = request_split[0].split()

    # Open the file
    try:
        if file_name == "/":
            file_name = "/HelloWorld.html"
        file = open(file_name[1:], 'rb')
        data = file.read()
        file.close()
        response = create_response(request_type, "200 OK", "text/html", data, file_name)
        response = create_response(request_type, "200 OK", "text/html", data, file_name)
        client_socket.sendall(response)
    except FileNotFoundError:
        response = create_response(request_type, "404 Not Found", "text/html", b"<h1>404 Not Found</h1>", file_name)
        client_socket.sendall(response)


# Create a TCP socket
serverPort = 11000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("127.0.0.1", serverPort))
serverSocket.listen(1)
print ("The server is ready to receive")
while True:
    # http://127.0.0.1:11000/HelloWorld.html 
    connectionSocket, addr = serverSocket.accept()

    handle_request(connectionSocket)
    connectionSocket.close()
