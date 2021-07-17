from aioconsole import ainput
import asyncio
import socketio
import os
import pty
import argparse
import sys
import fcntl

sio = socketio.AsyncClient()
serial_port = None

@sio.event
async def connect():
    print('Connected to server.')

@sio.event
async def message(data):
    try:
        print(f"[RECV] {data.decode()}")
    except UnicodeDecodeError:
        print(f"[RECV] {data}")

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

async def send_input():
    while True:
        line = await ainput(">>>")
        await send_message(line + "\r\n")

async def flash(path):
    print("Flashing...")
    if not os.path.exists(path):
        print(f"Error: path {path} does not exists")
        sys.exit(1)

    with open(path, 'rb') as f:
        file_data = f.read()

    async def flash_callback(*res):
        await sio.disconnect()

        exit_code, stdin, stdout = res
        if not exit_code:
            print("Success")
            sys.exit(0)
        else:
            print(f"Flash error: {stdout}")
            sys.exit(1)

    await sio.emit('flash', file_data, callback=flash_callback)
    await asyncio.sleep(10)
    print("Error: timeout on flash")
    sys.exit(1)

async def main(config):
    await sio.connect(f'http://{config.host}:{config.port}')

    if config.flash:
        await flash(config.flash)
        sys.exit(0)

    asyncio.create_task(send_input())
    await sio.wait()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start a socketio client which outputs messages on a virtual UART port.')
    parser.add_argument('host', type=str, help='Host to connect')
    parser.add_argument('port', type=int, help='Port to connect', default=8080, nargs="?")
    parser.add_argument('-f', '--flash', type=str, help='Build archive .tar.gz path to flash', nargs="?")
    config = parser.parse_args()

    print("Loaded config:")
    print(config)

    try:
        asyncio.run(main(config))
    except KeyboardInterrupt:
        print("Received exit, exiting")
        sio.disconnect()