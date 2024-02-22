import os

from clickhouse_driver import Client


class ClickHouseWriter:
    def __init__(self):
        self.clickhouse_client = Client(
            host=os.environ.get("CLICK_HOST"),
            port=os.environ.get("CLICK_PORT"),
            user=os.environ.get("CLICK_USER"),
            password=os.environ.get("CLICK_PASSWORD"),
            database=os.environ.get("CLICK_DATABASE"),
        )

    async def write_data(self, data):
        query = (
            f"INSERT INTO your_table "
            f"(Symbol, Time, Open, High, Low, Close) "
            f"VALUES "
            f"('{data['Symbol']}', {data['Time']}, {data['Open']}, "
            f"{data['High']}, {data['Low']}, {data['Close']})"
        )

        await self.execute_query(query)

    async def execute_query(self, query):
        await self.clickhouse_client.execute(query)
