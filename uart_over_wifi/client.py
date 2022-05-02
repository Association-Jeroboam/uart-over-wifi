from aioconsole import ainput
import asyncio
import socketio
import os
import pty
import argparse
import sys
import fcntl
import struct

sio = socketio.AsyncClient()
serial_port = None
data_stream_started = False
byte_buffer = bytearray()
synchro_word = b'\xef\xbe\xad\xde'
data_frame = bytearray(68)

def extract():
    global byte_buffer

    idx = byte_buffer.find(synchro_word)
    if idx > -1:
        if len(byte_buffer) >= idx + len(synchro_word) + len(data_frame):
            frame = byte_buffer[idx+len(synchro_word):idx+len(synchro_word)+len(data_frame)]
            byte_buffer = byte_buffer[idx+len(synchro_word)+len(data_frame):]
            data = struct.unpack("<Iffffffffffffffff", bytes(frame))
            return data

    return None
@sio.event
async def connect():
    print('Connected to server.')

@sio.event
async def message(data):
    global data_stream_started
    global byte_buffer

    if not data_stream_started:
        try:
            print(f"{data.decode()}", end="")
        except UnicodeDecodeError:
            data_stream_started = True
    else:
        ba = bytearray(data)
        byte_buffer.extend(ba)


        data = extract()
        while data is not None:
            print(f"{data}", end="")
            data = extract()




@sio.event
async def disconnect():
    print('Disconnected from server.')

async def send_message(data):
    global sio

    try:
        await sio.emit('message', data)
        print(f'{data}', end="")
    except Exception as err:
        print(f"Could not send message: {err}", file=sys.stderr)

async def send_input():
    global data_stream_started

    while True:
        line = await ainput(">>>")

        if line == "data_stream start":
            data_stream_started = True
        elif line == "data_stream stop":
            data_stream_started = False

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
