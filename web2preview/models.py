from typing import Any, Dict, Optional


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
        self._props: Dict[str, str] = {**properties}
        if url:
            self.url = url
        if title:
            self.title = title
        if description:
            self.description = description
        if image:
            self.image = image

    @property
    def url(self) -> Optional[str]:
        return self._props.get("url")

    @property
    def title(self) -> Optional[str]:
        return self._props.get("title")

    @property
    def description(self) -> Optional[str]:
        return self._props.get("description")

    @property
    def image(self) -> Optional[str]:
        return self._props.get("image")

    @url.setter
    def url(self, value: Optional[str]) -> None:
        self._props["url"] = value

    @title.setter
    def title(self, value: Optional[str]) -> None:
        self._props["title"] = value

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._props["description"] = value

    @image.setter
    def image(self, value: Optional[str]) -> None:
        self._props["image"] = value

    def __getattr__(self, __name: str) -> Any:
        return self._props.get(__name)

    def __getitem__(self, __name: str) -> Optional[str]:
        return self._props.get(__name)

    def __setitem__(self, __name: str, __value: str) -> None:
        self._props[__name] = __value

    def is_complete(self) -> bool:
        """Check that preview contains title, description, and image."""
        return bool(self.title and self.description and self.image)

    def extend(self, **properties: str) -> None:
        """Extend preview with new values. No overriding."""
        for k, v in properties.items():
            if k not in self._props:
                self._props[k] = v

    def merge(self, other: "WebPreview") -> None:
        """Merge values from other preview. No overriding."""
        self.__ior__(other)

    def __or__(self, other: "WebPreview") -> "WebPreview":
        props = {**other._props, **self._props}
        merged = WebPreview(**props)
        return merged

    def __ior__(self, other: "WebPreview") -> "WebPreview":
        self._props = {**other._props, **self._props}
        return self

    def __repr__(self) -> str:
        arguments = ", ".join([f'{k}="{v}"' for k, v in self._props.items() if v])
        return f"WebPreview({arguments})"

    def __str__(self) -> str:
        return self.__repr__()

    def __bool__(self) -> bool:
        return bool(self._props)
