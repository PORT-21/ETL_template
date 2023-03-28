from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field

from .redis_queue import RedisQueue


@dataclass
class BaseWorker(metaclass=ABCMeta):
    """
    Args:
        IN_QUEUE(str) - очередь из которой берём данные

        OUT_QUEUE(str) - очередь в которую кладём результаты
    """
    # Очередь на входяхие сообщения
    IN_QUEUE: RedisQueue | None = field(default=None)
    # Очередь на исходящие сообщения
    OUT_QUEUE: RedisQueue | None = field(default=None)

    @abstractmethod
    async def handle(self):
        """
        Метод обработки, вызывается из celery
        """
        raise NotImplementedError(
            f"определите метод handle у {self.__class__.__name__}"
        )

    async def _handle(self):
        """
        Обёртка над методом handle. Пропихивает в 
        так лучше, чем использовать декоратор. Этот метод вызывается celery
        """
        if self.IN_QUEUE:
            data = await self.IN_QUEUE.pop()
            await self.handle(data)

    async def run(self):
        while True:
            await self._handle()
