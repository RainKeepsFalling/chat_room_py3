#Python program to implement server side of chat room. 
import socket 
import select 
import sys 
from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

if len(sys.argv) != 3: 
    print ("Correct usage: script, IP address, port number")
    exit() 
  
IP_address = str(sys.argv[1]) 
  
Port = int(sys.argv[2]) 
  
server.bind((IP_address, Port)) 
  
server.listen(100) 
  
list_of_clients = [] 
  
def clientthread(conn, addr): 
  
    #send welcome message to the newly connected member in the chat room
    conn.send("Welcome to this chatroom!".encode()) 
  
    while True: 
            try: 
                message = conn.recv(2048) 
                if message: 
                    print("<" + addr[0] + "> " + message.decode())
  
                    # Calls broadcast function to send message to all defined later
                    message_to_send = "<" + addr[0] + "> " + message.decode()
                    broadcast(message_to_send, conn) 
  
                else: 
                    remove(conn)
  
            except: 
                continue
  
def broadcast(message, connection): 
    for clients in list_of_clients: 
        if clients!=connection: 
            try: 
                clients.send(message.encode()) 
            except: 
                clients.close() 
                # if the link is broken, we remove the client 
                remove(clients) 
  
#Removes the object from the list that was created at the beginning of the program
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection)
        print("<"+connection.getsockname()[0]+"> disconnected")
        broadcast("<"+connection.getpeername()[0]+"> disconnected", list_of_clients)

while True: 
  
    """Accepts a connection request and stores two parameters,  
    conn which is a socket object for that user, and addr  
    which contains the IP address of the client that just  
    connected"""
    conn, addr = server.accept() 
  
    #Maintains a list of clients for ease of broadcasting a message to all available people in the chatroom
    list_of_clients.append(conn) 
  
    # prints the address of the user that just connected 
    print(addr[0] + " connected")
    broadcast(addr[0]+" connected", list_of_clients)    
    # creates and individual thread for every user that connects 
    start_new_thread(clientthread,(conn,addr))
  
conn.close() 
server.close()