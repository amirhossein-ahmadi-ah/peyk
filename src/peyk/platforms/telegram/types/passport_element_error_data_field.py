from ._passport_factory import passport_type
from typing import List

PassportElementErrorDataField = passport_type("PassportElementErrorDataField", "data", [('type', str), ('field_name', str), ('data_hash', str), ('message', str)])
