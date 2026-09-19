from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def set_webhook(self, url: str, *, max_connections: Optional[int]=None, allowed_updates: Optional[List[str]]=None, drop_pending_updates: Optional[bool]=None, secret_token: Optional[str]=None) -> bool:
    """Use this method to specify a URL and receive incoming updates via an outgoing webhook. Whenever there is an update for the bot, we will send an HTTPS POST request to the specified URL, containing a JSON-serialized Update. In case of an unsuccessful request (a request with response HTTP status code different from 2XY), we will repeat the request and give up after a reasonable amount of attempts. Returns True on success.
If you'd like to make sure that the webhook was set by you, you can specify secret data in the parameter secret_token. If specified, the request will contain a header 'X-Telegram-Bot-Api-Secret-Token' with the secret token as content.
Notes
1. You will not be able to receive updates using getUpdates for as long as an outgoing webhook is set up.
2. To use a self-signed certificate, you need to upload your public key certificate using certificate parameter. Please upload as InputFile, sending a String will not work.
3. Ports currently supported for webhooks: 443, 80, 88, 8443.
If you're having any trouble setting up webhooks, please check out this amazing guide to webhooks.

Args:
    url: HTTPS URL to send updates to. Use an empty string to remove webhook integration.
    max_connections: The maximum allowed number of simultaneous HTTPS connections to the webhook for update delivery, 1-100. Defaults to 40. Use lower values to limit the load on your bot's server, and higher values to increase your bot's throughput.
    allowed_updates: A JSON-serialized list of the update types you want your bot to receive. For example, specify ["message", "edited_channel_post", "callback_query"] to only receive updates of these types. See Update for a complete list of available update types. Specify an empty list to receive all update types except chat_member, message_reaction, and message_reaction_count (default). If not specified, the previous setting will be used.
Please note that this parameter doesn't affect updates created before the call to the setWebhook, so unwanted updates may be received for a short period of time.
    drop_pending_updates: Pass True to drop all pending updates
    secret_token: A secret token to be sent in a header 'X-Telegram-Bot-Api-Secret-Token' in every webhook request, 1-256 characters. Only characters A-Z, a-z, 0-9, _ and - are allowed. The header is useful to ensure that the request comes from a webhook set by you.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'url': url}
    if max_connections is not None:
        payload['max_connections'] = max_connections
    if allowed_updates is not None:
        payload['allowed_updates'] = allowed_updates
    if drop_pending_updates is not None:
        payload['drop_pending_updates'] = drop_pending_updates
    if secret_token is not None:
        payload['secret_token'] = secret_token
    return bool(await self._call('setWebhook', json_body=payload))
