import json

class ApplicationLayer:
    def __init__(self, presentation_layer):
        self.presentation_layer = presentation_layer

    def send_request(self, dest_ip, message: str):
        print("[Application] Sending Request: b\"" + message + "\"")
        self.presentation_layer.send(dest_ip, message.encode('utf-8'))

    def receive_request(self) -> str:
        data = self.presentation_layer.receive()
        if data:
            request = data.decode('utf-8')
            print("[Application] Received Request: b\"" + request + "\"")
            return request
        return None

    def send_response(self, dest_ip, message: str):
        print("[Application] Sending Response: b\"" + message + "\"")
        self.presentation_layer.send(dest_ip, message.encode('utf-8'))

    def receive_response(self) -> str:
        data = self.presentation_layer.receive()
        if data:
            response = data.decode('utf-8')
            print("[Application] Received Response: b\"" + response + "\"")
            return response
        return None
