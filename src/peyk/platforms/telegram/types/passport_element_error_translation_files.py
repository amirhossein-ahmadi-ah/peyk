from ._passport_factory import passport_type
from typing import List

PassportElementErrorTranslationFiles = passport_type("PassportElementErrorTranslationFiles", "translation_files", [('type', str), ('file_hashes', List[str]), ('message', str)])
