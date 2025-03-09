import json

class SessionLayer:
    def __init__(self, transport_layer, role="client", peer_ip=None):
        self.transport_layer = transport_layer
        self.role = role
        self.session_established = False
        self.session_id = "open"
        self.peer_ip = peer_ip

    def start_session(self, dest_ip):
        # Send SYN
        syn = {"type": "SYN", "session_id": self.session_id}
        self.transport_layer.send(dest_ip, json.dumps(syn).encode('utf-8'))
        
        # Receive SYN-ACK
        syn_ack = self.transport_layer.receive()
        if syn_ack is None:
            return False
            
        try:
            syn_ack_data = json.loads(syn_ack.decode('utf-8'))
            if syn_ack_data.get("type") == "SYN-ACK":
                # Send ACK
                ack = {"type": "ACK", "session_id": self.session_id}
                self.transport_layer.send(dest_ip, json.dumps(ack).encode('utf-8'))
                self.session_established = True
                return True
        except:
            pass
        return False

    def accept_session(self):
        # Wait for SYN
        syn = self.transport_layer.receive()
        if syn is None:
            return False
            
        try:
            syn_data = json.loads(syn.decode('utf-8'))
            if syn_data.get("type") == "SYN":
                self.session_id = syn_data.get("session_id", "open")
                
                # Send SYN-ACK
                syn_ack = {"type": "SYN-ACK", "session_id": self.session_id}
                self.transport_layer.send(self.peer_ip, json.dumps(syn_ack).encode('utf-8'))
                
                # Wait for ACK
                ack = self.transport_layer.receive()
                if ack:
                    ack_data = json.loads(ack.decode('utf-8'))
                    if ack_data.get("type") == "ACK":
                        self.session_established = True
                        return True
        except:
            pass
        return False

    def send_data(self, dest_ip, payload: bytes):
        if not self.session_established:
            print("[Session] Error: No active session")
            return
            
        session_data = {
            "session": self.session_id,
            "data": payload.decode('utf-8', errors='replace')
        }
        session_json = json.dumps(session_data)
        
        print(f"[Session] Session Data: b'{session_json[:30]}...'")
        self.transport_layer.send(dest_ip, session_json.encode('utf-8'))

    def receive_data(self) -> bytes:
        if not self.session_established:
            print("[Session] Error: No active session")
            return None
            
        data = self.transport_layer.receive()
        if data:
            session_data = json.loads(data.decode('utf-8'))
            print(f"[Session] Session Data: b'{data.decode('utf-8')[:30]}...'")
            return session_data.get("data", "").encode('utf-8')
        return None
