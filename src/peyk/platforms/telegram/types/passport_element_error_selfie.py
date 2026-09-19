from ._passport_factory import passport_type
from typing import List

PassportElementErrorSelfie = passport_type("PassportElementErrorSelfie", "selfie", [('type', str), ('file_hash', str), ('message', str)])
