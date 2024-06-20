from pythonosc import dispatcher
from pythonosc import osc_server
from djitellopy import Tello
from pynput import keyboard

dummy1 = 0
dummy2 = 0

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
    tello.send_rc_control(0, 0, 0, -speed)

def yaw_right():
    tello.send_rc_control(0, 0, 0, speed)

def move_up():
    tello.send_rc_control(0, 0, speed, 0)

def move_down():
    tello.send_rc_control(0, 0, -speed, 0)

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
        global fourth_value
        fourth_value = args[3]
        print(f"w: {first_value}, x: {second_value}, y: {third_value}, z: {fourth_value}")
        if second_value < -0.2:
            move_forward()
            print("Vorwärts")
        elif second_value > 0.2:
            move_backward()
            print("Rückwärts")
        elif third_value < -0.2:
            move_left()
            print("Links")
        elif third_value > 0.2:
            move_right()
            print("Rechts")
        elif fourth_value > 0.2:
            yaw_left()
            print("Links drehen")
        elif fourth_value < -0.2:
            yaw_right()
            print("Rechts drehen")
        elif dummy1 == 1:
            move_up()
            print("Flying up")
        elif dummy2 == 1:
            move_down()
            print("Flying down")
        else:
            stop()

    else:
        print("Received quaternion message with insufficient arguments")

def button_handler(address, *args):
    global number, value, dummy1, dummy2
    if len(args) >= 1:
        number = args[0]
        value = args[1]

        print(f"Button: {number}, Value: {value}")
        if number == 1 and value == 1:
            takeoff()
            print("Takeoff")
        elif number == 3 and value == 1:
            land()
            print("Landing")
        elif number == 7 and value == 1:
            dummy1 = 1
        elif number == 9 and value == 1:
            dummy2 = 1
        elif number == 7 and value == 0:
            dummy1 = 0
        elif number == 9 and value == 0:
            dummy2 = 0

    else:
        print("Received touch count message with insufficient arguments")


if __name__ == "__main__":
    # Dispatcher to handle incoming OSC messages
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/gyrosc/quat", quaternion_handler)
    dispatcher.map("/gyrosc/button", button_handler)

    # Define the IP address and port for the OSC server
    ip = "0.0.0.0"  # Listen on all available interfaces
    port = 50000

    # Create and start the OSC server
    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    print(f"Serving on {server.server_address}")

    # Run the server. This will keep the program running and listening for incoming messages.
    server.serve_forever()
