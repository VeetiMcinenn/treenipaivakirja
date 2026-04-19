from flask import Flask, g
from flask_wtf.csrf import CSRFProtect
import routes
import os

app = Flask(__name__)
# CSFR key
app.secret_key = "treenipaivakirja_salaisuus_123" 

# OTETAAN SUOJAUS KÄYTTÖÖN
csrf = CSRFProtect(app) 

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Reitit pysyvät samoina
app.add_url_rule("/", view_func=routes.index)
app.add_url_rule("/register", view_func=routes.register, methods=["GET", "POST"])
app.add_url_rule("/login", view_func=routes.login, methods=["GET", "POST"])
app.add_url_rule("/logout", view_func=routes.logout)
app.add_url_rule("/new", view_func=routes.new_workout, methods=["GET", "POST"])
app.add_url_rule("/delete/<int:id>", view_func=routes.delete_workout, methods=["POST"])
app.add_url_rule("/profile", view_func=routes.profile)
app.add_url_rule("/workout/<int:id>", view_func=routes.view_workout)
app.add_url_rule("/workout/<int:id>/comment", view_func=routes.add_comment, methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True)