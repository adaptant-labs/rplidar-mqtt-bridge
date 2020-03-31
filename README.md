# RPLIDAR-MQTT-Bridge

This package provides a simple app for bridging data between a SLAMTEC [RPLIDAR] device (specifically tested on an
[RPLIDAR-A1]) and an MQTT Broker.

## Known Limitations

At present this is limited to streaming data from the LiDAR device to the broker, and assumes a direct USB connection.
This will be extended to support controlling motor speed and scanning frequency in a future version in order to work as
a bi-directional _bridge_.

In addition to the direct USB connection, this will also be extended to support drving the device directly via GPIOs
(note that on a Raspberry Pi this requires an external 5V DC supply and a 3.3V-5V level shifter on the GPIO & PWM pins,
given the power requirements of the motor itself).

[RPLIDAR]: https://www.slamtec.com/en/Lidar
[RPLIDAR-A1]: https://www.slamtec.com/en/Lidar/A1

## Quick Start

Provided that a direct connection with the device has already been established via USB and the MQTT Broker is directly
reachable on the same machine, `rplidar_mqtt_bridge` can be run as-is:

```
$ rplidar_mqtt_bridge
Connected to RPLiDAR device at /dev/ttyUSB0
Publishing to localhost:1883/rplidar/9efxxxxxxxxxxxx...
```

## MQTT Format

The following MQTT topic and sub-topics are published:

```
/rplidar/<device-id>/measurement
/rplidar/<device-id>/source
/rplidar/<device-id>/info/model
/rplidar/<device-id>/info/hardware
/rplidar/<device-id>/info/firmware
/rplidar/<device-id>/info/serialnumber
```

The `measurement` itself is provided in a JSON-encoded payload, consisting of the sensor readings and an ISO 8601
timestamp:

```json
{
  "quality": 13,
  "angle": 328.703125,
  "distance": 353,
  "timestamp": "2020-03-31T17:28:29.828000"
}
```

## Configuration

Configuration via an `rplidar-mqtt.ini` file is also possible, with the defaults set as below:

```ini
[DEFAULT]

MQTT_BROKER_HOST="localhost"
MQTT_BROKER_PORT="1336"
MQTT_TOPIC_PREFIX="rplidar"
RPLIDAR_DEVICE_PATH="/dev/ttyUSB0"
```

the configuration file can live in any of:

- `rplidar-mqtt.ini`
- `/etc/rplidar-mqtt-bridge/rplidar-mqtt.ini`
- `$HOME/.config/rplidar-mqtt-bridge/rplidar-mqtt.ini`

## Usage


```
$ rplidar_mqtt_bridge --help
usage: rplidar_mqtt_bridge [-h] [--mqtt-host MQTT_HOST]
                           [--mqtt-port MQTT_PORT]
                           [--rplidar-device RPLIDAR_DEVICE]
                           [--reset-messages]

optional arguments:
  -h, --help            show this help message and exit
  --mqtt-host MQTT_HOST
                        MQTT broker host to connect to
  --mqtt-port MQTT_PORT
                        MQTT broker port to connect to
  --rplidar-device RPLIDAR_DEVICE
                        RPLiDAR device path
  --reset-messages      Clear existing readings
```

## Docker Image

It is also possible to deploy and run `rplidar_mqtt_bridge` from a Docker image. In
this case, the host where the image is being run will need to pass on the
RPLiDAR device connection to the container. This can be achieved two different ways:

To run the image in `privileged` mode, where the container has direct access to
the host's devices, allowing the application to try and find the RPLiDAR device
directly by itself:

```
$ docker run --privileged adaptant/rplidar-mqtt-bridge:latest
...
```

Or in a more constrained way, in which the specific device that the RPLiDAR device
connection is made to be passed through explicitly:

```
$ docker run --device /dev/ttyUSB0 adaptant/rplidar-mqtt-bridge:latest
...
```

## License

`rplidar-mqtt-bridge` is licensed under the terms of the Apache 2.0 license,
the full version of which can be found in the LICENSE file included in the
distribution.
