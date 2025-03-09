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
    # Initialize server-side layers
    server_physical = PhysicalLayer(is_server=True)
    server_data_link = DataLinkLayer(server_physical, mac_address="AA:BB:CC:DD:EE:01")
    server_network = NetworkLayer(server_data_link, ip_address="192.168.1.1",
                                  routing_table={"192.168.1.2": "AA:BB:CC:DD:EE:02"})
    server_transport = TransportLayer(server_network)
    server_session = SessionLayer(server_transport, role="server", peer_ip="192.168.1.2")
    server_presentation = PresentationLayer(server_session, encryption_key=b'secret')
    server_application = ApplicationLayer(server_presentation)
    
    # Accept session handshake from the client
    if server_session.accept_session():
        # Receive the request from the client
        request = server_application.receive_request()
        print("Server received request:", request)
        # Send a response back to the client
        server_application.send_response("192.168.1.2", "HTTP/1.1 200 OK")
    
    server_physical.close()

def client():
    # Delay to ensure the server starts first
    time.sleep(1)
    # Initialize client-side layers
    client_physical = PhysicalLayer(is_server=False)
    client_data_link = DataLinkLayer(client_physical, mac_address="AA:BB:CC:DD:EE:02")
    client_network = NetworkLayer(client_data_link, ip_address="192.168.1.2",
                                  routing_table={"192.168.1.1": "AA:BB:CC:DD:EE:01"})
    client_transport = TransportLayer(client_network)
    client_session = SessionLayer(client_transport, role="client")
    client_presentation = PresentationLayer(client_session, encryption_key=b'secret')
    client_application = ApplicationLayer(client_presentation)
    
    # Start the handshake and send a request
    if client_session.start_session("192.168.1.1"):
        client_application.send_request("192.168.1.1", "GET /index.html")
        # Receive the response from the server
        response = client_application.receive_response()
        print("Client received response:", response)
    
    client_physical.close()

if __name__ == "__main__":
    # Create threads for the server and client
    server_thread = threading.Thread(target=server)
    client_thread = threading.Thread(target=client)
    
    # Start both threads
    server_thread.start()
    client_thread.start()
    
    # Wait for both threads to complete
    server_thread.join()
    client_thread.join()
