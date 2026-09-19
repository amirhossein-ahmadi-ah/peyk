from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]
from ._serialization import _serialize_entities, _serialize_reply_parameters, _serialize_link_preview

async def send_poll(self, chat_id: ChatId, question: str, options: Sequence[Union[str, InputPollOption]], *, message_thread_id: Optional[int]=None, question_parse_mode: Optional[str]=None, question_entities: Optional[EntitiesInput]=None, is_anonymous: Optional[bool]=None, type: Optional[str]=None, allows_multiple_answers: Optional[bool]=None, allows_revoting: Optional[bool]=None, shuffle_options: Optional[bool]=None, allow_adding_options: Optional[bool]=None, hide_results_until_closes: Optional[bool]=None, members_only: Optional[bool]=None, country_codes: Optional[Sequence[str]]=None, correct_option_ids: Optional[Sequence[int]]=None, explanation: Optional[str]=None, explanation_parse_mode: Optional[str]=None, explanation_entities: Optional[EntitiesInput]=None, explanation_media: Optional[Union[InputPollMedia, Mapping[str, object]]]=None, open_period: Optional[int]=None, close_date: Optional[int]=None, is_closed: Optional[bool]=None, description: Optional[str]=None, description_parse_mode: Optional[str]=None, description_entities: Optional[EntitiesInput]=None, media: Optional[Union[InputPollMedia, Mapping[str, object]]]=None, disable_notification: Optional[bool]=None, protect_content: Optional[bool]=None, reply_parameters: Optional[Union[ReplyParameters, Mapping[str, object]]]=None, reply_markup: Optional[ReplyMarkup]=None) -> Message:
    """Use this method to send a native poll. On success, the sent Message is returned.

Args:
    chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username. Polls can't be sent to channel direct messages chats.
    question: Poll question, 1-300 characters
    options: A JSON-serialized list of 1-12 answer options
    message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
    question_parse_mode: Mode for parsing entities in the question. See formatting options for more details. Currently, only custom emoji entities are allowed.
    question_entities: A JSON-serialized list of special entities that appear in the poll question. It can be specified instead of question_parse_mode.
    is_anonymous: True, if the poll needs to be anonymous, defaults to True
    type: Poll type, 'quiz' or 'regular', defaults to 'regular'
    allows_multiple_answers: Pass True if the poll allows multiple answers, defaults to False
    allows_revoting: Pass True if the poll allows to change chosen answer options, defaults to False for quizzes and to True for regular polls
    shuffle_options: Pass True if the poll options must be shown in random order
    allow_adding_options: Pass True if answer options can be added to the poll after creation; not supported for anonymous polls and quizzes
    hide_results_until_closes: Pass True if poll results must be shown only after the poll closes
    members_only: Pass True if voting is limited to users who have been members of the chat where the poll is being sent for more than 24 hours; for channel chats only
    country_codes: A JSON-serialized list of 0-12 two-letter ISO 3166-1 alpha-2 country codes indicating the countries from which users can vote in the poll; for channel chats only. Use 'FT' as a country code to allow users with anonymous numbers to vote. If omitted or empty, then users from any country can participate in the poll.
    correct_option_ids: A JSON-serialized list of monotonically increasing 0-based identifiers of the correct answer options, required for polls in quiz mode
    explanation: Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style poll, 0-200 characters with at most 2 line feeds after entities parsing
    explanation_parse_mode: Mode for parsing entities in the explanation. See formatting options for more details.
    explanation_entities: A JSON-serialized list of special entities that appear in the poll explanation. It can be specified instead of explanation_parse_mode.
    explanation_media: Media added to the quiz explanation
    open_period: Amount of time in seconds the poll will be active after creation, 5-2628000. Can't be used together with close_date.
    close_date: Point in time (Unix timestamp) when the poll will be automatically closed. Must be at least 5 and no more than 2628000 seconds in the future. Can't be used together with open_period.
    is_closed: Pass True if the poll needs to be immediately closed. This can be useful for poll preview.
    description: Description of the poll to be sent, 0-1024 characters after entities parsing
    description_parse_mode: Mode for parsing entities in the poll description. See formatting options for more details.
    description_entities: A JSON-serialized list of special entities that appear in the poll description, which can be specified instead of description_parse_mode
    media: Media added to the poll description
    disable_notification: Sends the message silently. Users will receive a notification with no sound.
    protect_content: Protects the contents of the sent message from forwarding and saving
    reply_parameters: Description of the message to reply to
    reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.

Returns:
    Message: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'chat_id': chat_id, 'question': question, 'options': [{'text': o} if isinstance(o, str) else o.to_dict() for o in options]}
    if question_parse_mode is not None:
        payload['question_parse_mode'] = question_parse_mode
    serialized_q = _serialize_entities(question_entities)
    if serialized_q is not None:
        payload['question_entities'] = serialized_q
    if is_anonymous is not None:
        payload['is_anonymous'] = is_anonymous
    if type is not None:
        payload['type'] = type
    if allows_multiple_answers is not None:
        payload['allows_multiple_answers'] = allows_multiple_answers
    if allows_revoting is not None:
        payload['allows_revoting'] = allows_revoting
    if shuffle_options is not None:
        payload['shuffle_options'] = shuffle_options
    if allow_adding_options is not None:
        payload['allow_adding_options'] = allow_adding_options
    if hide_results_until_closes is not None:
        payload['hide_results_until_closes'] = hide_results_until_closes
    if members_only is not None:
        payload['members_only'] = members_only
    if country_codes is not None:
        payload['country_codes'] = list(country_codes)
    if correct_option_ids is not None:
        payload['correct_option_ids'] = list(correct_option_ids)
    if explanation is not None:
        payload['explanation'] = explanation
    if explanation_parse_mode is not None:
        payload['explanation_parse_mode'] = explanation_parse_mode
    serialized_e = _serialize_entities(explanation_entities)
    if serialized_e is not None:
        payload['explanation_entities'] = serialized_e
    serialized_em = self._serialize_poll_media(explanation_media)
    if serialized_em is not None:
        payload['explanation_media'] = serialized_em
    if open_period is not None:
        payload['open_period'] = open_period
    if close_date is not None:
        payload['close_date'] = close_date
    if is_closed is not None:
        payload['is_closed'] = is_closed
    if description is not None:
        payload['description'] = description
    if description_parse_mode is not None:
        payload['description_parse_mode'] = description_parse_mode
    serialized_d = _serialize_entities(description_entities)
    if serialized_d is not None:
        payload['description_entities'] = serialized_d
    serialized_m = self._serialize_poll_media(media)
    if serialized_m is not None:
        payload['media'] = serialized_m
    self._apply_send_options_json(payload, message_thread_id=message_thread_id, disable_notification=disable_notification, protect_content=protect_content, reply_parameters=reply_parameters, reply_markup=reply_markup)
    result = await self._call('sendPoll', json_body=payload)
    return Message.from_dict(result)
