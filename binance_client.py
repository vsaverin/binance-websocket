import websockets
import json

from database import ClickHouseWriter


class BinanceAsyncWebSocket:
    def __init__(self, symbol, interval="1m", candlestick_chart=None):
        self.base_url = "wss://stream.binance.com:9443/ws/"
        self.symbol = symbol.lower() + "@kline_" + interval
        self.uri = self.base_url + self.symbol
        self.candlestick_chart = candlestick_chart
        self.connection = None
        self.database = ClickHouseWriter()

    async def on_message(self, message):
        data = json.loads(message)
        if data.get("error"):
            return
        kline = data.get("k")
        if not kline:
            return
        data = {
            "Symbol": self.symbol,
            "Time": kline.get("t"),
            "Open": kline.get("o"),
            "High": kline.get("h"),
            "Low": kline.get("l"),
            "Close": kline.get("c"),
        }
        await self.database.write_data(data)

    async def connect(self):
        self.connection = await websockets.connect(self.uri)
        request = {"method": "SUBSCRIBE", "params": [self.symbol], "id": 1}
        await self.connection.send(json.dumps(request))

    async def start(self):
        await self.connect()
        while True:
            message = await self.connection.recv()
            await self.on_message(message)
