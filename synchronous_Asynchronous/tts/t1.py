from synchronous_Asynchronous.resources.item_resource import ItemResource
import json
import asyncio


async def t1():
    it = ItemResource()

    result = await it.get_student()
    if result:
        print("t1: result = \n", json.dumps(result, indent=2))
    else:
        print("Did not get a result.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(t1())
