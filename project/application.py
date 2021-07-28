from flask import Flask,render_template, request, session
# from flask.wrappers import Request
from operator import and_
from models import *
import os
from werkzeug.utils import redirect
import pandas as pd
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cbseenirjmcrfo:9d6eb7d9a9fe0d6cb660adcc3ff5c7ea4710c9ab387e648618fee3c40f824a24@ec2-52-2-118-38.compute-1.amazonaws.com:5432/den3pregbprqi9'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.secret_key = "any random string"
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    df = pd.read_csv('books.csv', index_col='isbn')
    for ind in df.index:
        try:
            b = Bookdetails(id=ind,title=df['title'][ind],author=df['author'][ind],year=str(df['year'][ind]))
            db.session.add(b)
        except Exception as e:
            print("pandas ind",e)
    db.session.commit()
    user = Bookdetails.query.all()
    return render_template("success.html",users=user)





@app.route("/home")
def demo():

    flag = False
    if 'email' in session:
        email = session['email']
        flag = True
        return render_template("mainpage.html",user=email,flag=True)

    return render_template("mainpage.html",flag = False)

    # return render_template("index.html")

@app.route("/forms", methods=["POST","GET"])
def forms():

    if(request.method=="GET"):
        return render_template("index.html")
    else:
        fname=request.form.get("fname")
        lname=request.form.get("lname")
        email=request.form.get("email")
        pwd=request.form.get("pwd")

        try:
            alreadyanuser = Users.query.filter(Users.email==email).first()
            
            if alreadyanuser.email != None:
                session['email'] = email
                return render_template("index.html",flag=True)               
        except:
            
            details=Users(firstname=fname,lastname=lname,email=email,pwd=pwd)
            session['email'] = email
            db.session.add(details)
            db.session.commit()
            
            
            return redirect('/home')

@app.route("/login", methods=["POST","GET"])
def login():
    if(request.method=="GET"):
        return render_template("loginpage.html")
    else:
        try:
            email=request.form.get("email")
            pwd=request.form.get("pwd")
            user=Users.query.filter(and_(Users.email==email, Users.pwd==pwd)).first()
            session['email'] = user.email
            return redirect('/home')
            
        except:
            return render_template("loginpage.html",flag=True)

@app.route("/logout",methods=["POST","GET"])
def logout():
    session.pop('email',None)
    return redirect('/home')

@app.route("/books",methods=["POST","GET"])
def books():
    
    # return f"{val} {searchname}"

    if request.method == "POST":
        val=request.form.get("books")
        searchname=request.form.get("searchname")
        # det = request.form.get("searchname")
        tag = '%'+searchname+'%'
        if(val=="all"):

            book1 = Bookdetails.query.filter(Bookdetails.id.ilike(tag)).all()
            book2 = Bookdetails.query.filter(Bookdetails.title.ilike(tag)).all()
            book3 = Bookdetails.query.filter(Bookdetails.author.ilike(tag)).all()
            book4 = Bookdetails.query.filter(Bookdetails.year.ilike(tag)).all()
            book = book1+book2+book3+book4
        elif(val=="id"):
           
            print("val=",val)
            book = Bookdetails.query.filter(Bookdetails.id.ilike(tag)).all()
        elif(val=="title"):
           
            print("val=",val)
            book = Bookdetails.query.filter(Bookdetails.title.ilike(tag)).all()
        elif(val=="author"):
           
            print("val=",val)
            book = Bookdetails.query.filter(Bookdetails.author.ilike(tag)).all()
        elif(val=="year"):
           
            print("val=",val)
            book = Bookdetails.query.filter(Bookdetails.year.ilike(tag)).all()
            # book=Bookdetails.query.filter_by(val)
        # print(book)
        email = session['email']
        flag = True
        return render_template("mainpage.html",email = email,flag = flag,books=book)
    else:
        return redirect('/home')

@app.route("/id/<id>",methods=["POST","GET"])
def id(id):
    # session.pop('email',None)
    # print()
    # id1=request.args.get("bookname")
    # books = Bookdetails.query.filter(Bookdetails.id==id).first()
    # # book = Bookdetails.query.get(Bookdetails.id==id).all()
    # # print(book.id)
    # return render_template("review.html",book=books,flag=True)
    # return f"isbn number {id} {book.id} {book.title} {book.author}"
    det = Bookdetails.query.filter(Bookdetails.id==id).all()
    reviews_display = reviews.query.filter(reviews.id==id).all()
    session['id'] = id
    flag_review = False
    if 'email' in session:
        email = session['email']
        try:
            existing_user = reviews.query.filter(and_(reviews.id==id,reviews.email==email)).first()
            if existing_user.email != None:
                flag_review = False
        except:
           
            flag_review = True
    
        return render_template('review.html',reviews=reviews_display,uname=email,flag_review=flag_review,flag=True,details=det)
    else:
        return render_template('review.html',reviews=reviews_display,flag_review=flag_review,flag=False,details=det)

@app.route("/review", methods=['POST','GET'])
def review():
    if request.method == 'GET':
        return render_template('review.html')
    else:
        review = request.form.get('review')
        rating = request.form.get('rating')
        email = session['email']
        id = session['id']
        # print("from /review , user= ",user," book = ",bookid)
        add_review = reviews(id=id,email=email,review=review,rating=int(rating))
        db.session.add(add_review)
        db.session.commit()
        det = Bookdetails.query.filter(Bookdetails.id==id).all()
        reviews_display = reviews.query.filter(reviews.id==id).all()
        return render_template('review.html', reviews=reviews_display, flag_review=False, uname=email, flag=True, details=det)


