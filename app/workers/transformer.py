from dataclasses import dataclass
from .interfaces import BaseWorker
from app.settings import settings


@dataclass
class Transformer(BaseWorker):
    async def handle(self):
        ...
