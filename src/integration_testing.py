import threading
import time
from physical_layer import PhysicalLayer
from datalink_layer import DataLinkLayer
from network_layer import NetworkLayer
from transport_layer import TransportLayer
from session_layer import SessionLayer
from presentation_layer import PresentationLayer
from application_layer import ApplicationLayer

def server():
    # Initialize server silently
    server_physical = PhysicalLayer(is_server=True)
    server_data_link = DataLinkLayer(server_physical, mac_address="AA:BB:CC:DD:EE:FF")
    server_network = NetworkLayer(server_data_link, ip_address="192.168.1.1",
                              routing_table={"192.168.1.2": "AA:BB:CC:DD:EE:FF"})
    server_transport = TransportLayer(server_network)
    server_session = SessionLayer(server_transport, role="server", peer_ip="192.168.1.2")
    server_presentation = PresentationLayer(server_session, encryption_key=b'secret')
    server_application = ApplicationLayer(server_presentation)
    
    # Process client request
    if server_session.accept_session():
        request = server_application.receive_request()
        # Extract the actual message content from the request format
        if "HTTP_REQUEST:b'" in request and request.endswith("'"):
            message_content = request.split("'", 1)[1].rsplit("'", 1)[0]
        else:
            message_content = request
            
        response = f"HTTP_RESPONSE:OK '{message_content}'"
        server_application.send_response("192.168.1.2", response)
    server_physical.close()

def client():
    time.sleep(1)  # Wait for server
    
    # Setup client 
    client_physical = PhysicalLayer(is_server=False)
    client_data_link = DataLinkLayer(client_physical, mac_address="AA:BB:CC:DD:EE:FF")
    client_network = NetworkLayer(client_data_link, ip_address="192.168.1.2",
                              routing_table={"192.168.1.1": "AA:BB:CC:DD:EE:FF"})
    client_transport = TransportLayer(client_network)
    client_session = SessionLayer(client_transport, role="client")
    client_presentation = PresentationLayer(client_session, encryption_key=b'secret')
    client_application = ApplicationLayer(client_presentation)
    
    # Establish session and send data
    if client_session.start_session("192.168.1.1"):
        message = input("\nEnter message to send: ")
        
        print("\n--- SENDING DATA ---\n")
        client_application.send_request("192.168.1.1", f"HTTP_REQUEST:b'{message}'")
        
        print("\n--- RECEIVING DATA ---\n")
        response = client_application.receive_response()
        print(f"\nReceived Message: {response}")
    client_physical.close()

if __name__ == "__main__":
    print("\nOSI Model Simulation - Data Flow Demonstration")
    print("Server starting... ", end="")
    server_thread = threading.Thread(target=server)
    client_thread = threading.Thread(target=client)
    
    server_thread.start()
    time.sleep(0.5)
    print("ready!")
    
    client_thread.start()
    
    server_thread.join()
    client_thread.join()
