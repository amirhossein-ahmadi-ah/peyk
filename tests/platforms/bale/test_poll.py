from __future__ import annotations

import asyncio

from peyk.dispatcher.router import Router, UNHANDLED
from peyk.platforms.bale.models import Message, Poll, PollOption, Update

RAW_POLL = {
    'id': 77,
    'question': 'Tea or coffee?',
    'options': [
        {'persistent_id': 'a1', 'text': 'Tea', 'voter_count': 3},
        {'persistent_id': 'b2', 'text': 'Coffee', 'voter_count': 1},
    ],
    'total_voter_count': 4,
    'is_closed': False,
    'is_anonymous': False,
    'type': 'regular',
    'allows_multiple_answers': True,
    'allows_revoting': True,
    'members_only': False,
}


def test_poll_from_dict_parses_bale_fields() -> None:
    poll = Poll.from_dict(RAW_POLL)
    assert poll is not None
    assert poll.id == 77 and poll.question == 'Tea or coffee?'
    assert poll.options == [PollOption('a1', 'Tea', 3), PollOption('b2', 'Coffee', 1)]
    assert poll.total_voter_count == 4
    assert poll.allows_multiple_answers and poll.allows_revoting
    assert not poll.is_anonymous and not poll.members_only


def test_poll_from_dict_none_and_sparse() -> None:
    assert Poll.from_dict(None) is None
    sparse = Poll.from_dict({'id': 1})
    assert sparse is not None and sparse.options is None and sparse.total_voter_count == 0


def test_message_carries_poll() -> None:
    message = Message.from_dict({'message_id': 5, 'poll': RAW_POLL})
    assert message is not None and message.poll is not None
    assert message.poll.options[0].persistent_id == 'a1'
    assert Message.from_dict({'message_id': 6}).poll is None


def test_update_poll_kind_is_parsed() -> None:
    update = Update.from_dict({'update_id': 9, 'poll': RAW_POLL})
    assert update.poll is not None and update.poll.question == 'Tea or coffee?'
    assert update.message is None


def test_router_poll_observer_fires_for_bale_only_for_poll() -> None:
    router = Router()
    seen: list[Poll] = []

    @router.poll()
    async def on_poll(poll: Poll) -> None:
        seen.append(poll)

    update = Update.from_dict({'update_id': 1, 'poll': RAW_POLL})
    result = asyncio.run(router.propagate_platform_event(update, platform='bale'))
    assert result is not UNHANDLED or seen
    assert len(seen) == 1 and seen[0].id == 77

    plain = Update.from_dict({'update_id': 2, 'message': {'message_id': 1, 'text': 'hi'}})
    seen.clear()
    asyncio.run(router.propagate_platform_event(plain, platform='bale'))
    assert seen == []
