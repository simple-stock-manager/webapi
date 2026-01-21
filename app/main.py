from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import engine, Base, get_session
from .models import InventoryItem
from .schemas import CreateInventoryItem, UpdateInventoryItem, InventoryItemResponse

app = FastAPI(title="Simple Stock Manager API")


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/items", response_model=InventoryItemResponse)
async def create_item(payload: CreateInventoryItem, session: AsyncSession = Depends(get_session)):
    item = InventoryItem(**payload.dict())
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


@app.get("/items", response_model=List[InventoryItemResponse])
async def list_items(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(InventoryItem).offset(skip).limit(limit))
    items = result.scalars().all()
    return items


@app.get("/items/{item_id}", response_model=InventoryItemResponse)
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)):
    item = await session.get(InventoryItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=InventoryItemResponse)
async def update_item(item_id: int, payload: UpdateInventoryItem, session: AsyncSession = Depends(get_session)):
    item = await session.get(InventoryItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(item, k, v)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int, session: AsyncSession = Depends(get_session)):
    item = await session.get(InventoryItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    await session.delete(item)
    await session.commit()
    return
