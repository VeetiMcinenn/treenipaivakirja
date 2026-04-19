from flask import render_template, request, redirect, session
import users
import workouts

def index():
    query = request.args.get("query")
    workout_list = workouts.get_all(query)
    return render_template("index.html", workouts=workout_list, query=query)

def register():
    if request.method == "POST":
        # .strip() estää tyhjät välilyönnit
        username = request.form["username"].strip()
        password = request.form["password"]
        
        # Syötteiden validointi
        if len(username) < 3 or len(password) < 4:
            return "Käyttäjätunnuksen (min 3) ja salasanan (min 4) on oltava pidempiä! <br><a href='/register'>Takaisin</a>"
        
        # Yritetään rekisteröidä
        if users.register(username, password):
            return redirect("/login")
        return "Tunnus on jo varattu! <br><a href='/register'>Kokeile toista</a>"
        
    return render_template("register.html")

def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user_id = users.login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
            
        return "Väärä tunnus tai salasana! <br><a href='/login'>Takaisin</a>"
        
    return render_template("login.html")

def logout():
    session.clear() # Fiksuin tapa tyhjentää kirjautuminen
    return redirect("/")

def new_workout():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        date = request.form["date"]
        sport = request.form["sport"]
        duration = request.form["duration"]
        notes = request.form["notes"]
        
        workouts.add(session["user_id"], date, sport, duration, notes)
        return redirect("/")
        
    return render_template("new.html")

def delete_workout(id):
    if "user_id" not in session:
        return redirect("/login")
        
    workouts.delete(id, session["user_id"])
    return redirect("/")