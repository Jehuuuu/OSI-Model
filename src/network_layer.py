import struct

class NetworkLayer:
    def __init__(self, data_link_layer, ip_address, routing_table=None):
        self.data_link_layer = data_link_layer
        self.ip_address = ip_address
        self.routing_table = routing_table if routing_table is not None else {}

    def create_packet(self, dest_ip, payload: bytes) -> bytes:
        header = f"IP_HEADER:{dest_ip}->{self.ip_address}:".encode('utf-8')
        packet = header + payload
        return packet

    def send(self, dest_ip, payload: bytes):
        if dest_ip not in self.routing_table:
            print(f"[Network] Error: No route to {dest_ip}")
            return
            
        dest_mac = self.routing_table[dest_ip]
        packet = self.create_packet(dest_ip, payload)
        
        print(f"[Network] Packet: {self.ip_address} -> {dest_ip} ({len(payload)} bytes)")
        self.data_link_layer.send(dest_mac, packet)

    def receive(self) -> bytes:
        packet = self.data_link_layer.receive()
        if not packet:
            return None
            
        try:
            # Extract IP header information
            header_end = packet.find(b':', packet.find(b'>') + 1) + 1
            header = packet[:header_end]
            payload = packet[header_end:]
            
            # Extract source and destination IP
            header_str = header.decode('utf-8')
            src_ip = header_str.split('->')[0].split(':')[1]
            dest_ip = header_str.split('->')[1].split(':')[0]
            
            print(f"[Network] Packet: {src_ip} -> {dest_ip} ({len(payload)} bytes)")
            return payload
        except Exception as e:
            print(f"[Network] Error: {e}")
            return None
