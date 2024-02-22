import asyncio
from time import sleep

from binance_client import BinanceAsyncWebSocket


if __name__ == "__main__":
    SYMBOL = "btcusdt"
    INTERVAL = "1m"
    binance_ws = BinanceAsyncWebSocket(SYMBOL, INTERVAL)

    async def run():
        await binance_ws.start()

    sleep(5) # waiting dev clickhouse init
    asyncio.run(run())
