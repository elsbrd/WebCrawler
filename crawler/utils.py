import asyncio


class AtomicSet:
    def __init__(self):
        self._set = set()
        self._lock = asyncio.Lock()

    async def add(self, item):
        """
        Atomically adds an item to the set.
        """

        async with self._lock:
            self._set.add(item)

    async def contains(self, item):
        """
        Atomically checks if an item is in the set.
        """

        async with self._lock:
            return item in self._set
