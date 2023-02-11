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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/necati/Desktop/kalacak/kalacakyerlazim.db'
db = SQLAlchemy(app)


class kalacakyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    countof = db.Column(db.Integer())
    phonenum = db.Column(db.Integer())
    location = db.Column(db.String(30))
    emergency = db.Column(db.String(20))
    infonote = db.Column(db.String(240))
    date = db.Column(db.DateTime)

class kabulet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    countof = db.Column(db.Integer())
    phonenum = db.Column(db.Integer())
    location = db.Column(db.String(30))
    emergency = db.Column(db.String(20))
    infonote = db.Column(db.String(240))
    date = db.Column(db.DateTime)

class helperstable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    kind = db.Column(db.Integer())
    phonenum = db.Column(db.Integer())
    infonote = db.Column(db.String(240))
    location = db.Column(db.String(30))
    date = db.Column(db.DateTime)

with app.app_context():
    db.create_all()

@app.route("/", methods = ["GET","POST"])
def index():
    username = request.form.get("username")
    usercnt = request.form.get("usercount")
    userphone = request.form.get("usertel")
    userlocation = request.form.get("userlocation")
    infonotte = request.form.get("usernote")
    emergencyy = request.form.get("emergency")


    helperuser = request.form.get("helpername")
    helperkind = request.form.get("helperkind")
    helpertele = request.form.get("helpertel")
    helpernotee = request.form.get("helpernote")
    helperloc = request.form.get("helperlocation")

    if helperuser and helperkind and helpertele and helpernotee and helperloc:
        newhelper = helperstable(
                username = helperuser,
                kind = helperkind,
                phonenum = helpertele,
                infonote = helpernotee,
                location = helperloc,
                date = datetime.datetime.now(),
                )
        db.session.add(newhelper)
        db.session.commit()
    

    if username and usercnt and userphone and userlocation:
        newuser = kalacakyer(
                username = username,
                countof = usercnt,
                phonenum = userphone,
                location = userlocation,
                emergency = emergencyy,
                infonote = infonotte,
                date = datetime.datetime.now(),
                )
        db.session.add(newuser)
        db.session.commit()

    return render_template("index.html")

@app.route("/yerarayanlar", methods = ["GET","POST"])
def yerarayanlar():
    import sqlite3 as sql
    arayansorgu = sql.connect('kalacakyerlazim.db')
    introcursor = arayansorgu.cursor()
    introcursor.row_factory = sql.Row
    introappsels = introcursor.execute(f"SELECT * FROM kalacakyer ORDER BY location").fetchall()
    arayansorgu.commit()
    apprreq = request.form.get("approvereq")

    if apprreq:
        apreeq = sql.connect('kalacakyelazimr.db')
        introcursor = apreeq.cursor()
        introcursor.row_factory = sql.Row
        introappsel = introcursor.execute(f"SELECT * FROM kalacakyer WHERE id = {apprreq} ").fetchall()
        apreeq.commit()
        usernameapp = introappsel[0][1]
        usercount = introappsel[0][2]
        userphon = introappsel[0][3]
        userloc = introappsel[0][4]
        emergent = '112 ihbarı Yapildi'
        usernote = introappsel[0][5]

        newappr = kabulet(
                username = usernameapp,
                countof = usercount,
                phonenum = userphon,
                location = userloc,
                emergency = emergent,
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

    return render_template('yerarayanlar.html', introappsels = introappsels, countt = countt)

@app.route("/helpers", methods = ["GET","POST"])
def helpers():
    import sqlite3 as sql
    helpersorgu = sql.connect('kalacakyerlazim.db')
    introcursor = helpersorgu.cursor()
    introcursor.row_factory = sql.Row
    helpers = introcursor.execute(f"SELECT * FROM helperstable ORDER BY kind").fetchall()
    apprhelp = request.form.get("approvehelp")

    if apprhelp:
        introcursor.execute(f"DELETE FROM helperstable WHERE id = {apprhelp} ;")
        helpersorgu.commit()
        return redirect(url_for("helpers"))


    return render_template('helpers.html', helpers = helpers)

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)