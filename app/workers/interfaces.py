from abc import ABCMeta, abstractmethod
import aioredis
from uuid import uuid4
from dataclasses import dataclass, field


class RedisQueue:
    def __init__(self, host: str):
        self.host = host
        self.query = aioredis.from_url(self.host)

    async def pop(self):
        """
        Достаёт первое значение и удаляет его
        """
        key = await self.query.lpop()
        return key

    async def publish(self, value) -> None:
        """
        Кладёт новые данные в очередь
        """
        await self.query.lpush(str(uuid4()), value)


@dataclass
class BaseWorker(metaclass=ABCMeta):
    """
    Args:
        IN_QUEUE_HOST(str) - хост очереди из которой берём данные

        OUT_QUEUE_HOST(str) - хост очереди в которую кладём результаты
    """
    OUT_QUEUE_HOST: str = field(default_factory=str)
    IN_QUEUE_HOST: str = field(default_factory=str)
    # Очередь на входяхие сообщения
    IN_QUEUE: RedisQueue | None = field(init=False, default=None)
    # Очередь на исходящие сообщения
    OUT_QUEUE: RedisQueue | None = field(init=False, default=None)

    def __post_init__(self):
        self.init_queries()

    def init_queries(self):
        """
        Инициализирует очереди для воркера в зависимости от праметров
        """
        for obj_name, host in dict(OUT_QUEUE=self.OUT_QUEUE_HOST,
                                   IN_QUEUE=self.IN_QUEUE_HOST).items():
            if host:
                setattr(self, obj_name, RedisQueue(host))

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
        обёртка над методом handle. Пропихивает в 
        так лучше, чем использовать декоратор. Этот метод вызывается celery
        """
        if self.IN_QUEUE:
            data = self.IN_QUEUE.pop()
            await self.handle(data)
