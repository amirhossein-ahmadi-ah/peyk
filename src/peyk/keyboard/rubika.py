from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class _RubikaButton:
    text: str
    button_id: str

    def as_payload(self) -> dict[str, object]:
        """Performs the as payload operation for the keyboard client.

Returns:
    Result produced by the keyboard operation."""
        return {'button_text': self.text, 'id': self.button_id}

@dataclass(frozen=True)
class Selection(_RubikaButton):
    """Selection provides the keyboard API surface used by peyk."""
    selection_id: str = ''
    search_type: str = 'None'
    get_type: str = 'Local'
    items: tuple[object, ...] = ()
    is_multi_selection: bool = False
    columns_count: str = '1'
    title: str | None = None

@dataclass(frozen=True)
class Calendar(_RubikaButton):
    """Calendar provides the keyboard API surface used by peyk."""
    default_value: str | None = None
    type: str = 'DatePersian'
    min_year: str = '1300'
    max_year: str = '1450'
    title: str = ''

@dataclass(frozen=True)
class NumberPicker(_RubikaButton):
    """NumberPicker provides the keyboard API surface used by peyk."""
    min_value: str = '0'
    max_value: str = '100'
    default_value: str | None = None
    title: str = ''

@dataclass(frozen=True)
class StringPicker(_RubikaButton):
    """StringPicker provides the keyboard API surface used by peyk."""
    items: tuple[str, ...] = ()
    default_value: str | None = None
    title: str | None = None

@dataclass(frozen=True)
class Location(_RubikaButton):
    """Location provides the keyboard API surface used by peyk."""
    default_pointer_location: object | None = None
    default_map_location: object | None = None
    type: str = 'Picker'
    title: str | None = None

@dataclass(frozen=True)
class CameraImage(_RubikaButton):
    """CameraImage provides the keyboard API surface used by peyk."""
    pass

@dataclass(frozen=True)
class CameraVideo(_RubikaButton):
    """CameraVideo provides the keyboard API surface used by peyk."""
    pass

@dataclass(frozen=True)
class GalleryImage(_RubikaButton):
    """GalleryImage provides the keyboard API surface used by peyk."""
    pass

@dataclass(frozen=True)
class GalleryVideo(_RubikaButton):
    """GalleryVideo provides the keyboard API surface used by peyk."""
    pass

@dataclass(frozen=True)
class File(_RubikaButton):
    """File provides the keyboard API surface used by peyk."""
    pass

@dataclass(frozen=True)
class Audio(_RubikaButton):
    """Audio provides the keyboard API surface used by peyk."""
    pass

@dataclass(frozen=True)
class RecordAudio(_RubikaButton):
    """RecordAudio provides the keyboard API surface used by peyk."""
    pass

@dataclass(frozen=True)
class Textbox(_RubikaButton):
    """Textbox provides the keyboard API surface used by peyk."""
    type_line: str = 'SingleLine'
    type_keypad: str = 'String'
    place_holder: str | None = None
    title: str | None = None
    default_value: str | None = None

@dataclass(frozen=True)
class Link(_RubikaButton):
    """Link provides the keyboard API surface used by peyk."""
    url: str = ''

@dataclass(frozen=True)
class AskMyPhoneNumber(_RubikaButton):
    """AskMyPhoneNumber provides the keyboard API surface used by peyk."""
    pass

@dataclass(frozen=True)
class AskMyLocation(_RubikaButton):
    """AskMyLocation provides the keyboard API surface used by peyk."""
    pass

@dataclass(frozen=True)
class Barcode(_RubikaButton):
    """Barcode provides the keyboard API surface used by peyk."""
    pass
