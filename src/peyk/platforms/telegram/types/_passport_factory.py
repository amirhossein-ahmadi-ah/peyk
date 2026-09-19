"""Factory support for Telegram Passport element-error dataclasses."""

from __future__ import annotations

from dataclasses import dataclass


def passport_type(name: str, source: str, extra_fields: list[tuple[str, object]]):
    """Create a Telegram Passport element-error dataclass.

    Args:
        name: Public class name.
        source: Telegram ``source`` discriminator value.
        extra_fields: Additional field names and annotations.

    Returns:
        A dataclass matching the legacy Passport error model.
    """
    annotations = {k: t for k, t in extra_fields}
    annotations["source"] = str
    namespace = {"__annotations__": annotations, "source": source}

    @classmethod
    def from_dict(cls, data):
        """Executes the from_dict operation.
        
        Args:
            data: Value of the declared parameter type.
        
        
        Returns:
            The operation result (``Any``).
        """
        if data is None:
            return None
        kw = {"source": data.get("source", source)}
        for k, _ in extra_fields:
            kw[k] = data.get(k)
        return cls(**kw)
    namespace["from_dict"] = from_dict

    @classmethod
    def list_from(cls, data):
        """Executes the list_from operation.
        
        Args:
            data: Value of the declared parameter type.
        
        
        Returns:
            The operation result (``Any``).
        """
        return [cls.from_dict(x) for x in data or []]
    namespace["list_from"] = list_from

    def to_dict(self):
        """Executes the to_dict operation.
        
        Returns:
            The operation result (``Any``).
        """
        return {k: getattr(self, k) for k in annotations if getattr(self, k, None) is not None}
    namespace["to_dict"] = to_dict
    namespace["__doc__"] = f"{name} Telegram Bot API type."
    return dataclass(type(name, (), namespace))
