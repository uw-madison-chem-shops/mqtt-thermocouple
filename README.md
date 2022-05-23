# MQTT thermocouple

Simple project for getting thermocouple sensors online using MQTT.

Designed to work with [mqtt.chem.wisc.edu](https://mqtt.chem.wisc.edu/).

## Repository

This is an open source hardware project licensed under the CERN Open Hardware Licence Version 2 - Permissive.
Please see the LICENSE file for the complete license.

This repository is being mirrored to several version control systems in an attempt to ensure maximum avaliability.

| name             | url                                                        |
| ---------------- | ---------------------------------------------------------- |
| GitHub (primary) | https://github.com/uw-madison-chem-shops/mqtt-thermocouple |
| GitLab           | https://gitlab.com/uw-madison-chem-shops/mqtt-thermocouple |

## PCB

This PCB was designed using KiCAD version 5.
Refer to `mqtt-thermocouple.pdf` for schematic.
Refer to `mqtt-thermocouple.csv` for bill of materials.
PCB images generated with [tracespace](https://github.com/tracespace/tracespace) follow.

<img src="./mqtt-thermocouple-.top.svg" width="100%"/>
<img src="./mqtt-thermocouple-.bottom.svg" width="100%"/>

## Firmware

This project uses [micropython](https://micropython.org/), specifically [microhomie](https://github.com/microhomie/microhomie).
Refer to the "firmware" directory in this repository for detailed instructions.

## Changelog

### Unprinted

### B

#### added
- oshw logo
- github link

#### fixed
- resized holes for mounting piece
- added i2c pull up resistors

### A

#### Added
- initial design

