from app.workers.interfaces import RedisQueue


def test_extractor_alive(extractor):
    assert extractor and \
           extractor.OUT_QUEUE and \
           extractor.OUT_QUEUE is RedisQueue
