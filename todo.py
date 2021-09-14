from flask import Flask, render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy


# ORM - Database bağlantısı
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////TodoApp/todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Veritanbanına Todo isimli tablo eklicez.
class Todo(db.Model):

    id = db.Column(db.Integer, primary_key=True) # Primary key true deyince otomatik bir şekilde artsın diyoruz.
    title = db.Column(db.String(80))#Max 80 Karakter
    complete  = db.Column(db.Boolean)
    # yani ya sıfır ya da bir True ya da False


@app.route('/')
def index():
    todos = Todo.query.all()#listenin içinden sözlükler

    return render_template("index.html",todos = todos)

@app.route('/complete/<string:id>')
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first()

    todo.complete = not todo.complete # daha kısa yazımı, her türlü tersine çeviriyor.
    """if todo.complete == True:
        todo.complete = False
    else:
        todo.complete =True"""
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete/<string:id>')
def delete(id):
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/add',methods=['POST']) #sadece posta izin vericez.
def addTodo():
    title = request.form.get('title')
    newTodo = Todo(title = title, complete = False)
    db.session.add(newTodo)
    db.session.commit()

    return redirect(url_for("index"))



if __name__ == "__main__":
    db.create_all() #Tüm classları tablo halinde ekliyor.
    app.run(debug=True)


