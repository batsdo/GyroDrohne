from djitellopy import Tello
from pythonosc import dispatcher
from pythonosc import osc_server
import threading
import time

# Variablen zum Speichern der empfangenen Daten
first_value = None
second_value = None
touch_count = None

# Verbindung zur Drohne herstellen
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

def stop():
    tello.send_rc_control(0, 0, 0, 0)

# Handler für OSC-Nachrichten
def quaternion_handler(address, *args):
    global first_value, second_value
    if len(args) >= 2:
        first_value = args[0]
        second_value = args[1]
        print(f"First value: {first_value}, Second value: {second_value}")

def touchcount_handler(address, *args):
    global touch_count
    if len(args) >= 1:
        touch_count = args[0]
        print(f"Touch count: {touch_count}")

# Dispatcher für OSC-Nachrichten
dispatcher = dispatcher.Dispatcher()
dispatcher.map("/ZIGSIM/*/quaternion", quaternion_handler)
dispatcher.map("/ZIGSIM/*/touchcount", touchcount_handler)

# Funktion zum Aktualisieren der Drohnensteuerung basierend auf den Quaternion-Daten
def update_drone_control():
    global first_value, second_value, touch_count
    while True:
        if first_value is not None and second_value is not None:
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
            else:
                stop()
        
        if touch_count is not None:
            if touch_count == 2:
                takeoff()
                print("Takeoff")
            elif touch_count == 1:
                land()
                print("Landen")
        
        # Warten für einen kurzen Moment, bevor die Steuerung erneut aktualisiert wird
        time.sleep(0.1)

# Funktion zum Starten des OSC-Servers
def start_osc_server():
    ip = "0.0.0.0"  # Listen on all available interfaces
    port = 50000
    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    print(f"Serving on {server.server_address}")
    server.serve_forever()

# Starten des OSC-Servers in einem separaten Thread
osc_thread = threading.Thread(target=start_osc_server)
osc_thread.start()

# Starten der Drohnensteuerung in einem separaten Thread
control_thread = threading.Thread(target=update_drone_control)
control_thread.start()

# Hauptprogramm warten lassen, bis die Threads beendet werden
try:
    osc_thread.join()
    control_thread.join()
except KeyboardInterrupt:
    print("Programm wird beendet...")

# Drohne landen lassen und Verbindung trennen
land()
tello.end()