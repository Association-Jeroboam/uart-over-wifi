# uart-over-wifi
## Dependencies
### Poetry
```curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -```

## Installation
```poetry install```

## Usage
### Server
```poetry run python uart_over_wifi/server.py /dev/ttyACM```

### Client
```poetry run python uart_over_wifi/client.py /tmp/ttyACM0```