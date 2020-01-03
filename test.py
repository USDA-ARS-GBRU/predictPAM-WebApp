from flask import Flask, render_template, url_for, flash, redirect
from forms import InputForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route("/")
# @app.route("/home")
# def home():
#     return render_template('home.html', posts=posts)


@app.route("/input", methods=['GET', 'POST'])
def input_form():
    form = InputForm()
    return render_template('input.html', title='PAMform', form=form)
    # if form.validate_on_submit():
    #     if((form.strand == 'forward' or form.strand == 'reverse') 
    #         and (form.eds >= 0 and form.eds <= 5)):
    #         flash('Correct Data', 'success')
    #         # return redirect(url_for('submit.html'))
    

if __name__ == '__main__':
    app.run(debug=True)