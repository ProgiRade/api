import uuid

from bytepit_api.database import db
from bytepit_api.models.auth_schemes import UserInDB


def get_user_by_username(username: str):
    query_tuple = ("SELECT * FROM users WHERE username = %s", (username,))
    result = db.execute_one(query_tuple)
    if result["result"]:
        return UserInDB(**result["result"][0])
    else:
        return None


def get_user_by_email(email: str):
    query_tuple = ("SELECT * FROM users WHERE email = %s", (email,))
    result = db.execute_one(query_tuple)
    if result["result"]:
        return UserInDB(**result["result"][0])
    else:
        return None


def get_user_by_id(user_id: uuid.UUID):
    query_tuple = ("SELECT * FROM users WHERE id = %s", (user_id,))
    result = db.execute_one(query_tuple)

    if result["result"]:
        return UserInDB(**result["result"][0])
    else:
        return None


def create_user(username, password_hash, name, surname, email, role, confirmation_token):
    user_insert_query = (
        "INSERT INTO users (username, password_hash, name, surname, email, role, is_verified) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (username, password_hash, name, surname, email, role, False),
    )

    token_insert_query = (
        "INSERT INTO verification_tokens (token, email) " "VALUES (%s, %s)",
        (confirmation_token, email),
    )
    result = db.execute_many([user_insert_query, token_insert_query])
    return result["affected_rows"] == 2


def update_user_role(user_id: uuid.UUID, role: str):
    user = get_user_by_id(user_id)

    if user:
        user_update_query = ("UPDATE users SET role = %s WHERE id = %s", (role, user_id))
        result = db.execute_one(user_update_query)

        return result["affected_rows"] == 1

    return False
