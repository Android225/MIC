from fastapi import FastAPI
import requests
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str

@app.get("/")
def read_root():
    return {"Сообщение": "Привяо из service1"}

@app.get("/call_service2")
def call_service2():
    response = requests.get("http://service2:8001/data")
    return {"service2_response": response.json()}

@app.put("/update_item/{item_id}")
def update_item(item_id: int, item: Item):
    response = requests.put(f"http://service2:8001/update_item/{item_id}", json=item.dict())
    return {"service2_response": response.json()}

@app.delete("/delete_item/{item_id}")
def delete_item(item_id: int):
    response = requests.delete(f"http://service2:8001/delete_item/{item_id}")
    return {"service2_response": response.json()}

@app.patch("/patch_item/{item_id}")
def patch_item(item_id: int, item: Item):
    response = requests.patch(f"http://service2:8001/patch_item/{item_id}", json=item.dict())
    return {"service2_response": response.json()}
