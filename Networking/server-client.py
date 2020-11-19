import socket
import sys
import json

# Switch off if you don't want console print
VERBOSE = True

class Server:
    '''This class manages the Server interface 
    '''
    def __init__(self, host='', port=9090):
        '''Initialize class with host and port. 

        # Arguments:
            - host: the ip address of the server; default is ''
            - port: the ip port of the server; default is 9091.
        '''
        # Preparing the server using socket to listen
        self.host = host
        self.port = port

    def run(self):
        '''Run socket 
        '''
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))

    def listening(self):
        '''Listening for incoming connection 
        '''
        if VERBOSE:
            print(f"[+] Listening on port: {self.port}")

        # Server start listening
        self.s.listen(1)
        self.conn, self.addr = self.s.accept()

        if VERBOSE:
            print(f"[+] Establish connection with {self.addr}")

    def retrieve_data(self):
        ''' Retrieve data from client

        # Returns
            - data: the data retrieved from client
        '''
        try:
            # Retrieving data from client
            self.data = json.loads((self.conn.recv(1024)))
            if not self.data:
                print("[+] No data received")
                #self.close_connection()

            if VERBOSE:
                print(f"[+] Received data: {self.data}")

            return self.data

        except socket.error as e:
            print(f"[-] An error has occured: {e}\n\n")
            self.close_connection()

        
    def send_data(self, data=''):   
        ''' Send data back to the client. Default is send back ACK=1 when everything went good 0 otherwise

        # Arguments:
            - data: data to send back to client. Must be a dictionary
        ''' 
        try:         
            self.response = data
           
            # ACK=1 everything worked fine
            self.response['ACK'] = 1

            # Sending response back to client
            self.dataToSend = json.dumps(self.response).encode("utf-8")

            if VERBOSE:
                print(f"[+] Sending back: {self.dataToSend}\n\n")

            self.conn.sendall(self.dataToSend)

        except Exception as e:

            # ACK=0, an error has occurred; reset all the response variable
            self.response['ACK'] = 0

            # Sending ACK back to client
            self.dataToSend = json.dumps(self.response).encode("utf-8")

            print(f"[+] Sending back: {self.dataToSend}")
            self.conn.sendall(self.dataToSend)
            print(f"[-] An error as occured: {e}\n\n")


    def close_connection(self):
        ''' Close connection
        '''
        if VERBOSE:
            print("[+] Closing connection ...")

        self.conn.close()


class Client:
    '''This class manages the Client interface 
    '''
    def __init__(self, host='127.0.0.1', port=9090):
        '''Initialize class with host and port. 

        # Arguments:
            - host: the ip address of the server we want to reach ; default is localhost
            - port: the ip port of the server we want to reach; default is 9091. Must be equal to Server
        '''
        # Preparing the server using socket to listen
        self.host = host
        self.port = port

    def run(self, data=''):
        '''Create socket 

        # Arguments:
            - data: data you want to send through the socket

        # Returns:
            - received: server response
        '''
        try:
            # Encode data and send as JSON
            self.dataToSend = json.dumps(data).encode("utf-8")

            # Create a socket (SOCK_STREAM means a TCP socket)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

            # Connect to server and send data
            if VERBOSE:
                print(f"[+] Connecting to server\n\tHOST: {self.host}\n\tPORT: {self.port}")
            self.sock.connect((self.host,self.port))

            # Send data
            if VERBOSE:
                print("[+] Sending data ...")
            self.sock.sendall(self.dataToSend)
            if VERBOSE:
                print(f"[+] Sent: {self.dataToSend}")

            # Receive data from the server
            self.received = json.loads((self.sock.recv(1024)))
            
            if VERBOSE:
                print(f"[-] Received: {self.received}\n")

            return self.received    

        except Exception as e:
            print(f"[-] An error has occurred: {e}")
            self.close_connection()

    def close_connection(self):
        ''' Close connection
        '''
        if VERBOSE:
            print("[+] Closing connection ...")

        self.sock.close()

if __name__ == "__main__":

    # Server Example
    server = Server()
    server.run()

    while True:
        server.listening()
        server.retrieve_data()
        data = {}
        data['msg'] = 'test_back'
        server.send_data(data)

    # Client Example
    # client = Client()

    # while True:
    #     data = 'test'
    #     client.run(data)