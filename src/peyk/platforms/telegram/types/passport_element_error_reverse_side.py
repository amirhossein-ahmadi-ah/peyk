from ._passport_factory import passport_type
from typing import List

PassportElementErrorReverseSide = passport_type("PassportElementErrorReverseSide", "reverse_side", [('type', str), ('file_hash', str), ('message', str)])
