import socket
import time

import RPi.GPIO as GPIO

RASPBERRY_IP = "192.168.137.170"

LATCH_PIN = 22
PROXIMITY_PIN = 18
BUZZER_PIN = 16
LED_GREEN_PIN = 3
LED_RED_PIN = 5
server = None


def setup():
    global server
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(LATCH_PIN, GPIO.OUT)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.setup(LED_GREEN_PIN, GPIO.OUT)
    GPIO.setup(LED_RED_PIN, GPIO.OUT)
    GPIO.setup(PROXIMITY_PIN, GPIO.IN)

    GPIO.output(LATCH_PIN, GPIO.LOW)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    GPIO.output(LED_GREEN_PIN, GPIO.LOW)
    GPIO.output(LED_RED_PIN, GPIO.LOW)

    # start server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((RASPBERRY_IP, 8080))
    server.listen(5)
    print("SERVER: started")


def beep(times: int = 1):
    for i in range(times):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(BUZZER_PIN, GPIO.LOW)


def loop():
    global server
    while True:
        if GPIO.input(PROXIMITY_PIN) == 1:
            continue

        print("Someone Came, start detecting")
        beep()

        if server is None:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((RASPBERRY_IP, 8080))
            server.listen(5)

        conn, addr = server.accept()
        print("Detecting through cam")
        conn.send("Detect".encode())
        print("SERVER: connection to Client established")
        while True:
            data = conn.recv(4096).decode()
            if not data:
                break
            print(data)
            if data == "Access Granted":
                GPIO.output(LED_GREEN_PIN, GPIO.HIGH)
                beep()
                GPIO.output(LATCH_PIN, GPIO.HIGH)
                time.sleep(5)
                GPIO.output(LATCH_PIN, GPIO.LOW)
                GPIO.output(LED_GREEN_PIN, GPIO.LOW)
                break
            elif data == "Access Declined":
                GPIO.output(LED_RED_PIN, GPIO.HIGH)
                beep(3)
                GPIO.output(LED_RED_PIN, GPIO.LOW)
                break
        # close connection and exit
        conn.close()


if __name__ == '__main__':
    setup()
    loop()
