# Create DB

from sqlmodel import SQLModel
from models import Book
from database import engine

print("CREATING DB .....")

SQLModel.metadata.create_all(engine)
