"""
Unit тесты для клиента Deribit
"""
import pytest
from unittest.mock import AsyncMock, patch
from deribit_task.deribit_client import DeribitClient


@pytest.mark.asyncio
async def test_get_btc_price_success():
    """Тест успешного получения цены BTC"""
    mock_response_data = {
        'result': {
            'index_price': 50000.5,
            'index_name': 'BTC_USD'
        }
    }
    
    async with DeribitClient() as client:
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value=mock_response_data)
            mock_get.return_value.__aenter__.return_value = mock_response
            
            result = await client.get_btc_price()
            
            assert result is not None
            assert result['index_price'] == 50000.5


@pytest.mark.asyncio
async def test_get_eth_price_success():
    """Тест успешного получения цены ETH"""
    mock_response_data = {
        'result': {
            'index_price': 3000.25,
            'index_name': 'ETH_USD'
        }
    }
    
    async with DeribitClient() as client:
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value=mock_response_data)
            mock_get.return_value.__aenter__.return_value = mock_response
            
            result = await client.get_eth_price()
            
            assert result is not None
            assert result['index_price'] == 3000.25


@pytest.mark.asyncio
async def test_get_index_price_error():
    """Тест обработки ошибки при получении цены"""
    async with DeribitClient() as client:
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = AsyncMock()
            mock_response.status = 500
            mock_get.return_value.__aenter__.return_value = mock_response
            
            result = await client.get_btc_price()
            
            assert result is None
