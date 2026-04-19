from flask import Flask, g
import routes

app = Flask(__name__)
app.secret_key = "treenipaivakirja_salaisuus"

# Flask ajaa tämän funktion automaattisesti jokaisen sivulatauksen päätteeksi
@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Reititykset ohjataan routes.py -tiedostoon
app.add_url_rule("/", view_func=routes.index)
app.add_url_rule("/register", view_func=routes.register, methods=["GET", "POST"])
app.add_url_rule("/login", view_func=routes.login, methods=["GET", "POST"])
app.add_url_rule("/logout", view_func=routes.logout)
app.add_url_rule("/new", view_func=routes.new_workout, methods=["GET", "POST"])
app.add_url_rule("/delete/<int:id>", view_func=routes.delete_workout, methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True)