from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World!!!"}

@app.get("/items")
def read_item():
    return { "values": [{ "id": 1, "value": "item1" }, { "id": 2, "value": "item2" }] }