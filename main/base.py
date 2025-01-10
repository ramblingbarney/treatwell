from typing import Generic, TypeVar

TVar = TypeVar("Tvar", bound="Base")


class Base(Generic[TVar]):
    @classmethod
    def get_class(cls) -> "Base":
        return cls()
