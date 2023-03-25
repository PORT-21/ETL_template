from abc import ABCMeta, abstractmethod


class BaseWorker(metaclass=ABCMeta):
    @abstractmethod
    async def handle(self):
        """
        Метод обработки, вызывается из celery
        """
        raise NotImplementedError(
            f"определите метод handle у {self.__class__.__name__}"
        )
