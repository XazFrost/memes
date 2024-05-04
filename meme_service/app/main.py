import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from database import database as database
from database.database import MemeDB
from model.model import Meme

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'Service alive'}


@app.post("/add_meme")
async def add_meme(meme: Meme, db: db_dependency):
    new_meme = MemeDB(**meme.dict())
    db.add(new_meme)
    db.commit()
    db.refresh(new_meme)
    return new_meme


@app.get("/memes")
async def list_memes(db: db_dependency):
    return db.query(MemeDB).all()


@app.get("/get_meme_by_id/{meme_id}")
async def get_meme_by_id(meme_id: int, db: db_dependency):
    meme = db.query(MemeDB).filter(MemeDB.id == meme_id).first()
    if not meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    return meme


@app.delete("/delete_meme/{meme_id}")
async def delete_meme(meme_id: int, db: db_dependency):
    meme = db.query(MemeDB).filter(MemeDB.id == meme_id).first()
    if not meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    db.delete(meme)
    db.commit()
    return {"message": "Meme deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
