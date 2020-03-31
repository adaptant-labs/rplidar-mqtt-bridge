import argparse
import logging

from rplidar_mqtt_bridge.bridge import RPLidarMQTTBridge
from rplidar_mqtt_bridge import MQTT_BROKER_PORT, MQTT_BROKER_HOST, RPLIDAR_DEVICE


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--mqtt-host",
                        help="MQTT broker host to connect to",
                        type=str,
                        default=MQTT_BROKER_HOST)
    parser.add_argument("--mqtt-port",
                        help="MQTT broker port to connect to",
                        type=int,
                        default=MQTT_BROKER_PORT)
    parser.add_argument("--rplidar-device",
                        help="RPLiDAR device path",
                        default=RPLIDAR_DEVICE,
                        type=str)
    parser.add_argument("--reset-messages",
                        help="Clear existing readings",
                        action='store_true',
                        default=False)

    args = parser.parse_args()

    bridge = RPLidarMQTTBridge(device=args.rplidar_device, host=args.mqtt_host, port=args.mqtt_port,
                               reset=args.reset_messages)
    print("Connected to RPLiDAR device at {}".format(args.rplidar_device))
    print("Publishing to {}:{}/{}...".format(args.mqtt_host, args.mqtt_port, bridge.topic_prefix))
    bridge.poll()
    print("Exiting")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s")
    main()
