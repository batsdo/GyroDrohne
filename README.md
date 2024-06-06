# GyroDrohne#

Projekt Gyro Drohne [Bearbeiten]
Unser Ziel war es, mithilfe des Gyroskops eines iPhones eine Drohne zu steuern.

Systemplan
Der Aufbau besteht wie man vielleicht vermutet hätte aus einer Drohne, einem iPhone und zusätzlich einem Laptop. Dieser dient als "Mittelpunkt" bzw. Kommunikationsmodul. Er enthält die Steuerbefehle vom iPhone, wandelt sie um und schickt sie in Echtzeit zur Drohne.

Meilensteine
Der erste Meilenstein war die Verbindung von Laptop zur Drohne.
Der zweite Meilenstein war die Verbindung von iPhone zum Laptop.
Der dritte Meilenstein war die "Hochzeit" der beiden Kommunikationswege.

Prinzipieller Aufbau
Die Drohne selbst spannt ein Wlan-Netzwerk auf, in welchem sich der Laptop und das iPhone befinden müssen. Die gesamte Software besteht aus einem Python-Programm.
Der erste Teil des Programms startet einen Webserver, mit dem sich das iPhone verbindet. Mithilfe der App "ZIG SIM" werden die relevanten Gyroskop-Daten des iPhones über OSC an den Webserver gesendet.
