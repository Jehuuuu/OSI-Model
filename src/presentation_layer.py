import zlib

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
        return encrypted

    def retrieve_data(self, data: bytes) -> bytes:
        decrypted = self.xor_encrypt(data)  # XOR decryption is the same as encryption.
        try:
            decompressed = zlib.decompress(decrypted)
        except zlib.error as e:
            print("PresentationLayer: Decompression failed:", e)
            return None
        return decompressed

    def send(self, dest_ip, data: bytes):
        prepared_data = self.prepare_data(data)
        self.session_layer.send_data(dest_ip, prepared_data)
        print("PresentationLayer: Data sent.")

    def receive(self) -> bytes:
        data = self.session_layer.receive_data()
        if data is None:
            return None
        original_data = self.retrieve_data(data)
        print("PresentationLayer: Data received.")
        return original_data
