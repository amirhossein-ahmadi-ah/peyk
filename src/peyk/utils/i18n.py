from __future__ import annotations
import gettext
from typing import Awaitable
from pathlib import Path
from typing import Callable, Mapping
LocaleGetter = Callable[[object, Mapping[str, object]], str]

class LazyText:
    """LazyText provides the utility API surface used by peyk."""

    def __init__(self, resolver: Callable[[], str]) -> None:
        self._resolver = resolver

    def __str__(self) -> str:
        return self._resolver()

    def __repr__(self) -> str:
        return repr(str(self))

class I18n:
    """Load GNU gettext catalogs and provide aiogram-style translation helpers."""

    def __init__(self, path: str | Path, default_locale: str='fa', domain: str='messages') -> None:
        self.path = Path(path)
        self.default_locale = default_locale
        self.domain = domain
        self.current_locale = default_locale
        self._translations: dict[str, gettext.NullTranslations] = {}

    def _translation(self, locale: str) -> gettext.NullTranslations:
        if locale not in self._translations:
            self._translations[locale] = gettext.translation(self.domain, localedir=str(self.path), languages=[locale], fallback=True)
        return self._translations[locale]

    def set_locale(self, locale: str) -> None:
        """Updates locale through the utility API.

Args:
    locale: Locale used for translation lookup."""
        self.current_locale = locale

    def gettext(self, message: str, locale: str | None=None) -> str:
        """Performs the gettext operation for the utility client.

Args:
    message: Value used by this operation.
    locale: Locale used for translation lookup.

Returns:
    Result produced by the utility operation."""
        return self._translation(locale or self.current_locale).gettext(message)

    def ngettext(self, singular: str, plural: str, n: int, locale: str | None=None) -> str:
        """Performs the ngettext operation for the utility client.

Args:
    singular: Value used by this operation.
    plural: Value used by this operation.
    n: Value used by this operation.
    locale: Locale used for translation lookup.

Returns:
    Result produced by the utility operation."""
        return self._translation(locale or self.current_locale).ngettext(singular, plural, n)

    def lazy_gettext(self, message: str, locale: str | None=None) -> LazyText:
        """Performs the lazy gettext operation for the utility client.

Args:
    message: Value used by this operation.
    locale: Locale used for translation lookup.

Returns:
    Result produced by the utility operation."""
        return LazyText(lambda: self.gettext(message, locale))

class I18nMiddleware:
    """Inject ``i18n``, ``locale`` and translation callables into dispatcher DI."""

    def __init__(self, i18n: I18n, get_locale: LocaleGetter | None=None) -> None:
        self.i18n = i18n
        self.get_locale = get_locale or self._default_locale

    def _default_locale(self, event: object, data: Mapping[str, object]) -> str:
        user = getattr(event, 'from_user', None) or data.get('event_from_user')
        return getattr(user, 'language_code', None) or self.i18n.default_locale

    async def __call__(self, handler: Callable[[], Awaitable[object]], event: object, data: dict[str, object]) -> object:
        locale = self.get_locale(event, data)
        self.i18n.set_locale(locale)
        data.update({'i18n': self.i18n, 'locale': locale, 'gettext': self.i18n.gettext, 'ngettext': self.i18n.ngettext, 'lazy_gettext': self.i18n.lazy_gettext})
        return await handler()
