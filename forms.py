from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class InputForm(FlaskForm):
    motive = StringField('Motive',
                           validators=[DataRequired()])
    target_length = IntegerField('Target Length', default = 22,
                           validators=[DataRequired()])
    strand = StringField('Strand',
                           validators=[DataRequired()])
    lcp = IntegerField('Length of conserved sequence', default = 12,
                           validators=[DataRequired()])
    eds = IntegerField('Levenshtein Edit Distance', default = 2,
                           validators=[DataRequired()])
    gbk_file = FileField()
    submit = SubmitField('Submit')


