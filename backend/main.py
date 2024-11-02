from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database.connection import SessionLocal, engine
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create the database tables
User.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def create_user(firstName: str, lastName: str, email: str, db: Session = Depends(get_db)):
    db_user = User(firstName = firstName, lastName = lastName, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
