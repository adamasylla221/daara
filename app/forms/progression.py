from flask_wtf import FlaskForm #bibliothèques pour importer des formulaires Flask
from wtforms import StringField, SelectField, DateField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional


class ProgressionForm(FlaskForm):
    sourate = StringField("Sourate ", validators=[DataRequired()])
    nombre_versets = IntegerField(
        "Nombre de versets ", validators=[DataRequired(), NumberRange(min=0)]
    )
    date_evaluation = DateField("Date d'évaluation ", validators=[DataRequired()])
    observations = TextAreaField("Observations ", validators=[Optional()])

    talibe_matricule = SelectField("Talibé ", validators=[DataRequired()])

    submit = SubmitField("Enregistrer ")