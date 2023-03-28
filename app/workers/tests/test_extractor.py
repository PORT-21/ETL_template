from asyncio import sleep
import pytest
import json
from app.workers.interfaces import RedisQueue, BaseWorker


def test_extractor_alive(extractor):
    assert extractor and \
           extractor.OUT_QUEUE and \
           type(extractor.OUT_QUEUE) is RedisQueue


@pytest.mark.asyncio
async def test_task_extractor_to_transformer(extractor: BaseWorker,
                                             transformer: BaseWorker):
    data = dict(value=10)
    await extractor.OUT_QUEUE.publish(value=json.dumps(data))
    await sleep(1)
    recieved_value = await transformer.IN_QUEUE.pop()
    assert data == json.loads(recieved_value)
