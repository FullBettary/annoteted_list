from peewee import Model, TextField, SqliteDatabase, ForeignKeyField, PrimaryKeyField

database = SqliteDatabase('annotatedlist')


class BaseModel(Model):
    class Meta:
        database = database


class Autor(BaseModel):
    id = PrimaryKeyField(column_name='id')
    autor = TextField(column_name='autor')

    class Meta:
        table_name = 'Autors'


class Book(BaseModel):
    id = PrimaryKeyField(column_name='id')
    name = TextField(column_name='name')
    path = TextField(column_name='path')
    annotation = TextField(column_name='annotation')

    class Meta:
        table_name = 'Book'


class AutorBooks(BaseModel):
    autor_id = ForeignKeyField(Autor, column_name='autor_id')
    book_id = ForeignKeyField(Book, column_name='book_id')

    class Meta:
        table_name = 'autorbooks'
