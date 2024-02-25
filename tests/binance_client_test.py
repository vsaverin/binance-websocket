import pytest
from unittest.mock import AsyncMock, patch
from websockets import WebSocketClientProtocol
from src.binance_client import BinanceAsyncWebSocket


@pytest.mark.asyncio
async def test_parse_kline():
    binance_ws = BinanceAsyncWebSocket()
    symbol = "BTCUSDT"
    interval = "1m"
    kline_data = {
        "t": 1645635912345,
        "o": 40000.0,
        "h": 40500.0,
        "l": 39800.0,
        "c": 40250.0,
    }
    expected_result = {
        "Symbol": f"{symbol.lower()}@kline_{interval}",
        "Time": 1645635912345,
        "Open": 40000.0,
        "High": 40500.0,
        "Low": 39800.0,
        "Close": 40250.0,
    }
    result = binance_ws._parse_kline(symbol, interval, kline_data)
    assert result == expected_result


@pytest.mark.asyncio
async def test_on_message_error():
    binance_ws = BinanceAsyncWebSocket()
    symbol = "BTCUSDT"
    interval = "1m"
    message_with_error = '{"error": "Some error message"}'
    with patch.object(
        binance_ws.database, "write_data", new_callable=AsyncMock
    ) as mock_write_data:
        await binance_ws.on_message(symbol, interval, message_with_error)
        mock_write_data.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_no_kline():
    binance_ws = BinanceAsyncWebSocket()
    symbol = "BTCUSDT"
    interval = "1m"
    message_without_kline = '{"some_key": "some_value"}'
    with patch.object(
        binance_ws.database, "write_data", new_callable=AsyncMock
    ) as mock_write_data:
        await binance_ws.on_message(symbol, interval, message_without_kline)
        mock_write_data.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_successful_write():
    binance_ws = BinanceAsyncWebSocket()
    symbol = "BTCUSDT"
    interval = "1m"
    valid_kline_message = (
        '{"k": {'
        '"t": 1645635912345, '
        '"o": 40000.0, '
        '"h": 40500.0, '
        '"l": 39800.0, '
        '"c": 40250.0}}'
    )
    with patch.object(
        binance_ws.database, "write_data", new_callable=AsyncMock
    ) as mock_write_data:
        await binance_ws.on_message(symbol, interval, valid_kline_message)
        mock_write_data.assert_called_once()


@pytest.mark.asyncio
async def test_connect():
    binance_ws = BinanceAsyncWebSocket()
    symbol = "BTCUSDT"
    interval = "1m"
    with patch("websockets.connect") as mock_connect:
        mock_connection = AsyncMock(spec=WebSocketClientProtocol)
        mock_connect.return_value = mock_connection

        await binance_ws.connect(symbol, interval)

        mock_connect.assert_called_once_with(
            binance_ws.base_url + f"{symbol.lower()}@kline_{interval}"
        )
        mock_connection.send.assert_called_once_with(
            f'{{"method": "SUBSCRIBE", '
            f'"params": ["{symbol.lower()}@kline_{interval}"], "id": 1}}'
        )


@pytest.mark.asyncio
async def test_start():
    binance_ws = BinanceAsyncWebSocket()
    symbol = "BTCUSDT"
    interval = "1m"
    with patch.object(
        binance_ws, "connect", new_callable=AsyncMock
    ) as mock_connect, patch.object(
        binance_ws.connection, "recv", new_callable=AsyncMock
    ) as mock_recv, patch.object(
        binance_ws, "on_message", new_callable=AsyncMock
    ) as mock_on_message:
        await binance_ws.start(symbol, interval)

        mock_connect.assert_called_once_with(symbol, interval)
        mock_recv.assert_called()
        mock_on_message.assert_called()
