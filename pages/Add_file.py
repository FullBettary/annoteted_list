import sys
import os
# sys.path.append('../ORM.py')
import hmac
import streamlit as st
from ORM import add_book, delete_book, get_book_info_by_id


def save_file(file):
    name = file.name
    with open(os.path.join('books', name), 'wb') as f:
        f.write(file.getbuffer())


@st.cache_data
def get_file(path):
    with open(path, 'rb') as f:
        file = f.read()
    return file


def delete_file(path):
    os.remove(os.path.join(path))


def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            # del st.session_state["password"]  # Don't store the username or password.
            # del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


if not check_password():
    st.stop()

st.write('<h4>Добавить книгу</h4>',
         unsafe_allow_html=True)

authors = st.text_input(label='Список авторов. Перечисляйте авторов через запятую!')

annotation = st.text_area(label='Аннотация')

with st.form("my-form", clear_on_submit=True):
    uploaded_file = st.file_uploader('Поместите Ваш файл сюда',
                                     type=['pdf', 'docx', 'doc', 'txt'])
    submitted = st.form_submit_button("Добавить книгу")

if submitted:
    if uploaded_file is not None:
        authors_list = authors.split(',')
        add_book(book_name=uploaded_file.name,
                 authors=authors_list, annotation=annotation)
        st.write(f'Файл добавлен как: {uploaded_file.name}')
        save_file(uploaded_file)

st.write('<h4>Удалить книгу</h4>',
         unsafe_allow_html=True)

id_for_remove = st.number_input(label='Введите id книги для ее удаления', value=None, min_value=0)
if st.button(label='Удалить!'):
    try:
        path_to_file = get_book_info_by_id(id_for_remove)['book_info']['path']
        delete_file(path_to_file)
        delete_book(id_for_remove)
    except Exception:
        st.write('Что-то не то! Возможно такой книги в базе нет!')