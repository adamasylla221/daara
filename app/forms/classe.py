from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class ClasseForm(FlaskForm):
    code = StringField("Code", validators=[DataRequired(), Length(max=50)])
    libelle = StringField("Libellé", validators=[DataRequired(), Length(max=150)])
    niveau = StringField("Niveau", validators=[Optional(), Length(max=50)])

    # Les choices sont alimentés dans la vue depuis Maitre.query
    # (jamais de saisie libre) : voir app/views/classe.py
    maitre_matricule = SelectField("Maître", validators=[DataRequired()])

    submit = SubmitField("Enregistrer")
