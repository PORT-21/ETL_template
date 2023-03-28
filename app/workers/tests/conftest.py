from app.utils.redis_queue import RedisQueue
from app.workers import Extractor, Transformer, Loader
import pytest


@pytest.fixture
def extractor_out_queue():
    queue = RedisQueue(host="redis://127.0.0.1:6379",
                       queue_name="extractor_out_queue")
    return queue


@pytest.fixture
def transformer_out_queue():
    queue = RedisQueue(host="redis://127.0.0.1:6379",
                       queue_name="transformer_out_queue")
    return queue


@pytest.fixture
def extractor(extractor_out_queue):
    extractor = Extractor(OUT_QUEUE=extractor_out_queue)
    return extractor


@pytest.fixture
def transformer(transformer_out_queue, extractor_out_queue):
    transformer = Transformer(IN_QUEUE=extractor_out_queue,
                              OUT_QUEUE=transformer_out_queue)
    return transformer


@pytest.fixture
def loader(transformer_out_queue_host):
    loader = Loader(IN_QUEUE=transformer_out_queue)
    return loader
