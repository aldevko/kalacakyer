from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy
import datetime

"""
kodlarini pythonanywhere'e gönderirken database adreslemelerini bu şekilde yapmayi unutma;
flaskai klasor adin, onu da bu projede degistireceksin

app = Flask(__name__, static_folder="images")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ozelmiray/kalacak/kalacakyer.db'
db = SQLAlchemy(app)
"""

app = Flask(__name__, static_folder="images")
app.secret_key = 'kalaca'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/necati/Desktop/kalacak/kalacakyer.db'
db = SQLAlchemy(app)


class kalacakyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    countof = db.Column(db.Integer())
    phonenum = db.Column(db.Integer(), unique=True)
    location = db.Column(db.String(30))
    date = db.Column(db.DateTime)

with app.app_context():
    db.create_all()

@app.route("/", methods = ["GET","POST"])
def index():
    username = request.form.get("username")
    print(username)
    usercnt = request.form.get("usercount")
    print(usercnt)
    userphone = request.form.get("usertel")
    print(userphone)
    userlocation = request.form.get("userlocation")
    print(userlocation)
    if username and usercnt and userphone and userlocation:
        newuser = kalacakyer(
                username = username,
                countof = usercnt,
                phonenum = userphone,
                location = userlocation,
                date = datetime.datetime.now(),
                )
        db.session.add(newuser)
        db.session.commit()

    return render_template("index.html")

@app.route("/yerarayanlar", methods = ["GET","POST"])
def yerarayanlar():
    import sqlite3 as sql
    arayansorgu = sql.connect('kalacakyer.db')
    introcursor = arayansorgu.cursor()
    introcursor.row_factory = sql.Row
    introappsel = introcursor.execute(f"SELECT * FROM kalacakyer").fetchall()
    arayansorgu.commit()
    return render_template('yerarayanlar.html', introappsel = introappsel)

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)