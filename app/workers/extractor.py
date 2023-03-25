from .interfaces import BaseWorker
from app import settings


class Extractor(BaseWorker):
    async def handle(self):
        ...
