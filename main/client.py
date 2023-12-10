import json
import socket
import time

from gesture import get_pin
from gesture import speak_text
from recognize_user import recognize_face

RASPBERRY_IP = "192.168.137.170"


def start() -> str:
    username = recognize_face()
    with open("users_register.json", "r") as file:
        data = json.load(file)
    if data.get(username) is None:
        speak_text('Access Declined')
        return 'Access Declined'
    if data[username]["category"] == "Normal":
        speak_text("Detected " + username)
        return 'Access Declined'

    pin = get_pin(4)
    user_pin = data.get(username)["pin"]
    print(user_pin)
    if pin == str(user_pin):
        speak_text('Access Granted')
        return 'Access Granted'

    speak_text('Access Declined')
    return 'Access Declined'


# connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((RASPBERRY_IP, 8080))
print("CLIENT: connected")

while True:
    data = client.recv(4096).decode()
    if data == "Detect":
        msg = start()
        client.send(msg.encode())

        time.sleep(5)
        client.close()
        print("CLIENT: disconnected")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((RASPBERRY_IP, 8080))
        print("CLIENT: connected")
