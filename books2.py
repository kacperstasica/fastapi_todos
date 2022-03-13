from typing import Optional

from fastapi import FastAPI, HTTPException, Request, Form, status, Header
from pydantic import BaseModel, Field
from uuid import UUID

from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: Optional[str] = Field(
        title="Description of the book",
        min_length=1,
        max_length=100,
    )
    rating: int = Field(ge=0, le=100)

    class Config:
        schema_extra = {
            "example": {
                "id": "0608778f-9a37-4f28-b957-07aa59d69a45",
                "title": "Tęcza Grawitacji",
                "author": "Thomas Pynchon",
                "description": "Best book ever",
                "rating": 100
            }
        }


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: Optional[str] = Field(
        title="Description of the book",
        min_length=1,
        max_length=100,
    )

    class Config:
        schema_extra = {
            "example": {
                "id": "0608778f-9a37-4f28-b957-07aa59d69a45",
                "title": "Tęcza Grawitacji",
                "author": "Thomas Pynchon",
                "description": "Best book ever",
            }
        }


BOOKS = []


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(
        request: Request,
        exception: NegativeNumberException,
):
    return JSONResponse(
        status_code=418,
        content={
            "message": f"Hey, why do you want {exception.books_to_return} "
                       f"books? You need to read more."
        }
    )


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()


@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):

    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)

    if len(BOOKS) < 1:
        create_books_no_api()
    if books_to_return and len(BOOKS) >= books_to_return > 0:
        return BOOKS[:books_to_return]
    return BOOKS


@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0

    for x in BOOKS:
        if x.id == book_id:
            counter += 1
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.post("/books/login")
async def book_login(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "password": password}


@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"header": random_header}


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            book_title = BOOKS[counter - 1].title
            del BOOKS[counter - 1]
            return f"ID: {book_id}, TITLE: {book_title} deleted"
    raise raise_item_cannot_be_found_exception()


def create_books_no_api():
    book_1 = Book(
        id="0608778f-9a37-4f28-b957-07aa59d69a44",
        title='Title 1',
        author='Author 1',
        description="Description 1",
        rating=60,
    )
    book_2 = Book(
        id="0608778f-9a37-4f28-b957-07aa59d69a41",
        title='Title 2',
        author='Author 2',
        description="Description 2",
        rating=40,
    )
    book_3 = Book(
        id="0608778f-9a37-4f28-b957-07aa59d69a42",
        title='Title 3',
        author='Author 3',
        description="Description 3",
        rating=66,
    )
    book_4 = Book(
        id="0608778f-9a37-4f28-b957-07aa59d69a45",
        title='Title 4',
        author='Author 4',
        description="Description 4",
        rating=98,
    )
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)


def raise_item_cannot_be_found_exception():
    return HTTPException(
        status_code=404,
        detail='Book not found',
        headers={
            'X-Header-Error': 'Nothing to be seen at the UUID'
        },
    )
