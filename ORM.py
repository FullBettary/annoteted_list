from models.sql_models import *


def get_books_list():
    books_name = [(item['id'], item['name']) for item in Book.select(Book.id, Book.name).dicts().execute()]
    return books_name


def get_book_info_by_id(book_id):
    b = Book.get(Book.id == book_id)
    book_info = {'id': b.id, 'name': b.name, 'annotation': b.annotation, 'path': b.path}
    autor_ids = [item['autor_id'] for item in AutorBooks.select(AutorBooks.autor_id).where(AutorBooks.book_id == book_id).dicts().execute()]
    authors = []
    for ids in autor_ids:
        authors.append(
            Autor.get(Autor.id == ids).autor
        )
    return {'book_info': book_info, 'authors': authors}


def add_book(book_name: str, authors: list, annotation: str):
    b_name = book_name.split('.')[:-1]  # remove file extension
    b_name = '.'.join(b_name)

    a = [item['autor'] for item in Autor.select(Autor.autor).dicts().execute()]
    for autor in authors:
        if autor not in a:
            Autor.create(autor=autor)

    is_created = False
    id_book = None
    for autor in authors:
        autor_id = Autor.get(Autor.autor == autor).id
        sq = AutorBooks.select(AutorBooks.book_id).where(AutorBooks.autor_id == autor_id)
        books = []
        for book_id in [item['book_id'] for item in sq.dicts().execute()]:
            book = Book.get(Book.id == book_id).name
            books.append(book)
        if not (b_name in books):
            if not is_created:
                id_book = Book.create(name=b_name, annotation=annotation, path=f'books/{book_name}')
                is_created = True
            AutorBooks.create(autor_id=autor_id, book_id=id_book)


def delete_book(book_id):
    if book_id in [item['id'] for item in Book.select(Book.id).dicts().execute()]:
        Book.get(Book.id == book_id).delete_instance()
        AutorBooks.delete().where(AutorBooks.book_id == book_id).execute()


# add_book('book5000.pdf', ['autor221', 'autor152', 'autor412'], 'very long annotation')
# delete_book(21)


