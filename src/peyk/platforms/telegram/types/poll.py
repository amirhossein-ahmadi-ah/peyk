from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .message_entity import MessageEntity
from .poll_media import PollMedia
from .poll_option import PollOption

@dataclass
class Poll:
    """This object contains information about a poll.

Attributes:
    id: Unique poll identifier
    question: Poll question, 1-300 characters
    options: List of poll options
    total_voter_count: Total number of users that voted in the poll
    is_closed: True, if the poll is closed
    is_anonymous: True, if the poll is anonymous
    type: Poll type, currently can be 'regular' or 'quiz'
    allows_multiple_answers: True, if the poll allows multiple answers
    allows_revoting: True, if the poll allows to change the chosen answer options
    members_only: True if voting is limited to users who have been members of the chat where the poll was originally sent for more than 24 hours
    question_entities: Special entities that appear in the question. Currently, only custom emoji entities are allowed in poll questions
    country_codes: A list of two-letter ISO 3166-1 alpha-2 country codes indicating the countries from which users can vote in the poll. The country code 'FT' is used for users with anonymous numbers. If omitted, then users from any country can participate in the poll.
    correct_option_ids: Array of 0-based identifiers of the correct answer options. Available only for polls in quiz mode which are closed or were sent (not forwarded) by the bot or to the private chat with the bot.
    explanation: Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style poll, 0-200 characters
    explanation_entities: Special entities like usernames, URLs, bot commands, etc. that appear in the explanation
    explanation_media: Media added to the quiz explanation
    open_period: Amount of time in seconds the poll will be active after creation
    close_date: Point in time (Unix timestamp) when the poll will be automatically closed
    description: Description of the poll; for polls inside the Message object only
    description_entities: Special entities like usernames, URLs, bot commands, etc. that appear in the description
    media: Media added to the poll description; for polls inside the Message object only
    correct_option_id: 0-based identifier of the correct answer option. Available only for polls in the quiz mode, which are closed, or was sent (not forwarded) by the bot or to the private chat with the bot."""
    id: str
    question: str
    options: List[PollOption]
    total_voter_count: int = 0
    is_closed: bool = False
    is_anonymous: bool = True
    type: str = 'regular'
    allows_multiple_answers: bool = False
    allows_revoting: bool = False
    members_only: Optional[bool] = None
    country_codes: Optional[List[str]] = None
    question_entities: Optional[List[MessageEntity]] = None
    correct_option_ids: Optional[List[int]] = None
    explanation: Optional[str] = None
    explanation_entities: Optional[List[MessageEntity]] = None
    explanation_media: Optional[PollMedia] = None
    open_period: Optional[int] = None
    close_date: Optional[int] = None
    description: Optional[str] = None
    description_entities: Optional[List[MessageEntity]] = None
    media: Optional[PollMedia] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Poll']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(id=data.get('id', ''), question=data.get('question', ''), options=[o for o in (PollOption.from_dict(item) for item in data.get('options', [])) if o is not None], total_voter_count=data.get('total_voter_count', 0), is_closed=data.get('is_closed', False), is_anonymous=data.get('is_anonymous', True), type=data.get('type', 'regular'), allows_multiple_answers=data.get('allows_multiple_answers', False), allows_revoting=data.get('allows_revoting', False), members_only=data.get('members_only'), country_codes=data.get('country_codes'), question_entities=MessageEntity.list_from(data.get('question_entities')), correct_option_ids=data.get('correct_option_ids'), explanation=data.get('explanation'), explanation_entities=MessageEntity.list_from(data.get('explanation_entities')), explanation_media=PollMedia.from_dict(data.get('explanation_media')), open_period=data.get('open_period'), close_date=data.get('close_date'), description=data.get('description'), description_entities=MessageEntity.list_from(data.get('description_entities')), media=PollMedia.from_dict(data.get('media')))
