import struct

class DataLinkLayer:
    def __init__(self, physical_layer, mac_address):
        self.physical_layer = physical_layer
        self.mac_address = mac_address

    def create_frame(self, dest_mac, payload: bytes) -> bytes:
        header_str = f"{dest_mac}||{self.mac_address}||{len(payload)}||"
        header_bytes = header_str.encode('utf-8')
        header_len = len(header_bytes)
        # Pack header length as a 4-byte integer (big-endian)
        header_len_bytes = struct.pack("!I", header_len)
        frame = header_len_bytes + header_bytes + payload
        return frame

    def send(self, dest_mac, payload: bytes):
        """
        Create a frame and send it using the Physical Layer.
        """
        frame = self.create_frame(dest_mac, payload)
        self.physical_layer.send(frame)
        print("DataLinkLayer: Frame sent.")

    def receive(self) -> bytes:
        # Receive the raw frame from the Physical Layer
        raw_frame = self.physical_layer.receive()
        if not raw_frame:
            return None

        # Read the first 4 bytes for header length
        if len(raw_frame) < 4:
            print("DataLinkLayer: Incomplete frame received.")
            return None
        header_len = struct.unpack("!I", raw_frame[:4])[0]
        # Ensure that the raw_frame has enough bytes for the header and payload
        if len(raw_frame) < 4 + header_len:
            print("DataLinkLayer: Frame too short for declared header length.")
            return None

        # Extract the header and decode it
        header_bytes = raw_frame[4:4 + header_len]
        try:
            header_str = header_bytes.decode('utf-8')
        except Exception as e:
            print("DataLinkLayer: Error decoding header:", e)
            return None

        # Parse header fields using the delimiter "||"
        parts = header_str.split("||")
        if len(parts) < 3:
            print("DataLinkLayer: Incomplete header information.")
            return None

        dest_mac, src_mac, payload_len_str = parts[:3]
        expected_payload_len = int(payload_len_str)

        # Extract payload (rest of the frame)
        payload = raw_frame[4 + header_len:]
        if len(payload) != expected_payload_len:
            print("DataLinkLayer: Warning - payload length mismatch.")
        print(f"DataLinkLayer: Frame received from {src_mac} with payload: {payload}")
        return payload
