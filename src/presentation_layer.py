import zlib
import base64

class PresentationLayer:
    def __init__(self, session_layer, encryption_key=b'secret'):
        self.session_layer = session_layer
        self.encryption_key = encryption_key

    def xor_encrypt(self, data: bytes) -> bytes:
        key = self.encryption_key
        encrypted = bytearray()
        for i, byte in enumerate(data):
            encrypted.append(byte ^ key[i % len(key)])
        return bytes(encrypted)

    def prepare_data(self, data: bytes) -> bytes:
        compressed = zlib.compress(data)
        encrypted = self.xor_encrypt(compressed)
        encoded = base64.b64encode(encrypted)
        print(f"[Presentation] Encoded Data: b\"{encoded.decode('utf-8')[:30]}...\"")
        return encoded

    def retrieve_data(self, data: bytes) -> bytes:
        try:
            print(f"[Presentation] Decoded Data: b\"{data.decode('utf-8')[:30]}...\"")
            decrypted = self.xor_encrypt(base64.b64decode(data))
            decompressed = zlib.decompress(decrypted)
            return decompressed
        except Exception as e:
            print(f"[Presentation] Error: {e}")
            return None

    def send(self, dest_ip, data: bytes):
        prepared_data = self.prepare_data(data)
        self.session_layer.send_data(dest_ip, prepared_data)

    def receive(self) -> bytes:
        data = self.session_layer.receive_data()
        if data is None:
            return None
        return self.retrieve_data(data)
