from typing import Optional

from fastapi import FastAPI


app = FastAPI()


BOOKS = {
    'book_1': {'title': 'Book One', 'author': 'Author One'},
    'book_2': {'title': 'Book Two', 'author': 'Author Two'},
    'book_3': {'title': 'Book Three', 'author': 'Author Three'},
    'book_4': {'title': 'Book Four', 'author': 'Author Four'},
    'book_5': {'title': 'Book Five', 'author': 'Author Five'},
}


@app.get('/')
async def read_all_books(skip_book: Optional[str] = None):
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[skip_book]
        return new_books
    return BOOKS


@app.get("/book/{book_name}")
async def read_book(book_name: str):
    return BOOKS[book_name]


@app.post('/')
async def create_book(book_title, book_author):
    current_book_id = 0

    if len(BOOKS) > 0:
        last_book = list(BOOKS.keys())[-1]
        last_book_id = int(last_book.split('_')[-1])
        current_book_id = last_book_id

    BOOKS[f"book_{current_book_id + 1}"] = {'title': book_title, 'author': book_author}
    return BOOKS[f"book_{current_book_id + 1}"]


@app.put('/{book_name}')
async def update_book(book_name: str, book_title: str, book_author: str):
    book_info = {'title': book_title, 'author': book_author}
    BOOKS[book_name] = book_info
    return BOOKS


@app.delete("/{book_name}")
async def delete_book(book_name: str):
    del BOOKS[book_name]
    return f"Book {book_name} has been deleted"
