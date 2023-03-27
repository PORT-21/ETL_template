from app.workers import Extractor, Transformer, Loader
import pytest


@pytest.fixture
def extractor_out_queue_host():
    return "redis://0.0.0.0:6379"

@pytest.fixture
def transformer_out_queue_host():
    return "redis://0.0.0.0:6380"


@pytest.fixture
def extractor(extractor_out_queue_host):
    extractor = Extractor(OUT_QUEUE_HOST=extractor_out_queue_host)
    return extractor


@pytest.fixture
def transformer(transformer_out_queue_host, extractor_out_queue_host):
    transformer = Transformer(IN_QUEUE_HOST=extractor_out_queue_host,
                              OUT_QUEUE_HOST=transformer_out_queue_host)
    return transformer


@pytest.fixture
def loader(transformer_out_queue_host):
    loader = Loader(IN_QUEUE_HOST=transformer_out_queue_host)
    return loader
