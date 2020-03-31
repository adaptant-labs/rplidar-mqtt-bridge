import paho.mqtt.client as mqtt
import hashlib
import logging
import json

from . import MQTT_BROKER_PORT, MQTT_TOPIC_PREFIX, MQTT_BROKER_HOST, RPLIDAR_DEVICE
from rplidar import RPLidar
from .utils import iso8601_timestamp


def on_mqtt_connect(client, userdata, flags, rc):
    logging.info("on_mqtt_connect: connected with result code: '%s': %s", str(rc), mqtt.connack_string(rc))


class RPLidarMQTTBridge(object):
    health_state = 0

    def __init__(self, device=RPLIDAR_DEVICE, topic_prefix=MQTT_TOPIC_PREFIX, host=MQTT_BROKER_HOST,
                 port=MQTT_BROKER_PORT, reset=False):

        self.mqtt = mqtt.Client(client_id="rplidar_mqtt_bridge", clean_session=True)
        self.mqtt.on_connect = on_mqtt_connect
        self.mqtt.connect(host=host, port=port)

        self.lidar = RPLidar(device)

        # Generate a unique topic identifier by using the MD5 hash of the device serial number
        info = self.lidar.get_info()
        serial = info['serialnumber']
        serial_hash = hashlib.md5(serial.encode()).hexdigest()

        self.topic_prefix = topic_prefix + '/' + serial_hash

        if reset is True:
            self.clear_rplidar_readings()

        self.report_rplidar_source()
        self.report_rplidar_info(info)

    def generate_topic(self, subtopic):
        return self.topic_prefix + subtopic

    def clear_rplidar_readings(self):
        self.mqtt.publish(self.generate_topic('/measurement'), None, 1, True)

    def clear_rplidar_health(self):
        self.mqtt.publish(self.generate_topic('/health'), None, 1, True)

    def report_rplidar_measurement(self, measurement):
        # Only publish valid measurements
        if self.measurement_valid(measurement):
            reading = dict(quality=measurement[1], angle=measurement[2], distance=measurement[3],
                           timestamp=iso8601_timestamp())
            if measurement[3] == 0:
                print("logging invalid distance")
            self.publish_event(reading=reading)

    def report_rplidar_info(self, info):
        self.publish_event_raw(topic='/info/model', reading=info['model'])
        self.publish_event_raw(topic='/info/hardware', reading=info['hardware'])
        self.publish_event_raw(topic='/info/firmware', reading=("%d.%d" % (info['firmware'][0], info['firmware'][1])))
        self.publish_event_raw(topic='/info/serialnumber', reading=info['serialnumber'])

    def report_rplidar_source(self):
        self.publish_event_raw(topic='/source', reading="rplidar_mqtt_bridge")

    def report_rplidar_health(self, health):
        self.publish_event(reading=health, topic='/health')

    @staticmethod
    def measurement_valid(measurement):
        if len(measurement) != 4:
            return False

        # In the case of an invalid measurement, the distance and quality are both set to 0
        if measurement[1] == 0:
            return False
        if measurement[3] == 0.0:
            return False

        return True

    def publish_event(self, reading, topic='/measurement', raw=False):
        logging.debug(reading)

        if raw is True:
            data = reading
        else:
            data = json.dumps(reading, sort_keys=False)

        self.mqtt.publish(self.generate_topic(topic), data)

    def publish_event_raw(self, reading, topic='/measurement'):
        self.publish_event(reading, topic, raw=True)

    def poll(self):
        self.mqtt.loop_start()

        try:
            health = self.lidar.get_health()[0]
            if self.health_state != health:
                self.report_rplidar_health(health)

            for measurement in self.lidar.iter_measurments():
                self.report_rplidar_measurement(measurement)
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()

    def cleanup(self):
        self.lidar.stop()
        self.lidar.disconnect()

        self.clear_rplidar_health()

        self.mqtt.disconnect()
        self.mqtt.loop_stop()
