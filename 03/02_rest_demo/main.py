from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory "database"
items_db: dict[int, dict] = {}
item_id_counter = 1

class Item(BaseModel):
    name: str
    description: str | None = None
    enabled: bool = True

# Create - POST
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    global item_id_counter
    item_id = item_id_counter
    item_id_counter += 1
    items_db[item_id] = item.dict()
    return items_db[item_id]


# Read - GET
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    item = items_db.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Read all items - GET
@app.get("/items/", response_model=list[Item])
def read_all_items():
    return list(items_db.values())

# Update - PATCH
@app.patch("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    existing_item = items_db.get(item_id)
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item = item.dict(exclude_unset=True)
    items_db[item_id].update(updated_item)
    return items_db[item_id]

# Enable/Disable - PUT
@app.put("/items/{item_id}/status", response_model=Item)
def toggle_item_status(item_id: int, enabled: bool):
    item = items_db.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item['enabled'] = enabled
    return item

# Delete - DELETE
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"detail": "Item deleted successfully"}