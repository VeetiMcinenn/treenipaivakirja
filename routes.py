from flask import render_template, request, redirect, session
import users
import workouts

def index():
    query = request.args.get("query")
    workout_list = workouts.get_all(query)
    return render_template("index.html", workouts=workout_list, query=query)

def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        
        if len(username) < 3 or len(password) < 4:
            return "Käyttäjätunnuksen (min 3) ja salasanan (min 4) on oltava pidempiä! <br><a href='/register'>Takaisin</a>"
        
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
    session.clear()
    return redirect("/")

def new_workout():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        date = request.form["date"]
        sport = request.form["sport"]
        duration = request.form["duration"]
        notes = request.form["notes"]
        
    
        category_ids = request.form.getlist("categories")
        
        #sending list to workouts.py where it will be processed

        workouts.add(session["user_id"], date, sport, duration, notes, category_ids)
        return redirect("/")
        
    # Get classes 
    all_categories = workouts.get_categories()
    return render_template("new.html", categories=all_categories)

def delete_workout(id):
    if "user_id" not in session:
        return redirect("/login")
        
    workouts.delete(id, session["user_id"])
    return redirect("/")

def profile():
    # Deny access if not logged in
    if "user_id" not in session:
        return redirect("/login")
        
    user_id = session["user_id"]
    user_workouts = workouts.get_by_user(user_id)
    user_stats = workouts.get_stats(user_id)

    return render_template("profile.html", workouts=user_workouts, stats=user_stats)

def view_workout(id):
    workout = workouts.get_workout(id)
    if not workout:
        return redirect("/")
        
    comments = workouts.get_comments(id)
    return render_template("workout.html", workout=workout, comments=comments)

def add_comment(id):
    if "user_id" not in session:
        return redirect("/login")
        
    content = request.form["content"].strip()
    if content: # Validating that comment is not empty
        workouts.add_comment(id, session["user_id"], content)
        
    
    return redirect(f"/workout/{id}")