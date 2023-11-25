from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from datetime import datetime


app = Flask(__name__ , template_folder='./app/templates/' , static_folder='./app/static/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:salah@localhost/test'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def list_users():
    users = User.query.all()
    print(users)  # Afficher les utilisateurs dans la console.
    return render_template('users.html', users=users)


if __name__ == '__main__':
    app.run(debug=True)
    
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
with app.app_context():
    existing_user = User.query.filter_by(username='user1').first()
    if existing_user is None:
        user = User(username='user1', email='user1@example.com', password='securepassword')
        db.session.add(user)
        db.session.commit()
    else:
        print("existing user")



