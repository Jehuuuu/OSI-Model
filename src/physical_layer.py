import socket

class PhysicalLayer:
    def __init__(self, host='localhost', port=8000, is_server=False):
        self.host = host
        self.port = port
        self.is_server = is_server
        
        if self.is_server:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.host, self.port))
            self.sock.listen(1)
            print(f"[Server] Listening on {self.host}:{self.port}")
            self.conn, self.addr = self.sock.accept()
            print(f"[Server] Connection established with {self.addr}")
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            print(f"[Client] Connected to {self.host}:{self.port}")

    def send(self, data: bytes):
        # Convert each byte to its 8-bit binary representation
        bit_str = ''.join(format(byte, '08b') for byte in data)
        # Send the bit string encoded as UTF-8
        if self.is_server:
            self.conn.send(bit_str.encode('utf-8'))
        else:
            self.sock.send(bit_str.encode('utf-8'))
        print(f"Sent data as bit string: {bit_str}")

    def receive(self, bufsize=1024) -> bytes:
        if self.is_server:
            bit_str = self.conn.recv(bufsize).decode('utf-8')
        else:
            bit_str = self.sock.recv(bufsize).decode('utf-8')
        
        # Convert the bit string back to bytes
        byte_array = bytearray()
        for i in range(0, len(bit_str), 8):
            byte = bit_str[i:i+8]
            if len(byte) < 8:
                break  # Incomplete byte at the end
            byte_array.append(int(byte, 2))
        received_bytes = bytes(byte_array)
        print(f"Received bit string: {bit_str}")
        print(f"Converted to bytes: {received_bytes}")
        return received_bytes

    def close(self):
        if self.is_server:
            self.conn.close()
            self.sock.close()
        else:
            self.sock.close()
        print("Connection closed.")

