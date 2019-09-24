import os
import requests
from flask import Flask, session,render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import pandas as pd
from multiprocessing import Pool
import time
os.environ["DATABASE_URL"] = 'postgres://tgtnhaxxgotxjd:3a1e74426c6814e12e485bb992398a737e13eed72093b28cb53233a022f72b25@ec2-174-129-242-183.compute-1.amazonaws.com:5432/d6g54ari3aolfo'
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
app = Flask(__name__)
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

start=time.time()

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#data=pd.read_csv('books.csv')
# query="create table books (isbn CHAR(30) PRIMARY KEY,title CHAR(30) NOT NULL,year  INT  NOT NULL,author CHAR(30) NOT NULL)"
# query='select * from books'
# print(db.execute(query).fetchall())
# db.commit()
def InsertData(l):
    isbn=l[0]
    title=l[1]
    author=l[2]
    year=l[3]
    query = "INSERT INTO books(isbn,title,author,year) VALUES (:isbn,:title,:author,:year)"
    db.execute(query,{'isbn':isbn,'title':title,'author':author,'year':year})
    db.commit()
if __name__=='__main__':
    count=0
    data=data.values.tolist()
    p = Pool()  # Pool tells how many at a time
    p.map(InsertData, data)
    p.close()
    p.join()
end=time.time()
print(end-start)
# print(data[:5])
# for i in range(123,len(data)):
# if(len(db.execute('select isbn from books where isbn=:isbn',{'isbn':isbn}).fetchall())!=0):
        


