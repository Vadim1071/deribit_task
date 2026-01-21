"""
Клиент для работы с API криптобиржи Deribit
"""
import aiohttp
from typing import Dict, Optional
import logging

from deribit_task.config import DERIBIT_API_URL

logger = logging.getLogger(__name__)


class DeribitClient:
    """
    Клиент для получения данных с биржи Deribit
    """

    def __init__(self, base_url: str = DERIBIT_API_URL):
        """
        Инициализация клиента
        
        :param base_url: Базовый URL API Deribit
        """
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """
        Асинхронный контекстный менеджер - вход
        """
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Асинхронный контекстный менеджер - выход
        """
        if self.session:
            await self.session.close()

    async def get_index_price(self, currency: str) -> Optional[Dict]:
        """
        Получает индексную цену валюты
        
        :param currency: Валюта (BTC или ETH)
        :return: Словарь с данными о цене или None в случае ошибки
        """
        if not self.session:
            self.session = aiohttp.ClientSession()

        try:
            url = f"{self.base_url}/public/get_index_price"
            params = {"index_name": f"{currency}_USD"}
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('result'):
                        return data['result']
                    else:
                        logger.error(f"Ошибка получения цены для {currency}: {data}")
                        return None
                else:
                    logger.error(f"HTTP ошибка {response.status} при получении цены для {currency}")
                    return None
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка клиента при получении цены для {currency}: {e}")
            return None
        except Exception as e:
            logger.error(f"Неожиданная ошибка при получении цены для {currency}: {e}")
            return None

    async def get_btc_price(self) -> Optional[Dict]:
        """
        Получает индексную цену BTC/USD
        
        :return: Словарь с данными о цене BTC
        """
        return await self.get_index_price("BTC")

    async def get_eth_price(self) -> Optional[Dict]:
        """
        Получает индексную цену ETH/USD
        
        :return: Словарь с данными о цене ETH
        """
        return await self.get_index_price("ETH")
