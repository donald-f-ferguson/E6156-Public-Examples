from pydantic import BaseModel
import asyncio


class Item(BaseModel):
    name: str


class ItemResource:
    async def get_item(self, item: Item = None, sleep=5) -> str:
        # Simulate an asynchronous operation
        if item and item.name:
            n = item.name
        else:
            n = "Item with no name."
        await asyncio.sleep(sleep)
        return f"Hello, {n}! This is an asynchronous response."



