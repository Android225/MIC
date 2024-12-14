from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

DATABASE_URL = "postgresql://postgres:password@db:5432/mydb"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

class ItemCreate(BaseModel):
    name: str

@app.get("/data")
def read_data():
    db = SessionLocal()
    items = db.query(Item).all()
    return {"items": [item.name for item in items]}

@app.post("/add_item")
def add_item(item: ItemCreate):
    db = SessionLocal()
    new_item = Item(name=item.name)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"Сообщение": f"Элемент {new_item.name} добавлен"}

@app.put("/update_item/{item_id}")
def update_item(item_id: int, item: ItemCreate):
    db = SessionLocal()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Элемент не найден")
    db_item.name = item.name
    db.commit()
    db.refresh(db_item)
    return {"Сообщение": f"Элемент {item_id} обновлен до {db_item.name}"}

@app.delete("/delete_item/{item_id}")
def delete_item(item_id: int):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Элемент не найден")
    db.delete(item)
    db.commit()
    return {"Сообщение": f"Элемент {item_id} удален"}

@app.patch("/patch_item/{item_id}")
def patch_item(item_id: int, item: ItemCreate):
    db = SessionLocal()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Элемент не найден")
    if item.name:
        db_item.name = item.name
    db.commit()
    db.refresh(db_item)
    return {"Сообщение": f"Элемент {item_id} запатчен до {db_item.name}"}
