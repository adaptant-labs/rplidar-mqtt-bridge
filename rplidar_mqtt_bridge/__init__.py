import os
from .parser import UnquotedConfigParser

parser = UnquotedConfigParser()

paths = ['rplidar-mqtt.ini', '/etc/rplidar-mqtt-bridge/rplidar-mqtt.ini',
         os.getenv('HOME') + '/.config/rplidar-mqtt-bridge/rplidar-mqtt.ini']

parser.read(paths)

config = parser['DEFAULT']

MQTT_BROKER_HOST = config.get("MQTT_BROKER_HOST", "localhost")
MQTT_BROKER_PORT = config.get("MQTT_BROKER_PORT", "1883")
MQTT_TOPIC_PREFIX = config.get("MQTT_TOPIC_PREFIX", "rplidar")

RPLIDAR_DEVICE = config.get("RPLIDAR_DEVICE", "/dev/ttyUSB0")
