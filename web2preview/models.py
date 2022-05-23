from typing import Dict, Optional


class WebPreview:
    """Preview fields extracted from webpage."""

    def __init__(
        self,
        url: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        image: Optional[str] = None,
        **properties: str,
    ) -> None:
        self.url = url
        self.title = title
        self.description = description
        self.image = image
        self.extend(**properties)

    def __getitem__(self, __name: str) -> Optional[str]:
        return self.__dict__.get(__name)

    def __setitem__(self, __name: str, __value: str) -> None:
        self.__dict__[__name] = __value

    def __contains__(self, __name: str) -> bool:
        return __name in self.__dict__

    def is_complete(self) -> bool:
        """Check that preview contains title, description, and image."""
        return bool(self.title and self.description and self.image)

    def extend(self, **properties: str) -> None:
        """Extend preview with new values. No overriding."""
        for k, v in properties.items():
            if k not in self.__dict__:
                self.__dict__[k] = v

    def merge(self, other: "WebPreview") -> None:
        """Merge values from other preview. No overriding."""
        self.__ior__(other)

    def to_dict(self, exclude_empty: bool = False, exclude_none: bool = True) -> Dict[str, str]:
        result = {}
        for k, v in self.__dict__.items():
            if k == "_soup":
                continue
            if v is None and exclude_none:
                continue
            if not v and exclude_empty:
                continue
            result[k] = v
        return result

    def __or__(self, other: "WebPreview") -> "WebPreview":
        props = {**other.to_dict(), **self.to_dict()}
        merged = WebPreview(**props)
        return merged

    def __ior__(self, other: "WebPreview") -> "WebPreview":
        d = {**other.to_dict(), **self.to_dict()}
        self.__dict__.update(d)
        return self

    def __repr__(self) -> str:
        arguments = ", ".join([f'{k}="{v}"' for k, v in self.to_dict().items()])
        return f"WebPreview({arguments})"

    def __str__(self) -> str:
        return self.__repr__()

    def __bool__(self) -> bool:
        return any(self.__dict__.values())
