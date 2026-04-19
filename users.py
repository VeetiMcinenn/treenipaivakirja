from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

def register(username, password):
    db = get_db()
    hash_value = generate_password_hash(password)
    try:
        # ? is a safe placeholder
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hash_value))
        db.commit()
        return True
    except:
        return False # Unique constraint violation, username already exists

def login(username, password):
    db = get_db()
    cursor = db.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    # If username and password match
    if user and check_password_hash(user["password_hash"], password):
        return user["id"]
    return None