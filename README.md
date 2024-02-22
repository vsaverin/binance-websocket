# Binance Async WebSocket Client (for learning purposes)

## Overview

This Python code provides an asynchronous WebSocket client for interacting with Binance's WebSocket API to stream candlestick chart data. The code connects to Binance's WebSocket server, retrieves real-time candlestick data, and writes the data to a ClickHouse database.

## Files

1. **binance_client.py**
    - The main module containing the `BinanceAsyncWebSocket` class, responsible for handling the WebSocket connection and processing incoming candlestick data.
    - Utilizes the `websockets` library for asynchronous communication and `json` for handling JSON data.
    - The class has methods for connecting to the WebSocket, handling incoming messages, and starting the WebSocket client.

2. **database.py**
    - Contains the `ClickHouseWriter` class, which handles writing candlestick data to a ClickHouse database.
    - Uses the `clickhouse_driver` library for interacting with ClickHouse.
    - The `write_data` method constructs an SQL query to insert candlestick data into the specified table and executes the query.

## Usage

1. Import the necessary modules:

    ```python
    from binance_client import BinanceAsyncWebSocket
    ```

2. Create an instance of the `BinanceAsyncWebSocket` class, providing the symbol (e.g., "BTCUSDT") and optional interval (default is "1m"):

    ```python
    binance_ws = BinanceAsyncWebSocket(symbol="btcusdt", interval="1m")
    ```

3. Start the WebSocket client:

    ```python
    await binance_ws.start()
    ```

## Dependencies

- **websockets**: Handles asynchronous WebSocket communication.
- **json**: Parses JSON data.

## Configuration

- Adjust the WebSocket server URL (`base_url`) and ClickHouse connection details in the respective classes according to your environment.

## Requirements

- Python 3.7+
- `websockets` library (`pip install websockets`)
- `clickhouse-driver` library (`pip install clickhouse-driver`)

## Note

- Ensure that you have a ClickHouse server running and the necessary table (specified in the `INSERT INTO` query) created in your ClickHouse database.

## Disclaimer

This code is a basic example and may require further customization based on specific use cases and security considerations. Use it at your own discretion and responsibility.