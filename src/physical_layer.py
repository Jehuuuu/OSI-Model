import socket
import struct
import binascii

class PhysicalLayer:
    def __init__(self, host='localhost', port=8000, is_server=False):
        self.host = host
        self.port = port
        self.is_server = is_server
        
        if self.is_server:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.host, self.port))
            self.sock.listen(1)
            self.conn, self.addr = self.sock.accept()
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))

    def send(self, data: bytes):
        try:
            # Get hex representation of first few bytes
            sample_size = min(8, len(data))
            hex_sample = binascii.hexlify(data[:sample_size]).decode('utf-8')
            print(f"[Physical] Transmitting: {len(data)} bytes (starts with {hex_sample}...)")
            
            # Send length first
            length = len(data)
            length_bytes = struct.pack("!I", length)
            
            if self.is_server:
                self.conn.sendall(length_bytes)
                self.conn.sendall(data)
            else:
                self.sock.sendall(length_bytes)
                self.sock.sendall(data)
            
        except Exception as e:
            print(f"[Physical] Error: {e}")

    def receive(self) -> bytes:
        try:
            if self.is_server:
                length_bytes = self.conn.recv(4)
                if not length_bytes:
                    return None
                length = struct.unpack("!I", length_bytes)[0]
                data = self.conn.recv(length)
            else:
                length_bytes = self.sock.recv(4)
                if not length_bytes:
                    return None
                length = struct.unpack("!I", length_bytes)[0]
                data = self.sock.recv(length)
            
            # Get hex representation of first few bytes
            sample_size = min(8, len(data))
            hex_sample = binascii.hexlify(data[:sample_size]).decode('utf-8')
            print(f"[Physical] Receiving: {len(data)} bytes (starts with {hex_sample}...)")
            
            return data
            
        except Exception as e:
            print(f"[Physical] Error: {e}")
            return None

    def close(self):
        if self.is_server:
            self.conn.close()
            self.sock.close()
        else:
            self.sock.close()

