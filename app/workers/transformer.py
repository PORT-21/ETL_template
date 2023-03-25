from dataclasses import dataclass
import aioredis

from .interfaces import BaseWorker
from app.settings import settings


@dataclass
class Transformer(BaseWorker):
    @property
    def in_query(self):
        in_query = aioredis.from_url("redis://localhost")
        return in_query

    async def handle(self):
        ...
