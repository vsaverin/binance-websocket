import websockets
import json

from database import ClickHouseWriter


class BinanceAsyncWebSocket:
    def __init__(self, symbol: str, interval: str = "1m"):
        self.base_url = "wss://stream.binance.com:9443/ws/"
        self.symbol = symbol.lower() + "@kline_" + interval
        self.uri = self.base_url + self.symbol
        self.connection = None
        self.database = ClickHouseWriter()

    def _parse_kline(self, kline: dict) -> dict:
        return {
            "Symbol": self.symbol,
            "Time": kline.get("t"),
            "Open": kline.get("o"),
            "High": kline.get("h"),
            "Low": kline.get("l"),
            "Close": kline.get("c"),
        }

    async def on_message(self, message: str) -> None:
        data = json.loads(message)
        if data.get("error"):
            return
        kline = data.get("k")
        if not kline:
            return
        data = self._parse_kline(kline)
        await self.database.write_data(data)

    async def connect(self) -> None:
        self.connection = await websockets.connect(self.uri)
        request = {"method": "SUBSCRIBE", "params": [self.symbol], "id": 1}
        await self.connection.send(json.dumps(request))

    async def start(self) -> None:
        await self.connect()
        while True:
            message = await self.connection.recv()
            await self.on_message(message)
