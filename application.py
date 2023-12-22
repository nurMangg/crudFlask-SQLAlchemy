from flask import Flask, jsonify
from flask import request, render_template,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///crud.db"
db.init_app(app)

class crudUser(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    firstName: Mapped[str] = mapped_column(String, nullable=False)
    lastName: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    message: Mapped[str] = mapped_column(String, nullable=True)

with app.app_context():
    db.create_all()
    
@app.route('/')
def index():
    users = db.session.execute(db.select(crudUser).order_by(crudUser.id)).scalars()
    
    user_list = [{'id': user.id, 'firstName': user.firstName, 'lastName': user.lastName, 'email': user.email, 'message': user.message} for user in users]

    # return render_template('index.html', user=users)
    
    return jsonify(users=user_list)

@app.route('/user/add', methods=['GET','POST'])
def add_data():
    if request.method == 'GET':
        return render_template('addUser.html')
    
    if request.method == 'POST':
        user = crudUser(
            firstName=request.form['firstName'],
            lastName=request.form['lastName'],
            email=request.form['email'],
            message=request.form['message'],
        )
        
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('index'))

@app.route('/user/update/<id>', methods=['GET','POST', 'PUT'])
def update_data(id):
    if request.method == 'GET':
        user = db.session.execute(db.select(crudUser).filter_by(id=id)).scalar()
        return render_template('updateUser.html', user=user)
    
    if request.method == 'POST' or request.method == 'PUT':
        user = db.session.execute(db.select(crudUser).filter_by(id=id)).scalar()
        user.firstName = request.form['firstName']
        user.lastName = request.form['lastName']
        user.email = request.form['email']
        user.message = request.form['message']
        
        db.session.commit()
        
        return redirect(url_for('index'))
    
@app.route('/user/delete/<id>', methods=['POST', 'DELETE'])
def delete_data(id):
    user = db.session.execute(db.select(crudUser).filter_by(id=id)).scalar()
    db.session.delete(user)
    db.session.commit()
    
    return redirect(url_for('index'))
