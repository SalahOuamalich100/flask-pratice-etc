from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from datetime import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify

app = Flask(__name__ , template_folder='./app/templates/' , static_folder='./app/static/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:salah@localhost/test'
db = SQLAlchemy(app)

JWT_SECRET = 'test' 

def generate_user_token(email):
    encoded_jwt = jwt.encode({"email": email, "exp": datetime.datetime.utcnow() +       datetime.timedelta(days=365)}, JWT_SECRET, algorithm="HS256")

    return encoded_jwt

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            if not user.active:
                return jsonify({"message": "User not activated"}), 401
            else:
                token = generate_user_token(email)
                return jsonify({"message": "Login successful", "token": token.decode("utf-8")})
        else:
            return jsonify({"error": True, "message": "Invalid credentials"}), 401
    return render_template('login.html')
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first() 
        if user:    
            return redirect(url_for('register'))
        
        new_user = User(username=username, email=email, password=generate_password_hash(password))
        
        db.session.add(new_user)
        db.session.commit() 
        
        return redirect(url_for('login')) 
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
    
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


with app.app_context():
    db.create_all()
