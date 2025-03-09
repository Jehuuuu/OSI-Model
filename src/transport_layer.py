import struct
import json
from typing import Optional

class Segment:
    def __init__(self, seq_num: int, ack_num: int, flags: int, payload: bytes):
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.flags = flags  # SYN=1, ACK=2, FIN=4
        self.payload = payload
        self.checksum = sum(payload) % 256

    def to_bytes(self) -> bytes:
        header = struct.pack("!IIBI", 
            self.seq_num, 
            self.ack_num,
            self.flags,
            self.checksum
        )
        return header + self.payload

    @staticmethod
    def from_bytes(data: bytes) -> Optional['Segment']:
        try:
            header = data[:13]  # 4 + 4 + 1 + 4 bytes
            seq_num, ack_num, flags, checksum = struct.unpack("!IIBI", header)
            payload = data[13:]
            seg = Segment(seq_num, ack_num, flags, payload)
            if seg.checksum != checksum:
                print("[Transport] Checksum failed")
                return None
            return seg
        except Exception as e:
            print(f"[Transport] Error: {e}")
            return None

class TransportLayer:
    def __init__(self, network_layer):
        self.network_layer = network_layer
        self.seq_num = 0
        self.expected_seq = 0
        self.window_size = 1

    def send(self, dest_ip, payload: bytes):
        segment = Segment(
            seq_num=self.seq_num,
            ack_num=self.expected_seq,
            flags=0,
            payload=payload
        )
        
        print(f"[Transport] Segment Data (SEQ {segment.seq_num}): {len(payload)} bytes")
        self.network_layer.send(dest_ip, segment.to_bytes())
        self.seq_num += 1

    def receive(self) -> Optional[bytes]:
        data = self.network_layer.receive()
        if not data:
            return None

        segment = Segment.from_bytes(data)
        if not segment:
            return None

        if segment.seq_num != self.expected_seq and segment.flags == 0:  # Ignore for handshake
            print(f"[Transport] Out of order segment: expected {self.expected_seq}, got {segment.seq_num}")
            return None

        print(f"[Transport] Received Segment (SEQ {segment.seq_num}): {len(segment.payload)} bytes")
        self.expected_seq = segment.seq_num + 1
        return segment.payload
