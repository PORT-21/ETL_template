from .interfaces import BaseWorker


class Loader(BaseWorker):
    async def handle(self):
        ...
