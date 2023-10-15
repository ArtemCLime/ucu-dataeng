import socket

class ReplicationHandler:
    def __init__(self, servers, host, port):
        self.servers = servers
        self.host = host
        self.port = port
    
    def replicate(self, message):
        for server in self.servers:
            try:
                # establish connection to server
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.connect((server['host'], server['port']))
                
                # send message to server
                conn.sendall(message.encode())
                
                # close connection
                conn.close()
            except:
                print(f"Failed to replicate message to {server['host']}:{server['port']}")
    
    def receive(self):
        try:
            # create socket and bind to host and port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((self.host, self.port))
            
            # listen for incoming connections
            sock.listen(1)
            print(f"Listening for incoming connections on {self.host}:{self.port}")
            
            # accept incoming connection
            conn, addr = sock.accept()
            print(f"Received connection from {addr[0]}:{addr[1]}")
            
            # receive message
            data = conn.recv(1024)
            message = data.decode()
            print(f"Received message: {message}")
            
            # close connection
            conn.close()
        except:
            print("Failed to receive message")
