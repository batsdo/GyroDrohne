from pythonosc import dispatcher
from pythonosc import osc_server

def default_handler(address, *args):
    print(f"Received message: {address} - {args}")

if __name__ == "__main__":
    # Dispatcher to handle incoming OSC messages
    dispatcher = dispatcher.Dispatcher()
    dispatcher.set_default_handler(default_handler)

    # Define the IP address and port for the OSC server
    ip = "0.0.0.0"  # Listen on all available interfaces
    port = 50000

    # Create and start the OSC server
    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    print(f"Serving on {server.server_address}")

    # Run the server. This will keep the program running and listening for incoming messages.
    server.serve_forever()
