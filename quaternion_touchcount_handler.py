from pythonosc import dispatcher
from pythonosc import osc_server

def quaternion_handler(address, *args):
    if len(args) >= 2:
        global first_value
        first_value = args[0]
        global second_value
        second_value = args[1]
        print(f"First value: {first_value}, Second value: {second_value}")
    else:
        print("Received quaternion message with insufficient arguments")

def touchcount_handler(address, *args):
    global touch_count
    if len(args) >= 1:
        touch_count = args[0]
        print(f"Touch count: {touch_count}")
    else:
        print("Received touch count message with insufficient arguments")


if __name__ == "__main__":
    # Dispatcher to handle incoming OSC messages
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/ZIGSIM/*/quaternion", quaternion_handler)
    dispatcher.map("/ZIGSIM/*/touchcount", touchcount_handler)

    # Define the IP address and port for the OSC server
    ip = "0.0.0.0"  # Listen on all available interfaces
    port = 50000

    # Create and start the OSC server
    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    print(f"Serving on {server.server_address}")

    # Run the server. This will keep the program running and listening for incoming messages.
    server.serve_forever()