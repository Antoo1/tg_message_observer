from functools import cached_property
from typing import TypeVar, Callable, Any


T = TypeVar('T')


class LazyInitWrapper:

    def __init__(self, creator: Callable[[], T]):
        self._creator = creator

    @cached_property
    def __instance__(self) -> T:
        return self._creator()

    def __getattr__(self, item: str) -> Any:
        return getattr(self.__instance__, item)

    def __call__(self):
        return self.__instance__

    async def __aenter__(self, *args, **kwargs):
        return await self.__aenter__(*args, **kwargs)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.__aexit__(exc_type, exc_val, exc_tb)
