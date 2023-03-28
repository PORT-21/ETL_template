import asyncio
from argparse import ArgumentParser
import sys

from app.workers import Extractor, Transformer, Loader
from app.utils.redis_queue import RedisQueue
from app.settings import settings

parser = ArgumentParser(prog='ETL')
parser.add_argument("worker", choices=["Extractor",
                                       "Transformer",
                                       "Loader"])

if __name__ == "__main__":
    params = sys.argv[1:]
    args = parser.parse_args(params)

    EXTRACTOR_OUT_QUEUE = RedisQueue(
        host=settings.EXTRACTOR_TO_TRANSFORMER_QUERY_HOST,
        queue_name="extractor_out_queue"
    )

    TRANSFORMER_OUT_QUEUE = RedisQueue(
        host=settings.TRANSFORMER_TO_LOADER_QUERY_HOST,
        queue_name="transformer_out_queue"
    )

    WORKERS = [Extractor(OUT_QUEUE=EXTRACTOR_OUT_QUEUE),
               Transformer(IN_QUEUE=EXTRACTOR_OUT_QUEUE,
                           OUT_QUEUE=TRANSFORMER_OUT_QUEUE),
               Loader(IN_QUEUE=TRANSFORMER_OUT_QUEUE)]

    WORKERS = dict(zip([worker.__class__.__name__ for worker in WORKERS],
                       WORKERS))

    worker = WORKERS[args.worker]
    asyncio.run(worker.run())
