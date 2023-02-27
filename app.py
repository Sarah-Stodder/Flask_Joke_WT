from flask import Flask, g, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import json

class Config(): 
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(email, password):
    u = User.query.filter_by(email=email).first()
    if u is None:
        return False
    g.current_user = u
    return u.check_hashed_password(password)

joke_join = db.Table("joke_join",
    db.Column("joke_id",db.Integer, db.ForeignKey("joke.joke_id")),
    db.Column("User_id",db.Integer, db.ForeignKey("user.user_id"))
 )


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    user_jokes = db.relationship(
        "Joke",
        secondary=joke_join,
        backref="joke_join",
        lazy="dynamic",
        cascade ='all, delete-orphan',
        single_parent=True
        )


    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    
    def check_hashed_password(self, login_password):
        return check_password_hash(login_password)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def from_dict(self,data):
        self.email = data['email']
        self.password = self.hash_password(data['password'])

    def to_dict(self):
        return {"user_id" : self.user_id, "email" : self.email}
    
    def make_joke(self,post_joke):
        self.user_jokes.append(post_joke)
        db.session.commit()

    def remove_joke(self, jokes):
        for joke in jokes:
            self.user_jokes.remove(joke)
            db.session.commit()


class Joke (db.Model):
    joke_id= db.Column(db.Integer, primary_key=True)
    joke = db.Column(db.String)
    punchline = db.Column(db.String)
    


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def from_dict(self,data):
        self.joke= data['joke']
        self.punchline = data['punchline']

    def to_dict(self):
        return {"joke":self.joke, "punchline" : self.punchline}


#Routes
#Users
@app.post("/user")
def post_user():
    data = request.get_json()
    new_user = User()
    new_user.from_dict(data)
    new_user.save()
    return make_response("success", 200)

@app.get("/users")
def get_users():
    users = User.query.all()
    return make_response(json.dumps([user.to_dict() for user in users]), 200)

@app.get('/user/<id>')
def get_user_by_slug(id):
    user = User.query.filter_by(user_id=id).first()
    return make_response(json.dumps(user.to_dict()))

@app.put('/user/<id>')
def edit_user(id):
    data = request.get_json()
    user = User.query.filter_by(user_id=id).first()
    if user:
        user.from_dict(data)
        user.save()
        return make_response(f'Success!\n{json.dumps(user.to_dict())}')
    return make_response("User doesnt exist", 400)

@app.delete('/user/<id>')
def delete_user(id):
    user = User.query.filter_by(user_id=id).first()
    jokes = user.user_jokes.all()
    user.remove_joke(jokes)
    User.query.filter_by(user_id=id).delete()
    db.session.commit()
    return make_response("it might have worked?", 200)

#Jokes


@app.post('/joke/<id>') 
def post_jokes(id): 
    user = User.query.filter_by(user_id=id).first()
    data = request.get_json()
    new_joke = Joke()
    new_joke.from_dict(data)
    new_joke.save() 
    user.make_joke(new_joke)
    return make_response("success", 200)



@app.get('/jokes')
def get_jokes():
    jokes = Joke.query.all()
    return make_response(json.dumps([joke.to_dict() for joke in jokes]))

@app.get('/joke/<id>')
def get_joke(id):
    joke = Joke.query.filter_by(joke_id=id).first()
    return make_response(json.dumps(joke.from_dict()))


@app.post('/joke')
def post_joke():
    data = request.get_json()
    new_joke = Joke()
    new_joke.from_dict(data)
    new_joke.save()
    return make_response("success", 200)


@app.put('/joke/<id>')
def put_joke(id):
    data = request.get_json()
    joke = Joke.query.filter_by(joke_id=id).first()
    if joke:
        joke.from_dict(data)
        joke.save()
        return make_response(f"Success!\n{json.dumps(joke.to_dict())}", 200)
    return make_response("joke doesn't exist!", 400)

@app.delete("/joke/<id>")
def del_joke(id):
    Joke.query.filter_by(joke_id=id).delete()
    db.session.commit()
    return make_response("It might have worked?", 200)

@app.get('/user/<id>/jokes')
def get_users_jokes(id):
   user= (User.query.filter_by(user_id=id)).first()
   jokes = user.user_jokes.all()
   return make_response(json.dumps([joke.to_dict() for joke in jokes]))

