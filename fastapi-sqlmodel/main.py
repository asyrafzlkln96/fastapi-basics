from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from models import Book
from database import engine
from sqlmodel import Session, select
from typing import Optional, List, Dict

app = FastAPI()

session = Session(bind=engine)

@app.get('/books',response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_all_books():
    statement=select(Book)
    results = session.exec(statement).all()
    return results

@app.post('/books', response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_a_book(book:Book):
    new_book = Book(title=book.title, description=book.description)
    session.add(new_book)
    session.commit()
    # return {'Status': 'A new book has been added!', 'Book_Details': new_book}
    return new_book
   

@app.get('/books/{book_id}',status_code=status.HTTP_200_OK)
async def get_a_book(book_id:int):
    statement=select(Book).where(Book.id==book_id)
    result = session.exec(statement).first()

    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return result
    # return {'Status': 'Get book ID: {book_id}', 'Book_Details': result}

@app.put('/book/{book_id}',response_model=Book)
async def update_books(book_id:int, book:Book):
    statement = select(Book).where(Book.id==book_id)
    result = session.exec(statement).first()
    result.title = book.title
    result.description = book.description

    session.commit()

    return result

    # return {'Status': 'Book ID: {book_id} is updated!', 'Book_Details': result}

@app.delete('/book/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_books(book_id:int):
    statement = select(Book).where(Book.id==book_id)
    result = session.exec(statement).one_or_none()

    if result == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Book Not Found"
        )

    session.delete(result)
    return result