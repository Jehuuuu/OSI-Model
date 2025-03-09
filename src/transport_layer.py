class TransportLayer:
    def __init__(self, network_layer):
        self.network_layer = network_layer
        self.seq_num = 0

    def create_segment(self, payload: bytes) -> bytes:
        length = len(payload)
        checksum = sum(payload) % 256  # simple checksum computation
        header_str = f"{self.seq_num}||{length}||{checksum}||"
        header_bytes = header_str.encode('utf-8')
        segment = header_bytes + payload
        return segment

    def send(self, dest_ip, payload: bytes):
        segment = self.create_segment(payload)
        print(f"TransportLayer: Sending segment with sequence number {self.seq_num}")
        self.network_layer.send(dest_ip, segment)
        # Increase the sequence number for the next segment
        self.seq_num += 1

    def receive(self) -> bytes:
        segment = self.network_layer.receive()
        if segment is None:
            return None

        try:
            decoded_segment = segment.decode('utf-8')
            # Split header and payload: expecting 4 parts with the last part being the payload.
            parts = decoded_segment.split("||", 3)
            if len(parts) < 4:
                print("TransportLayer: Incomplete segment header.")
                return None

            seq_str, length_str, checksum_str, payload_str = parts
            seq_num = int(seq_str)
            length = int(length_str)
            expected_checksum = int(checksum_str)
            payload = payload_str.encode('utf-8')

            # Verify payload length
            if len(payload) != length:
                print("TransportLayer: Payload length mismatch.")
                return None

            # Verify checksum
            computed_checksum = sum(payload) % 256
            if computed_checksum != expected_checksum:
                print("TransportLayer: Checksum mismatch. Segment corrupted.")
                return None

            print(f"TransportLayer: Received segment with sequence number {seq_num}")
            return payload
        except Exception as e:
            print("TransportLayer: Error parsing segment:", e)
            return None
