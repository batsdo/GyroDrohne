from pythonosc import dispatcher
from pythonosc import osc_server
from djitellopy import Tello
from pynput import keyboard


tello = Tello()
tello.connect()

# Geschwindigkeit festlegen (Werte zwischen 10 und 100)
speed = 50

# Funktionen zum Steuern der Drohne
def takeoff():
    tello.takeoff()

def land():
    tello.land()

def move_forward():
    tello.send_rc_control(0, speed, 0, 0)

def move_backward():
    tello.send_rc_control(0, -speed, 0, 0)

def move_left():
    tello.send_rc_control(-speed, 0, 0, 0)

def move_right():
    tello.send_rc_control(speed, 0, 0, 0)

def yaw_left():
    tello.send_rc_control(0,0,0,-speed)

def yaw_right():
    tello.send_rc_control(0,0,0,speed)

def stop():
    tello.send_rc_control(0, 0, 0, 0)

def quaternion_handler(address, *args):
    if len(args) >= 2:
        global first_value
        first_value = args[0]
        global second_value
        second_value = args[1]
        global third_value
        third_value = args[2]
        print(f"First value: {first_value}, Second value: {second_value}")
        if first_value < -0.3:
            move_forward()
            print("Vorwärts")
        elif first_value > 0.3:
            move_backward()
            print("Rückwärts")
        elif second_value < -0.3:
            move_left()
            print("Links")
        elif second_value > 0.3:
            move_right()
            print("Rechts")
        elif third_value > 0.2:
            yaw_left()
            print("Links drehen")
        elif third_value < -0.2:
            yaw_right()
            print("Rechts drehen")
        else:
            stop()
    else:
        print("Received quaternion message with insufficient arguments")

def touchcount_handler(address, *args):
    global touch_count
    if len(args) >= 1:
        touch_count = args[0]
        print(f"Touch count: {touch_count}")
        if touch_count == 2:
            takeoff()
            print("Takeoff")
        elif touch_count == 1:
            land()
            print("Landing")
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
