import sqlite3
from flask import g

# Palauttaa yhteyden tietokantaan tai luo sen, jos sitä ei ole
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("database.db")
        # row_factory mahdollistaa sarakkeiden haun nimellä (esim. rivi["username"])
        g.db.row_factory = sqlite3.Row
    return g.db