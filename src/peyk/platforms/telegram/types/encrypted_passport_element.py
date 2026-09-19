from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class EncryptedPassportElement:
    """Describes documents or other Telegram Passport elements shared with the bot by the user.

Attributes:
    type: Element type. One of 'personal_details', 'passport', 'driver_license', 'identity_card', 'internal_passport', 'address', 'utility_bill', 'bank_statement', 'rental_agreement', 'passport_registration', 'temporary_registration', 'phone_number', 'email'.
    hash: Base64-encoded element hash for using in PassportElementErrorUnspecified
    data: Base64-encoded encrypted Telegram Passport element data provided by the user; available only for 'personal_details', 'passport', 'driver_license', 'identity_card', 'internal_passport' and 'address' types. Can be decrypted and verified using the accompanying EncryptedCredentials.
    phone_number: User's verified phone number; available only for 'phone_number' type
    email: User's verified email address; available only for 'email' type
    files: Array of encrypted files with documents provided by the user; available only for 'utility_bill', 'bank_statement', 'rental_agreement', 'passport_registration' and 'temporary_registration' types. Files can be decrypted and verified using the accompanying EncryptedCredentials.
    front_side: Encrypted file with the front side of the document, provided by the user; available only for 'passport', 'driver_license', 'identity_card' and 'internal_passport'. The file can be decrypted and verified using the accompanying EncryptedCredentials.
    reverse_side: Encrypted file with the reverse side of the document, provided by the user; available only for 'driver_license' and 'identity_card'. The file can be decrypted and verified using the accompanying EncryptedCredentials.
    selfie: Encrypted file with the selfie of the user holding a document, provided by the user; available if requested for 'passport', 'driver_license', 'identity_card' and 'internal_passport'. The file can be decrypted and verified using the accompanying EncryptedCredentials.
    translation: Array of encrypted files with translated versions of documents provided by the user; available if requested for 'passport', 'driver_license', 'identity_card', 'internal_passport', 'utility_bill', 'bank_statement', 'rental_agreement', 'passport_registration' and 'temporary_registration' types. Files can be decrypted and verified using the accompanying EncryptedCredentials."""
    type: str
    hash: str
    data: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    files: Optional[List[PassportFile]] = None
    front_side: Optional[PassportFile] = None
    reverse_side: Optional[PassportFile] = None
    selfie: Optional[PassportFile] = None
    translation: Optional[List[PassportFile]] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['EncryptedPassportElement']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['EncryptedPassportElement']``).\n        "
        if data is None:
            return None
        return cls(type=_parse_api_value('String', data.get('type')), hash=_parse_api_value('String', data.get('hash')), data=_parse_api_value('String', data.get('data')), phone_number=_parse_api_value('String', data.get('phone_number')), email=_parse_api_value('String', data.get('email')), files=_parse_api_value('Array of PassportFile', data.get('files')), front_side=_parse_api_value('PassportFile', data.get('front_side')), reverse_side=_parse_api_value('PassportFile', data.get('reverse_side')), selfie=_parse_api_value('PassportFile', data.get('selfie')), translation=_parse_api_value('Array of PassportFile', data.get('translation')))
