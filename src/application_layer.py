class ApplicationLayer:
    def __init__(self, presentation_layer):
        self.presentation_layer = presentation_layer

    def send_request(self, dest_ip, request: str):
        self.presentation_layer.send(dest_ip, request.encode('utf-8'))
        print("ApplicationLayer: Request sent.")

    def receive_request(self) -> str:
        data = self.presentation_layer.receive()
        if data:
            request_str = data.decode('utf-8')
            print("ApplicationLayer: Request received:", request_str)
            return request_str
        return None

    def send_response(self, dest_ip, response: str):
        self.presentation_layer.send(dest_ip, response.encode('utf-8'))
        print("ApplicationLayer: Response sent.")

    def receive_response(self) -> str:
        data = self.presentation_layer.receive()
        if data:
            response_str = data.decode('utf-8')
            print("ApplicationLayer: Response received:", response_str)
            return response_str
        return None
