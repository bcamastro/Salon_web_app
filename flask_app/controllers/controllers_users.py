from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.models_users import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    data = {
        'id':session['user_id']
    }
    print(session)
    return render_template("index.html", user=User.get_by_id(data))


@app.route('/services')
def load_service_page():
    return render_template("services.html")

@app.route('/about')
def load_about_page():
    return render_template("about.html")

@app.route('/contact')
def load_contact_page():
    return render_template("contact.html")

@app.route('/login_sign_up')
def login_register_page():
    return render_template("login_sign_up.html")

@app.route('/sign_up', methods =['POST'])
def register_account():
    if not User.registration_validation(request.form):
        return redirect("/login_sign_up")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "email": request.form["email"],
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "password": pw_hash
    }
    user_id = User.save(data)
    session["user_id"] = user_id
    return redirect("/")

@app.route('/login', methods = ['POST'])
def login():
    data = {"email" : request.form["email"]}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("invalid email or password",'login')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("invalid email or password",'login')
        return redirect("/")
    session['user_id'] = user_in_db.id
    return redirect('/')

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/login_sign_up')