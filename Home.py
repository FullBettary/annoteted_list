import streamlit as st
from ORM import *


@st.cache_data
def get_file(path):
    with open(path, 'rb') as f:
        file = f.read()
    return file


st.write('<h2>Аннотированный каталог</h2>',
         unsafe_allow_html=True)

book_list = get_books_list()

for Id, book_title in book_list:
    with st.expander(label=book_title):
        info = get_book_info_by_id(Id)
        authors = info['authors']
        book_info = info['book_info']

        st.write(f'<h20>Book id: {Id}</h20><br/>'
                 f'Авторы<br/>'
                 f'{", ".join(authors)}<br/><br/>'
                 f'Аннотация<br/>'
                 f'{book_info["annotation"]}',
                 unsafe_allow_html=True)
        file = get_file(book_info['path'])
        st.download_button(label='Download',
                           data=file,
                           file_name=book_info['path'].split('/')[-1])


