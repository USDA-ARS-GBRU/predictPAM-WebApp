from flask import Flask, flash, request, redirect, url_for, render_template
from forms import InputForm
from werkzeug.utils import secure_filename
import os
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

UPLOAD_FOLDER = '/templates'
#ALLOWED_EXTENSIONS = {'gbk','txt'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


# @app.route("/")

@app.route("/", methods=['GET', 'POST'])
def input():
    form = InputForm()
    if form.validate_on_submit():
        if form.strand.data == 'forward' or form.strand.data == 'reverse':
            flash('Correct Inputs!', 'success')
            return redirect(url_for('submit'))
        else:
            flash('Incorrect Data. Please check', 'danger')
    return render_template('input.html', title='PAMform', form=form)

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    return render_template('submit.html', title='Output')

@app.route("/abcd", methods=['GET', 'POST'])
def abcd():
    if 'file' not in request.files:
        print("hai")
        print(request.files)
        # flash('No file part')
        file = request.files['file']
        print(file.filename)
        return redirect(request.url)
    else:
        print("nahi hai")
    return render_template('abd.html', title='Output')

# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.email.data == 'admin@blog.com' and form.password.data == 'password':
#             flash('You have been logged in!', 'success')
#             return redirect(url_for('home'))
#         else:
#             flash('Login Unsuccessful. Please check username and password', 'danger')
#     return render_template('login.html', title='Login', form=form)

# 

if __name__ == '__main__':
    app.run(debug=True)
