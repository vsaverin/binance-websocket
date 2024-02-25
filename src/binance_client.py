import websockets
import json

from database import ClickHouseWriter


class BinanceAsyncWebSocket:
    def __init__(self):
        self.base_url = "wss://stream.binance.com:9443/ws/"
        self.uri = None
        self.connection = None
        self.database = ClickHouseWriter()

    def _parse_kline(self, symbol: str, kline: dict) -> dict:
        return {
            "Symbol": symbol,
            "Time": kline.get("t"),
            "Open": kline.get("o"),
            "High": kline.get("h"),
            "Low": kline.get("l"),
            "Close": kline.get("c"),
        }

    async def on_message(self, symbol: str, message: str) -> None:
        data = json.loads(message)
        if data.get("error"):
            return
        kline = data.get("k")
        if not kline:
            return
        data = self._parse_kline(symbol, kline)
        try:
            await self.database.write_data(data)
        except Exception:
            return

    async def connect(self, symbol: str, interval: str) -> None:
        self.uri = self.base_url + symbol.lower() + "@kline_" + interval
        self.connection = await websockets.connect(self.uri)
        request = {"method": "SUBSCRIBE", "params": [symbol], "id": 1}
        await self.connection.send(json.dumps(request))

    async def start(self, symbol: str, interval: str) -> None:
        await self.connect(symbol, interval)
        while True:
            message = await self.connection.recv()
            await self.on_message(symbol, message)
