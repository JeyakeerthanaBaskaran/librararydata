from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.sqlite3'

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    book_name = db.Column(db.String)
    author = db.Column(db.String)

    def __init__(self,book,author):
        self.book_name = book
        self.author = author



@app.route('/add')
def addBook():
    return render_template('add.html')

@app.route('/')
def showBooks():
    return render_template('view.html',books = Book.query.all())

@app.route('/submit',methods=['POST'])
def submit():
    book = request.form.get('bookname')
    author = request.form.get('author')

    b = Book(book,author)
    db.session.add(b)
    db.session.commit()
   
    return redirect('/')

@app.route('/delete')
def delete():
    delete_id = request.args.get('id')
    book = Book.query.filter_by(id=delete_id).first()
    # Delete the book
    db.session.delete(book)
    # Save the changes in the database
    db.session.commit()
    # Redirect to home page to show the table of books
    return redirect('/')

@app.route('/edit')
def edit():
    # Get the value of id from GET Request
    id = request.args.get('id')
    # Fetch the book from the database using the id
    book = Book.query.filter_by(id=id).first()
    # Send details of book to edit page
    return render_template('edit.html',book=book)

@app.route('/modify',methods=['POST'])
def change():
    id = request.form.get('id')
    bookname = request.form.get('bookname')
    author = request.form.get('author')

    # Fetch the book from the database using the id
    book = Book.query.filter_by(id=id).first()
    
    # Edit the attributes of the book
    book.book_name = bookname
    book.author = author

    # Save the changes in the database
    db.session.commit()
    
    # Redirect to home page to show the table of books
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


