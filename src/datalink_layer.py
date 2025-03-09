import struct

class DataLinkLayer:
    def __init__(self, physical_layer, mac_address):
        self.physical_layer = physical_layer
        self.mac_address = mac_address

    def create_frame(self, dest_mac, payload: bytes) -> bytes:
        # Create a frame with MAC addresses and payload
        header = f"MAC_HEADER:{self.mac_address}:{dest_mac}:".encode('utf-8')
        frame = header + payload
        return frame

    def send(self, dest_mac, payload: bytes):
        frame = self.create_frame(dest_mac, payload)
        print(f"[Data Link] Frame: {self.mac_address} -> {dest_mac} ({len(payload)} bytes)")
        self.physical_layer.send(frame)

    def receive(self) -> bytes:
        frame = self.physical_layer.receive()
        if not frame:
            return None
            
        try:
            # Extract MAC header information
            header_end = frame.find(b':', frame.find(b':', frame.find(b':') + 1) + 1) + 1
            header = frame[:header_end]
            payload = frame[header_end:]
            
            # Extract source and destination MAC
            header_str = header.decode('utf-8')
            src_mac = header_str.split(':')[1]
            dest_mac = header_str.split(':')[2]
            
            print(f"[Data Link] Frame: {src_mac} -> {dest_mac} ({len(payload)} bytes)")
            return payload
            
        except Exception as e:
            print(f"[Data Link] Error: {e}")
            return None
