from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "treenipaivakirja_salaisuus"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)



# 1. ETUSIVU, LISTAUS JA HAKUTOIMINTO

@app.route("/")
def index():

    query = request.args.get("query")
    
    if query:

        sql = text("""
            SELECT w.id, w.date, w.sport, w.duration, w.notes, u.username 
            FROM workouts w 
            JOIN users u ON w.user_id = u.id 
            WHERE w.sport LIKE :query OR w.notes LIKE :query
            ORDER BY w.date DESC
        """)
        result = db.session.execute(sql, {"query": f"%{query}%"})
    else:
        sql = text("""
            SELECT w.id, w.date, w.sport, w.duration, w.notes, u.username 
            FROM workouts w 
            JOIN users u ON w.user_id = u.id 
            ORDER BY w.date DESC
        """)
        result = db.session.execute(sql)
        
    workouts = result.fetchall()
    return render_template("index.html", workouts=workouts, query=query)



# 2. KIRJAUTUMINEN JA REKISTERÖITYMINEN

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        hash_value = generate_password_hash(password)

        try:
            sql = text("INSERT INTO users (username, password_hash) VALUES (:username, :password_hash)")
            db.session.execute(sql, {"username": username, "password_hash": hash_value})
            db.session.commit()
            return redirect("/login")
        except:
            return "Käyttäjätunnus on jo varattu! Kokeile toista."

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = text("SELECT id, password_hash FROM users WHERE username = :username")
        result = db.session.execute(sql, {"username": username})
        user = result.fetchone()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            session["username"] = username
            return redirect("/")
        else:
            return "Väärä tunnus tai salasana!"

    return render_template("login.html")

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")


# 3. TREENIEN LISÄÄMINEN, MUOKKAUS JA POISTO

@app.route("/new", methods=["GET", "POST"])
def new_workout():
    # Estetään pääsy, jos ei ole kirjautunut
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        date = request.form["date"]
        sport = request.form["sport"]
        duration = request.form["duration"]
        notes = request.form["notes"]
        
        sql = text("""
            INSERT INTO workouts (user_id, date, sport, duration, notes) 
            VALUES (:user_id, :date, :sport, :duration, :notes)
        """)
        db.session.execute(sql, {
            "user_id": session["user_id"], 
            "date": date, 
            "sport": sport, 
            "duration": duration, 
            "notes": notes
        })
        db.session.commit()
        return redirect("/")

    return render_template("new.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_workout(id):
    if "user_id" not in session:
        return redirect("/login")

    # Varmistetaan, että treeni on olemassa ja kuuluu TÄLLE käyttäjälle
    sql_check = text("SELECT * FROM workouts WHERE id = :id AND user_id = :user_id")
    result = db.session.execute(sql_check, {"id": id, "user_id": session["user_id"]})
    workout = result.fetchone()

    if not workout:
        return "Ei oikeutta muokata tätä treeniä tai sitä ei löydy!"

    if request.method == "POST":
        new_date = request.form["date"]
        new_sport = request.form["sport"]
        new_duration = request.form["duration"]
        new_notes = request.form["notes"]
        
        sql_update = text("""
            UPDATE workouts 
            SET date = :date, sport = :sport, duration = :duration, notes = :notes 
            WHERE id = :id
        """)
        db.session.execute(sql_update, {
            "date": new_date, 
            "sport": new_sport, 
            "duration": new_duration, 
            "notes": new_notes, 
            "id": id
        })
        db.session.commit()
        return redirect("/")

    return render_template("edit.html", workout=workout)

@app.route("/delete/<int:id>", methods=["POST"])
def delete_workout(id):
    if "user_id" not in session:
        return redirect("/login")

    # Vain oma treeni voidaan poistaa (user_id ehto turvaa tämän)
    sql = text("DELETE FROM workouts WHERE id = :id AND user_id = :user_id")
    db.session.execute(sql, {"id": id, "user_id": session["user_id"]})
    db.session.commit()
    
    return redirect("/")