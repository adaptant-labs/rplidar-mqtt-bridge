from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name="rplidar_mqtt_bridge",
    version="0.0.1",
    author="Adaptant Labs",
    author_email="labs@adaptant.io",
    url="https://github.com/adaptant-labs/rplidar-mqtt-bridge",
    description="A simple bridge between an RPLIDAR device and an MQTT Broker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    packages=find_packages(),
    zip_safe=False,
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [ 'rplidar_mqtt_bridge = rplidar_mqtt_bridge.main:main' ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: System :: Hardware",
        "Programming Language :: Python :: 3",
        "Topic :: Communications",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
    ],
    keywords="rplidar lidar sensors mqtt",
)
