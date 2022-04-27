# uart-over-wifi
## Dependencies
### Pyenv
```bash
sudo apt install libbz2-dev libreadline-dev libffi-dev

curl https://pyenv.run | bash

echo 'export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"' >> ~/.bashrc

source ~/.bashrc

pyenv install 3.9
pyenv global 3.9

```

### Poetry
```curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -```

### Openocd
```sudo apt update && sudo apt install -y openocd```

## Installation
```poetry install```

### Run without sudo
Add user in dialout for serial port access
```sudo usermod -a -G dialout $(whoami)```

Add user in plugdev for openocd
```sudo usermod -a -G plugdev $(whoami)```

Create file `/etc/udev/rules.d/99-openocd.rules` with content:

```
# Copy this file to /etc/udev/rules.d/

ACTION!="add|change", GOTO="openocd_rules_end"
SUBSYSTEM!="usb|tty|hidraw", GOTO="openocd_rules_end"

# Please keep this list sorted by VID:PID

# opendous and estick
ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="204f", MODE="664", GROUP="plugdev"

# Original FT232/FT245 VID:PID
ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", MODE="664", GROUP="plugdev"

# Original FT2232 VID:PID
ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6010", MODE="664", GROUP="plugdev"

# Original FT4232 VID:PID
ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6011", MODE="664", GROUP="plugdev"

# Original FT232H VID:PID
ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6014", MODE="664", GROUP="plugdev"

# DISTORTEC JTAG-lock-pick Tiny 2
ATTRS{idVendor}=="0403", ATTRS{idProduct}=="8220", MODE="664", GROUP="plugdev"

# TUMPA, TUMPA Lite
ATTRS{idVendor}=="0403", ATTRS{idProduct}=="8a98", MODE="664", GROUP="plugdev"
ATTRS{idVendor}=="0403", ATTRS{idProduct}=="8a99", MODE="664", GROUP="plugdev"

# XDS100v2
ATTRS{idVendor}=="0403", ATTRS{idProduct}=="a6d0", MODE="664", GROUP="plugdev"

# Xverve Signalyzer Tool (DT-USB-ST), Signalyzer LITE (DT-USB-SLITE)
ATTRS{idVendor}=="0403", ATTRS{idProduct}=="bca0", MODE="664", GROUP="plugdev"
ATTRS{idVendor}=="0403", ATTRS{idProduct}=="bca1", MODE="664", GROUP="plugdev"

# TI/Luminary Stellaris Evaluation Board FTDI (several)
ATTRS{idVendor}=="0403", ATTRS{idProduct}=="bcd9", MODE="664", GROUP="plugdev"

# TI/Luminary Stellaris In-Circuit Debug Interface FTDI (ICDI) Board
ATTRS{idVendor}=="0403", ATTRS{idProduct}=="bcda", MODE="664", GROUP="plugdev"

# egnite Turtelizer 2
ATTRS{idVendor}=="0403", ATTRS{idProduct}=="bdc8", MODE="664", GROUP="plugdev"

# Section5 ICEbear
ATTRS{idVendor}=="0403", ATTRS{idProduct}=="c140", MODE="664", GROUP="plugdev"
ATTRS{idVendor}=="0403", ATTRS{idProduct}=="c141", MODE="664", GROUP="plugdev"

# Amontec JTAGkey and JTAGkey-tiny
ATTRS{idVendor}=="0403", ATTRS{idProduct}=="cff8", MODE="664", GROUP="plugdev"

# TI ICDI
ATTRS{idVendor}=="0451", ATTRS{idProduct}=="c32a", MODE="664", GROUP="plugdev"

# STLink v1
ATTRS{idVendor}=="0483", ATTRS{idProduct}=="3744", MODE="664", GROUP="plugdev"

# STLink v2
ATTRS{idVendor}=="0483", ATTRS{idProduct}=="3748", MODE="664", GROUP="plugdev"

# STLink v2-1
ATTRS{idVendor}=="0483", ATTRS{idProduct}=="374b", MODE="664", GROUP="plugdev"

# Hilscher NXHX Boards
ATTRS{idVendor}=="0640", ATTRS{idProduct}=="0028", MODE="664", GROUP="plugdev"

# Hitex STR9-comStick
ATTRS{idVendor}=="0640", ATTRS{idProduct}=="002c", MODE="664", GROUP="plugdev"

# Hitex STM32-PerformanceStick
ATTRS{idVendor}=="0640", ATTRS{idProduct}=="002d", MODE="664", GROUP="plugdev"

# Amontec JTAGkey-HiSpeed
ATTRS{idVendor}=="0fbb", ATTRS{idProduct}=="1000", MODE="664", GROUP="plugdev"

# IAR J-Link USB
ATTRS{idVendor}=="1366", ATTRS{idProduct}=="0101", MODE="664", GROUP="plugdev"
ATTRS{idVendor}=="1366", ATTRS{idProduct}=="0102", MODE="664", GROUP="plugdev"
ATTRS{idVendor}=="1366", ATTRS{idProduct}=="0103", MODE="664", GROUP="plugdev"
ATTRS{idVendor}=="1366", ATTRS{idProduct}=="0104", MODE="664", GROUP="plugdev"

# J-Link-OB (onboard)
ATTRS{idVendor}=="1366", ATTRS{idProduct}=="0105", MODE="664", GROUP="plugdev"

# Raisonance RLink
ATTRS{idVendor}=="138e", ATTRS{idProduct}=="9000", MODE="664", GROUP="plugdev"

# Debug Board for Neo1973
ATTRS{idVendor}=="1457", ATTRS{idProduct}=="5118", MODE="664", GROUP="plugdev"

# Olimex ARM-USB-OCD
ATTRS{idVendor}=="15ba", ATTRS{idProduct}=="0003", MODE="664", GROUP="plugdev"

# Olimex ARM-USB-OCD-TINY
ATTRS{idVendor}=="15ba", ATTRS{idProduct}=="0004", MODE="664", GROUP="plugdev"

# Olimex ARM-JTAG-EW
ATTRS{idVendor}=="15ba", ATTRS{idProduct}=="001e", MODE="664", GROUP="plugdev"

# Olimex ARM-USB-OCD-TINY-H
ATTRS{idVendor}=="15ba", ATTRS{idProduct}=="002a", MODE="664", GROUP="plugdev"

# Olimex ARM-USB-OCD-H
ATTRS{idVendor}=="15ba", ATTRS{idProduct}=="002b", MODE="664", GROUP="plugdev"

# USBprog with OpenOCD firmware
ATTRS{idVendor}=="1781", ATTRS{idProduct}=="0c63", MODE="664", GROUP="plugdev"

# TI/Luminary Stellaris In-Circuit Debug Interface (ICDI) Board
ATTRS{idVendor}=="1cbe", ATTRS{idProduct}=="00fd", MODE="664", GROUP="plugdev"

# Marvell Sheevaplug
ATTRS{idVendor}=="9e88", ATTRS{idProduct}=="9e8f", MODE="664", GROUP="plugdev"

# CMSIS-DAP compatible adapters
ATTRS{product}=="*CMSIS-DAP*", MODE="664", GROUP="plugdev"

LABEL="openocd_rules_end"
```

Restart udev
```
sudo udevadm trigger
```

Source: https://forgge.github.io/theCore/guides/running-openocd-without-sudo.html

## Usage
### Server
Connect / reconnect to /dev/ttyACM* device:

```
poetry run python uart_over_wifi/server.py /dev/ttyACM
```

### Client
#### Uart console
```
poetry run python uart_over_wifi/client.py [ip] [port]
```

### Flash
```
tar -czvf build.tar.gz -C ../MotionBoardFirmware/firmware/src/hardware/robot ./cfg ./build/MotionBoard.bin

poetry run python uart_over_wifi/client.py --flash ./build.tar.gz [ip] [port]
```