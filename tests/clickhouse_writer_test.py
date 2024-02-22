import pytest
from unittest.mock import AsyncMock
from src.database import ClickHouseWriter


@pytest.fixture
def clickhouse_writer():
    return ClickHouseWriter()


@pytest.fixture
def mock_clickhouse_client(monkeypatch):
    async def mock_execute(self, query):
        pass

    monkeypatch.setattr(
        ClickHouseWriter, "execute_query", AsyncMock(
            side_effect=mock_execute)
    )
    return ClickHouseWriter()


@pytest.mark.asyncio
async def test_write_data_valid_data(clickhouse_writer):
    data = {
        "Symbol": "BTC",
        "Time": "timestamp",
        "Open": 100.0,
        "High": 110.0,
        "Low": 90.0,
        "Close": 105.0,
    }
    await clickhouse_writer.write_data(data)


@pytest.mark.asyncio
async def test_write_data_invalid_data(clickhouse_writer):
    data = {"InvalidKey": "value"}
    await clickhouse_writer.write_data(data)


@pytest.mark.asyncio
async def test_execute_query(mock_clickhouse_client):
    query = (
        "INSERT INTO btc_data ("
        "Symbol, Time, Open, High, Low, Close"
        ") VALUES ("
        "'BTC', 123456789, 100.0, 110.0, 90.0, 105.0)"
    )
    await mock_clickhouse_client.execute_query(query)
