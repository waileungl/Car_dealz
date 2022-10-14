from flask_app import app
from flask import render_template,redirect,request, session, flash
from flask_app.models.login import Users
from flask_bcrypt import Bcrypt
from flask_app.models.cars import Cars

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods = ['POST'])
def register():
    if not Users.validate_registration(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    session["id"] = Users.register(data)
    session["user_name"] = f"{request.form['first_name']} {request.form['last_name']}"
    return redirect('/cars')

@app.route('/login', methods = ['POST'])
def login():
    data = {
        "email": request.form['login_email']
    }
    user = Users.validate_login(data)
    if not user:
        flash("Invalid Email/Password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.hash, request.form['login_password']):
        flash("Invalid Email/Password", "login")
        return redirect('/')
    session["id"] = user.id
    session["user_name"] = f"{user.first_name} {user.last_name}"
    return redirect("/cars")

@app.route('/cars')
def profile():
    if 'id' not in session:
        return redirect('/')
    data = {
        "id": session["id"]
    }
    return render_template('cars.html', dashboard_info = Cars.get_all_info_for_dashboard(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')