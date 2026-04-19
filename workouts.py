from db import get_db

def get_categories():
    db = get_db()
    cursor = db.execute("SELECT id, name FROM categories ORDER BY name")
    return cursor.fetchall()

def get_all(query=None):
    db = get_db()
    base_sql = """
        SELECT w.id, w.date, w.sport, w.duration, w.notes, u.username, 
               GROUP_CONCAT(c.name, ', ') as category_list
        FROM workouts w 
        JOIN users u ON w.user_id = u.id 
        LEFT JOIN workout_categories wc ON w.id = wc.workout_id
        LEFT JOIN categories c ON wc.category_id = c.id
    """
    if query:
        sql = base_sql + " WHERE w.sport LIKE ? OR w.notes LIKE ? GROUP BY w.id ORDER BY w.date DESC"
        cursor = db.execute(sql, (f"%{query}%", f"%{query}%"))
    else:
        sql = base_sql + " GROUP BY w.id ORDER BY w.date DESC"
        cursor = db.execute(sql)
    return cursor.fetchall()

def add(user_id, date, sport, duration, notes, category_ids):
    db = get_db()
    cursor = db.execute("""
        INSERT INTO workouts (user_id, date, sport, duration, notes) 
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, date, sport, duration, notes))
    
    workout_id = cursor.lastrowid
    
    for cat_id in category_ids:
        db.execute("INSERT INTO workout_categories (workout_id, category_id) VALUES (?, ?)", (workout_id, cat_id))
        
    db.commit()

def delete(workout_id, user_id):
    db = get_db()
    db.execute("DELETE FROM workouts WHERE id = ? AND user_id = ?", (workout_id, user_id))
    db.commit()

# --- PROFIILISIVUN FUNKTIOT ---

def get_by_user(user_id):
    db = get_db()
    # Tähänkin on nyt lisätty tuo luokkien haku (GROUP_CONCAT)
    cursor = db.execute("""
        SELECT w.id, w.date, w.sport, w.duration, w.notes, 
               GROUP_CONCAT(c.name, ', ') as category_list
        FROM workouts w 
        LEFT JOIN workout_categories wc ON w.id = wc.workout_id
        LEFT JOIN categories c ON wc.category_id = c.id
        WHERE w.user_id = ? 
        GROUP BY w.id
        ORDER BY w.date DESC
    """, (user_id,))
    return cursor.fetchall()

def get_stats(user_id):
    db = get_db()
    
    cursor = db.execute("""
        SELECT COUNT(id) as total_workouts, SUM(duration) as total_duration
        FROM workouts WHERE user_id = ?
    """, (user_id,))
    stats = cursor.fetchone()
    
    cursor2 = db.execute("""
        SELECT sport, COUNT(id) as count
        FROM workouts WHERE user_id = ?
        GROUP BY sport ORDER BY count DESC LIMIT 1
    """, (user_id,))
    favorite = cursor2.fetchone()

    return {
        "total_workouts": stats["total_workouts"] or 0,
        "total_duration": stats["total_duration"] or 0,
        "favorite_sport": favorite["sport"] if favorite else "Ei vielä treenejä"
    }

# Hakee yhden tietyn treenin kaikki tiedot
def get_workout(workout_id):
    db = get_db()
    cursor = db.execute("""
        SELECT w.id, w.date, w.sport, w.duration, w.notes, u.username, 
               GROUP_CONCAT(c.name, ', ') as category_list
        FROM workouts w 
        JOIN users u ON w.user_id = u.id 
        LEFT JOIN workout_categories wc ON w.id = wc.workout_id
        LEFT JOIN categories c ON wc.category_id = c.id
        WHERE w.id = ?
        GROUP BY w.id
    """, (workout_id,))
    return cursor.fetchone()

# Hakee treeniin liittyvät kommentit
def get_comments(workout_id):
    db = get_db()
    cursor = db.execute("""
        SELECT c.content, c.sent_at, u.username
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.workout_id = ?
        ORDER BY c.sent_at ASC
    """, (workout_id,))
    return cursor.fetchall()

# Tallentaa uuden kommentin
def add_comment(workout_id, user_id, content):
    db = get_db()
    db.execute("INSERT INTO comments (workout_id, user_id, content) VALUES (?, ?, ?)", 
               (workout_id, user_id, content))
    db.commit()