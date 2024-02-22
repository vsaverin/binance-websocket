from clickhouse_driver import Client


class ClickHouseWriter:
    def __init__(self):
        self.clickhouse_client = Client(
            host="clickhouse-server",
            port=9000,
            user="main",
            password="localpassword",
            database="localpassword",
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
