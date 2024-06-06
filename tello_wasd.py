from djitellopy import Tello
from pynput import keyboard
import time

# Verbindung zur Drohne herstellen
tello = Tello()
tello.connect()

# Tastenbelegung
forward_key = 'w'
backward_key = 's'
left_key = 'a'
right_key = 'd'
takeoff_key = "t"
land_key = "l"

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

# Tastenereignisse abfangen und Drohne entsprechend steuern
def on_press(key):
    try:
        if key.char == forward_key:
            move_forward()
        elif key.char == backward_key:
            move_backward()
        elif key.char == left_key:
            move_left()
        elif key.char == right_key:
            move_right()
        elif key.char == takeoff_key:
            takeoff()
        elif key.char == land_key:
            land()
    except AttributeError:
        pass

def on_release(key):
    if key == keyboard.Key.esc:
        # Stoppt das Programm, wenn die Escape-Taste gedrückt wird
        return False
    else:
        stop()

# Listener für Tastatureingaben starten
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    # Warten, bis das Programm beendet wird
    listener.join()

# Drohne landen lassen und Verbindung trennen
land()
tello.end()
