from flask import render_template, redirect, request
from flask_app import app
from flask_app.models.email import Email
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/process',methods=['POST'])
def process():
    if not Email.is_valid(request.form):
        return redirect('/')
    Email.save(request.form)
    return redirect('/results')


@app.route('/results')
def results():
    return render_template("results.html",emails=Email.get_all())

@app.route('/destroy/<int:id>')
def destroy_email(id):
    data = {
        "id": id
    }
    Email.destroy(data)
    return redirect('/results')

bcrypt = Bcrypt(app)
@app.route('/register/user', methods=['POST'])
def register():
    # validate the form here ...
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        "username": request.form['username'],
        "password" : pw_hash
    }
    # Call the save @classmethod on User
    user_id = User.save(data)
    # store user id into session
    session['user_id'] = user_id
    return redirect("/dashboard")
