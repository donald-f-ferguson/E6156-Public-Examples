from pydantic import BaseModel
import asyncio
import aiohttp
import json


class Item(BaseModel):
    name: str


class ItemResource:
    #
    # These endpoints are on Prof. Ferguson's SwaggerHub mock APIs
    #
    resources = [
        {
            "resource": "student",
            "url": 'https://virtserver.swaggerhub.com/donald-f-ferguson/E6156Student/1.0.0/students/bb2101'
        },
        {
            "resource": "sections",
            "url": 'https://virtserver.swaggerhub.com/Columbia-Classes/Sections/1.0.0/sections?uni=bb2101'
        },
        {
            "resource": "projects",
            "url": 'https://virtserver.swaggerhub.com/Columbia-Classes/ProjectInfo/1.0.0/projects?uni=bb2021'
        }
    ]

    async def get_item(self, item: Item = None, sleep=5) -> str:
        # Simulate an asynchronous operation
        if item and item.name:
            n = item.name
        else:
            n = "Item with no name."
        await asyncio.sleep(sleep)
        return f"Hello, {n}! This is an asynchronous response."

    @classmethod
    async def fetch(cls, session, resource):
        url = resource["url"]
        print("Calling URL = ", url)
        async with session.get(url) as response:
            t = await response.json()
            print("URL ", url, "returned", str(t))
            result = {
                "resource": resource["resource"],
                "data": t
            }
        return result

    async def get_student(self):
        full_result = None

        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.ensure_future(
                ItemResource.fetch(session, res)) for res in ItemResource.resources]
            responses = await asyncio.gather(*tasks)
            full_result = {}
            for response in responses:
                full_result[response["resource"]] = response["data"]

            return full_result

            # print("\nFull Result = ", json.dumps(full_result, indent=2))



