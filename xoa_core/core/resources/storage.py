from __future__ import annotations
import asyncio
from pathlib import Path
import shelve
from functools import partial
from typing import Protocol, TypeVar
from .types import TesterID, StorageResource


class Resource(Protocol):
    @property
    def store_data(self) -> StorageResource:
        ...


class Methods:
    @staticmethod
    def save(open_db: partial[shelve.Shelf], params: StorageResource) -> None:
        with open_db() as db:
            db[params["id"]] = params

    @staticmethod
    def get_all(open_db: partial[shelve.Shelf]) -> tuple[StorageResource]:
        with open_db() as db:
            return tuple(db.values())

    @staticmethod
    def delete(open_db: partial[shelve.Shelf], id: TesterID) -> None:
        with open_db() as db:
            if id not in db:
                return None
            del db[id]

    @staticmethod
    def is_exist(open_db: partial[shelve.Shelf], id: TesterID) -> bool:
        with open_db() as db:
            return id in db


T = TypeVar("T")


class PrecisionStorage:
    __slots__ = ("_lock", "_loop", "__open",)

    def __init__(self, storage_path: Path) -> None:
        self._lock = asyncio.Lock()
        self._loop = asyncio.get_event_loop()
        self.__open = partial(shelve.open, str(storage_path))

    async def __run(self, func: partial[T]) -> T:
        async with self._lock:
            return await self._loop.run_in_executor(None, func)

    async def get_all(self) -> tuple[StorageResource]:
        method = partial(Methods.get_all, self.__open)
        return await self.__run(method)

    async def is_registered(self, t_id: TesterID) -> bool:
        method = partial(Methods.is_exist, self.__open, t_id)
        return await self.__run(method)

    async def save(self, resource: Resource) -> None:
        method = partial(Methods.save, self.__open, resource.store_data)
        return await self.__run(method)

    async def delete(self, t_id: TesterID) -> None:
        method = partial(Methods.delete, self.__open, t_id)
        return await self.__run(method)
