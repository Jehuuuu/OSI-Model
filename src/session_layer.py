class SessionLayer:
    def __init__(self, transport_layer, role="client", peer_ip=None):
        self.transport_layer = transport_layer
        self.role = role
        self.session_established = False
        self.session_id = None
        self.peer_ip = peer_ip

    def start_session(self, dest_ip):
        self.session_id = "SESSION1234"  # In practice, generate a unique session id.
        syn_message = f"SYN::{self.session_id}"
        print("SessionLayer (Client): Sending SYN...")
        self.transport_layer.send(dest_ip, syn_message.encode('utf-8'))
        
        response = self.transport_layer.receive()
        if response is None:
            print("SessionLayer (Client): No response received.")
            return False
        
        response_str = response.decode('utf-8')
        if response_str.startswith("SYN-ACK::"):
            parts = response_str.split("::")
            if len(parts) == 2 and parts[1] == self.session_id:
                ack_message = f"ACK::{self.session_id}"
                print("SessionLayer (Client): Sending ACK...")
                self.transport_layer.send(dest_ip, ack_message.encode('utf-8'))
                self.session_established = True
                print("SessionLayer (Client): Session established.")
                return True
        
        print("SessionLayer (Client): Session handshake failed.")
        return False

    def accept_session(self):
        print("SessionLayer (Server): Waiting for SYN...")
        message = self.transport_layer.receive()
        if message is None:
            print("SessionLayer (Server): No message received.")
            return False
        
        message_str = message.decode('utf-8')
        if message_str.startswith("SYN::"):
            parts = message_str.split("::")
            if len(parts) == 2:
                self.session_id = parts[1]
                syn_ack_message = f"SYN-ACK::{self.session_id}"
                if self.peer_ip is None:
                    print("SessionLayer (Server): peer_ip not set. Cannot send SYN-ACK.")
                    return False
                print("SessionLayer (Server): Sending SYN-ACK...")
                self.transport_layer.send(self.peer_ip, syn_ack_message.encode('utf-8'))
                print("SessionLayer (Server): Waiting for ACK...")
                ack_response = self.transport_layer.receive()
                if ack_response is None:
                    print("SessionLayer (Server): No ACK received.")
                    return False
                ack_str = ack_response.decode('utf-8')
                if ack_str.startswith("ACK::") and ack_str.split("::")[1] == self.session_id:
                    self.session_established = True
                    print("SessionLayer (Server): Session established.")
                    return True
        print("SessionLayer (Server): Session handshake failed.")
        return False

    def send_data(self, dest_ip, data: bytes):
        if not self.session_established:
            print("SessionLayer: Session not established. Cannot send data.")
            return
        self.transport_layer.send(dest_ip, data)

    def receive_data(self) -> bytes:
        if not self.session_established:
            print("SessionLayer: Session not established. Cannot receive data.")
            return None
        return self.transport_layer.receive()
