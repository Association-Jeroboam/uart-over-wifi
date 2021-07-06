import asyncio
import serial
import aiohttp
import socketio
import argparse
import sys
import glob

config = None
sio = socketio.AsyncServer()
app = aiohttp.web.Application()
sio.attach(app)

serial_port = None

@sio.event
def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def message(sid, data):
    print(f"[RECV] {data}")

    if serial_port is None:
        print("Warning: serial port is not initialized")
        return

    try:
        serial_port.write(data)
    except Exception as err:
        print(f"Could not write to port: {err}")

@sio.event
def disconnect(sid):
    print(f'Client disconnected: {sid}')

async def send_message(data):
    global sio

    try:
        await sio.emit('message', data)
        print(f'[SEND] {data}')
    except Exception as err:
        print(f"Could not send message: {err}", file=sys.stderr)

async def connect_to_serial(port_glob, baudrate, timeout=1):
    global serial_port
    serial_port = None

    while serial_port is None:
        ports_names = glob.glob(f'{port_glob}*')
        print(f"Detected ports: {ports_names}")

        for port_name in ports_names:
            try:
                serial_port = serial.Serial(port_name, baudrate, timeout=timeout, write_timeout=timeout)
                print(f"Connected to serial port: {port_name}")
                break
            except Exception as err:
                print(f"Could not open port: {err}", file=sys.stderr)

        await asyncio.sleep(1)

async def read_serial():
    global serial_port

    while True:
        if serial_port is not None: 
            try:
                if serial_port.in_waiting > 0:
                    data_str = serial_port.read(serial_port.in_waiting)
                    await send_message(data_str)
            except Exception as err:
                print(f"Could not read serial: {err}", file=sys.stderr)
                serial_port = None
                await connect_to_serial(config.tty_path, config.baudrate)
                continue

        await asyncio.sleep(0.01)

def close_serial():
    global serial_port

    if serial_port is None:
        return

    try:
        serial_port.close()
        print("Serial port closed.")
    except Exception as err:
        print(f"Could not close serial port: {err}", file=sys.stderr)

async def test_send():
    while True:
        await send_message("ping".encode())
        await asyncio.sleep(0.01)

async def start_server(host, port):
    try:
        runner = aiohttp.web.AppRunner(app)
        await runner.setup()
        site = aiohttp.web.TCPSite(runner, host, port)    
        await site.start()
        print(f'Server listening to {host}:{port}')
    except Exception as err:
        print(f"Could not start server: {err}", file=sys.stderr)
        sys.exit(1)

async def main(config):
    await connect_to_serial(config.tty_path, config.baudrate)
    await start_server(config.host, config.port)
    # asyncio.create_task(test_send())
    asyncio.create_task(read_serial())

    await asyncio.Event().wait()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start a socketio webserver which broadcast UART input of a given tty.')
    parser.add_argument('--host', type=str, help='Host to bind to', default="0.0.0.0")
    parser.add_argument('--port', type=int, help='Port to bind to', default=8080)
    parser.add_argument('--baudrate', type=int, help='tty baudrate', default=115200)
    parser.add_argument('--timeout', type=int, help='tty timeout in seconds', default=1)
    parser.add_argument('tty_path', type=str, help='tty input path prefix. Will try to Unix glob all ports of given prefix.')
    config = parser.parse_args()

    print("Loaded config:")
    print(config)

    try:
        asyncio.run(main(config))
    except KeyboardInterrupt:
        print("Received exit, exiting")
        close_serial()