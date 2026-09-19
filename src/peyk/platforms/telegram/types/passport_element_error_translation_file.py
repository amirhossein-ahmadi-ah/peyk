from ._passport_factory import passport_type
from typing import List

PassportElementErrorTranslationFile = passport_type("PassportElementErrorTranslationFile", "translation_file", [('type', str), ('file_hash', str), ('message', str)])
