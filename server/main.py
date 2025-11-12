import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print(f"Received data from {self.client_address[0]}: {self.data.decode()}")
        self.request.sendall(self.data.upper()) 



if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8225

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print(f"Server started at {HOST}:{PORT}")
        server.serve_forever()