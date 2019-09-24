import os
import requests

from flask import Flask, session, render_template, request
from flask_session import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
os.environ["DATABASE_URL"]='postgres://tgtnhaxxgotxjd:3a1e74426c6814e12e485bb992398a737e13eed72093b28cb53233a022f72b25@ec2-174-129-242-183.compute-1.amazonaws.com:5432/d6g54ari3aolfo'
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))

db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    #return "Project 1: TODO"
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "cG46cghUhz8fZwTxDxiwVQ", "isbns": "9781632168146"})
    return res.json()
@app.route("/Registration",methods=['GET','POST'])
def Registration():
    
    return render_template('Registration.html')
@app.route("/Login",methods=['GET','POST'])
def Login():
    #return request.method
    if request.method == 'POST':
        username=request.form['username']
        
        fullname=request.form['fullname']
        password=request.form['psw']
        query="INSERT INTO users (username, password, fullname) VALUES (:username,:password,:fullname)"
        #insert=(username, password, fullname)
        db.execute(query, {'username':username,'password':password,'fullname':fullname})
        db.commit()
    return render_template('Login.html')
@app.route("/Home",methods=['POST'])
def Home():
    username=request.form['username']
    password=request.form['psw']
    session['username'] = username
    query="SELECT username FROM users WHERE username=:username AND password=:password"
    user=db.execute(query, {'username':username, 'password':password}).fetchall()
    if (len(user)==0):
        return render_template('Login.html')
    else:
        return render_template('Home.html',username=username)
@app.route("/ShowRating",methods=['POST'])
def ShowRating():
    #return request.method
    book=request.form['books']
    searchkeyword=request.form['searchkeyword']
    if book=='year':
        query="SELECT * FROM books WHERE "+book+"=:searchkeyword"
    else:
        searchkeyword='%'+searchkeyword+'%'
        query="SELECT * FROM books WHERE "+book+" like :searchkeyword"
        #return query
    booklist=db.execute(query,{'searchkeyword':searchkeyword}).fetchall()
    #return booklist
    return render_template('Rating.html',booklist=booklist)
@app.route("/UpdateRating",methods=['POST'])
def UpdateRating():
    rating=request.form['rating']
    isbn=request.form['isbn']
    username=session['username']
    return username

if(__name__=="__main__"):
    app.run(debug=True,use_reloader=False)
