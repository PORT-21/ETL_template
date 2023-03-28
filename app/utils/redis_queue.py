from abc import ABCMeta, abstractmethod
import aioredis
from dataclasses import dataclass, field


class RedisQueue:
    def __init__(self, host: str, queue_name: str):
        self.queue_name = queue_name
        self.host = host
        self.query = aioredis.from_url(self.host)

    async def pop(self):
        """
        Достаёт первое значение и удаляет его
        """
        key = await self.query.lpop(self.queue_name)
        return key.decode()

    async def publish(self, value) -> None:
        """
        Кладёт новые данные в очередь
        """
        await self.query.lpush(self.queue_name, value)
