from ._passport_factory import passport_type
from typing import List

PassportElementErrorFiles = passport_type("PassportElementErrorFiles", "files", [('type', str), ('file_hashes', List[str]), ('message', str)])
