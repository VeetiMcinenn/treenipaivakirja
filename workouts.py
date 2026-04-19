from db import get_db

def get_all(query=None):
    db = get_db()
    if query:
        cursor = db.execute("""
            SELECT w.id, w.date, w.sport, w.duration, w.notes, u.username 
            FROM workouts w 
            JOIN users u ON w.user_id = u.id 
            WHERE w.sport LIKE ? OR w.notes LIKE ? 
            ORDER BY w.date DESC
        """, (f"%{query}%", f"%{query}%"))
    else:
        cursor = db.execute("""
            SELECT w.id, w.date, w.sport, w.duration, w.notes, u.username 
            FROM workouts w 
            JOIN users u ON w.user_id = u.id 
            ORDER BY w.date DESC
        """)
    return cursor.fetchall()

def add(user_id, date, sport, duration, notes):
    db = get_db()
    db.execute("""
        INSERT INTO workouts (user_id, date, sport, duration, notes) 
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, date, sport, duration, notes))
    db.commit()

def delete(workout_id, user_id):
    db = get_db()
    db.execute("DELETE FROM workouts WHERE id = ? AND user_id = ?", (workout_id, user_id))
    db.commit()