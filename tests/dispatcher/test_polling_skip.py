import asyncio
from types import SimpleNamespace as NS
from peyk.dispatcher.polling import prepare_polling


class FakeClient:
    def __init__(self, ids):
        self.queue = [NS(update_id=i) for i in ids]
        self.calls = []

    async def get_webhook_info(self):
        return NS(url='')

    async def delete_webhook(self, **kw):
        self.calls.append(('delete_webhook', kw))

    async def get_updates(self, *, offset=None, limit=None, timeout=None):
        self.calls.append(('get_updates', offset))
        if offset is not None:
            if offset < 0:
                end_slice = self.queue[offset:]
                return end_slice[:limit] if limit else end_slice
            self.queue = [u for u in self.queue if u.update_id >= offset]
        return self.queue[:limit]


def run(platform, skip, ids):
    bot = NS(platform=platform, client=FakeClient(ids))
    asyncio.run(prepare_polling(bot, skip_updates=skip))
    return bot.client


def test_bale_skip_drains_queue():
    c = run('bale', True, range(1, 251))
    assert c.queue == []
    get_updates_calls = [args for name, args in c.calls if name == 'get_updates']
    assert len(get_updates_calls) <= 3


def test_bale_skip_drains_large_backlog_in_few_calls():
    c = run('bale', True, range(1, 10001))
    assert c.queue == []
    get_updates_calls = [args for name, args in c.calls if name == 'get_updates']
    assert len(get_updates_calls) <= 3

def test_bale_no_skip_keeps_queue():
    c = run('bale', False, range(1, 11))
    assert len(c.queue) == 10

def test_telegram_unchanged():
    c = run('telegram', True, range(1, 11))
    assert ('delete_webhook', {'drop_pending_updates': True}) in c.calls
    assert not any(name == 'get_updates' for name, *_ in c.calls)