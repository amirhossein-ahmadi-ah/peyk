from ._passport_factory import passport_type
from typing import List

PassportElementErrorFrontSide = passport_type("PassportElementErrorFrontSide", "front_side", [('type', str), ('file_hash', str), ('message', str)])
