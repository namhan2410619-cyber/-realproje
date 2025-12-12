import paho.mqtt.publish as publish

def send_alarm(wake_time):
    publish.single("iot/alarm", payload=wake_time, hostname="raspberrypi.local")
