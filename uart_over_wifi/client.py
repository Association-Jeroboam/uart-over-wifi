import serial
import asyncio
import socketio
import os
import pty
import argparse
import sys
import fcntl

sio = socketio.AsyncClient()
serial_port = None
master, slave = None, None

@sio.event
async def connect():
    print('Connected to server.')
    await send_message(str.encode("data_stream start"))

@sio.event
async def message(data):
    global master

    # print(f'[RECV] {data}')

    # if serial_port is None:
    #     print("Warning: serial port is not initialized")
    #     return

    # try:
    #     print("write...")
    #     serial_port.write(data)
    # except Exception as err:
    #     print(f"could not write to port: {err}")


    if master is None:
        print("Warning: serial port is not initialized")
        return

    try:
        os.write(master, data)
        os.fsync(master)
        print(data)
    except BlockingIOError as err:
        print("Caught BlockingIOError")
        print(err)
        pass
    except Exception as err:
        print(f"Could not write to port: {err}")

@sio.event
async def disconnect():
    print('Disconnected from server.')

async def send_message(data):
    global sio

    try:
        await sio.emit('message', data)
        print(f'[SEND] {data}')
    except Exception as err:
        print(f"Could not send message: {err}", file=sys.stderr)


def create_serial_port(path, baudrate, timeout):
    global master, slave, serial_port

    try:
        master, slave = pty.openpty()

        flags = fcntl.fcntl(master, fcntl.F_GETFL)
        flags |= os.O_NONBLOCK
        fcntl.fcntl(master, fcntl.F_SETFL, flags)

        port_name = os.ttyname(slave)

        if os.path.exists(path) or os.path.islink(path):
            os.remove(path)

        os.symlink(port_name, path)

        # serial_port = serial.Serial(port_name, baudrate, timeout=timeout, write_timeout=timeout)
    except Exception as err:
        print(f"Could not create serial port: {err}", file=sys.stderr)
        sys.exit(1)

async def read_serial():
    global master

    while True:
        if master is not None and serial_port.in_waiting > 0: 
            try:
                data_str = serial_port.read(serial_port.in_waiting)
                print(data_str.hex()) 
            except Exception as err:
                print(f"Could not read serial: {err}", file=sys.stderr)
                continue

            await send_message(data_str)


        await asyncio.sleep(0.01)

async def test_send():
    while True:
        await send_message("mumuxe")

        await asyncio.sleep(2)

async def main(config):
    create_serial_port(config.tty_path, config.baudrate, config.timeout)

    await sio.connect('http://localhost:8080')
    # asyncio.create_task(test_send())
    await sio.wait()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start a socketio client which outputs messages on a virtual UART port.')
    parser.add_argument('tty_path', type=str, help='tty output path')
    parser.add_argument('--baudrate', type=int, help='tty baudrate', default=115200)
    parser.add_argument('--timeout', type=int, help='tty timeout in seconds', default=1)
    config = parser.parse_args()

    print("Loaded config:")
    print(config)

    try:
        asyncio.run(main(config))
    except KeyboardInterrupt:
        print("Received exit, exiting")