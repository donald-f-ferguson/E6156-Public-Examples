from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio
import uvicorn
from resources.item_resource import ItemResource, Item

app = FastAPI()


example_instance = ItemResource()


@app.get("/get_item")
async def async_call(item_name: str = None):
    result = await example_instance.get_item(item_name)
    return JSONResponse(content={"message": result})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
