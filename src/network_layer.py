class NetworkLayer:
    def __init__(self, data_link_layer, ip_address, routing_table=None):
        self.data_link_layer = data_link_layer
        self.ip_address = ip_address
        self.routing_table = routing_table if routing_table is not None else {}

    def create_packet(self, dest_ip, payload: bytes) -> bytes:
        header_str = f"{dest_ip}||{self.ip_address}||{len(payload)}||"
        header_bytes = header_str.encode('utf-8')
        packet = header_bytes + payload
        return packet

    def send(self, dest_ip, payload: bytes):
        packet = self.create_packet(dest_ip, payload)
        # Lookup the destination MAC address using the routing table.
        if dest_ip not in self.routing_table:
            print("NetworkLayer: Destination IP not found in routing table.")
            return
        dest_mac = self.routing_table[dest_ip]
        self.data_link_layer.send(dest_mac, packet)
        print(f"NetworkLayer: Packet sent to {dest_ip}.")

    def receive(self) -> bytes:
        packet = self.data_link_layer.receive()
        if packet is None:
            return None
        
        try:
            decoded_packet = packet.decode('utf-8')
            # Split the header and payload. We use a maximum of 3 splits.
            parts = decoded_packet.split("||", 3)
            if len(parts) < 4:
                print("NetworkLayer: Incomplete packet header.")
                return None

            dest_ip, src_ip, length_str, payload_str = parts
            if dest_ip != self.ip_address:
                print("NetworkLayer: Packet not addressed to this IP. Dropping packet.")
                return None

            payload = payload_str.encode('utf-8')
            if len(payload) != int(length_str):
                print("NetworkLayer: Warning - payload length mismatch.")
            print(f"NetworkLayer: Packet received from {src_ip}.")
            return payload
        except Exception as e:
            print("NetworkLayer: Error parsing packet:", e)
            return None
