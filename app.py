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
    infonote = db.Column(db.String(240))
    date = db.Column(db.DateTime)

class kabulet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    countof = db.Column(db.Integer())
    phonenum = db.Column(db.Integer(), unique=True)
    location = db.Column(db.String(30))
    infonote = db.Column(db.String(240))
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
    infonotte = request.form.get("usernote")
    if username and usercnt and userphone and userlocation:
        newuser = kalacakyer(
                username = username,
                countof = usercnt,
                phonenum = userphone,
                location = userlocation,
                infonote = infonotte,
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
    apprreq = request.form.get("approvereq")

    if apprreq:
        apreeq = sql.connect('kalacakyer.db')
        introcursor = apreeq.cursor()
        introcursor.row_factory = sql.Row
        introappsel = introcursor.execute(f"SELECT * FROM kalacakyer WHERE id = {apprreq} ").fetchall()
        apreeq.commit()
        #userid = introappsel[0]
        usernameapp = introappsel[0][1]
        usercount = introappsel[0][2]
        userphon = introappsel[0][3]
        userloc = introappsel[0][4]
        usernote = introappsel[0][5]

        newappr = kabulet(
                username = usernameapp,
                countof = usercount,
                phonenum = userphon,
                location = userloc,
                infonote = usernote,
                date = datetime.datetime.now(),
                )
        db.session.add(newappr)
        db.session.commit()

        introcursor.execute(f"DELETE FROM kalacakyer WHERE id = {apprreq} ;")
        apreeq.commit()

        return redirect(url_for("index"))

    ttlcount = []
    totalcount = introcursor.execute("SELECT countof FROM kabulet").fetchall()
    for i in totalcount:
        ttlcount.extend(i)
    countt = sum(map(int, ttlcount))

    return render_template('yerarayanlar.html', introappsel = introappsel, countt = countt)

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)