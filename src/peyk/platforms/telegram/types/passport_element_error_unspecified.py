from ._passport_factory import passport_type
from typing import List

PassportElementErrorUnspecified = passport_type("PassportElementErrorUnspecified", "unspecified", [('type', str), ('element_hash', str), ('message', str)])
