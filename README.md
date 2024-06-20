#Projekt Gyro Drohne [Bearbeiten]
Unser Ziel war es, mithilfe des Gyroskops eines iPhones eine Drohne zu steuern.

#Systemplan
Der Aufbau besteht wie man vielleicht vermutet hätte aus einer Drohne, einem iPhone und zusätzlich einem Laptop. Dieser dient als "Mittelpunkt" bzw. Kommunikationsmodul. Er enthält die Steuerbefehle vom iPhone, wandelt sie um und schickt sie in Echtzeit zur Drohne.
Das iPhone eröffnet einen "Persönlichen Hotspot". Darauf greift das MacBook per USB-Kabel zu. Außerdem ist das MacBook per Wlan mit dem Hotspot der Tello Drohne verbunden.

#Meilensteine
1. Meilenstein (April): Verbindung von Laptop zur Drohne

2. Meilenstein (Mai): Verbindung von iPhone zum Laptop

3. Meilenstein (Juni): "Hochzeit" der beiden Kommunikationswege

#Prinzipieller Aufbau
Die gesamte Software besteht aus einem Python-Programm.

Das Programm startet einen Webserver, mit dem sich das iPhone verbindet. Mithilfe der App "GyrOSC" werden die relevanten Gyroskop-Daten des iPhones über OSC an den Webserver gesendet. Die OSC-Daten werden vom Python Code interpretiert und in richtungsweisende Daten umgewandelt, die dann mithilfe einer Tello-Bibliothek an die Drohne geschickt werden.

Beim MacBook kann man über den Command "ifconfig" die IP-Adresse für GyrOSC rausfinden. Die relevante IP-Adresse befindet sich bei "en6": (172.20.10.6)

Für die Steuerung von vorne/hinten, links/rechts und Rotieren werden die Quaternion-Daten des iPhones verwendet. Außerdem verfügt die App "GyrOSC" über eine Funktion, die verschiedene Buttons zur Verfügung stellt. Diese Daten werden auch über OSC an den Laptop gesendet und werden zum Takeoff, Landen, Hoch- und Runterfliegen der Drohne verwendet.
