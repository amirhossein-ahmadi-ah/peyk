from ._passport_factory import passport_type
from typing import List

PassportElementErrorFile = passport_type("PassportElementErrorFile", "file", [('type', str), ('file_hash', str), ('message', str)])
