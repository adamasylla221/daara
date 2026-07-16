from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extension import db
from app.models.talibe import Talibe
from app.models.classe import Classe
from app.forms.talibe import TalibeForm
from app.exceptions import TalibeIntrouvableException, TalibeDejaExistantException

bp_talibes = Blueprint('talibes', __name__, url_prefix='/talibes')


@bp_talibes.route('/')
def lister():
    q = request.args.get('q', '').strip()
    classe_code = request.args.get('classe', '').strip()
    query = Talibe.query
    if classe_code:
        query = query.filter_by(classe_code=classe_code)
    if q:
        query = query.filter(
            Talibe.nom.ilike(f'%{q}%') | Talibe.prenom.ilike(f'%{q}%')
        )
    talibes = query.order_by(Talibe.nom).all()
    classes = Classe.query.order_by(Classe.libelle).all()
    return render_template('talibes/liste.html',
                           talibes=talibes, classes=classes, q=q,
                           classe_code=classe_code)


@bp_talibes.route('/nouveau', methods=['GET', 'POST'])
def creer():
    form = TalibeForm()
    form.classe_code.choices = [
        (c.code, c.libelle) for c in Classe.query.order_by(Classe.libelle).all()
    ]
    if form.validate_on_submit():
        if db.session.get(Talibe, form.matricule.data):
            raise TalibeDejaExistantException(form.matricule.data)
        talibe = Talibe(
            matricule=form.matricule.data,
            prenom=form.prenom.data,
            nom=form.nom.data,
            date_naissance=form.date_naissance.data,
            nom_tuteur=form.nom_tuteur.data,
            telephone_tuteur=form.telephone_tuteur.data,
            classe_code=form.classe_code.data
        )
        db.session.add(talibe)
        db.session.commit()
        flash('Talibé ajouté avec succès.', 'success')
        return redirect(url_for('talibes.lister'))
    return render_template('talibes/formulaire.html', form=form, talibe=None)


@bp_talibes.route('/<matricule>/modifier', methods=['GET', 'POST'])
def modifier(matricule):
    talibe = db.session.get(Talibe, matricule)
    if not talibe:
        raise TalibeIntrouvableException(matricule)
    form = TalibeForm(obj=talibe)
    form.classe_code.choices = [
        (c.code, c.libelle) for c in Classe.query.order_by(Classe.libelle).all()
    ]
    if form.validate_on_submit():
        talibe.prenom = form.prenom.data
        talibe.nom = form.nom.data
        talibe.date_naissance = form.date_naissance.data
        talibe.nom_tuteur = form.nom_tuteur.data
        talibe.telephone_tuteur = form.telephone_tuteur.data
        talibe.classe_code = form.classe_code.data
        db.session.commit()
        flash('Talibé modifié avec succès.', 'success')
        return redirect(url_for('talibes.lister'))
    return render_template('talibes/formulaire.html', form=form, talibe=talibe)


@bp_talibes.route('/<matricule>/supprimer', methods=['POST'])
def supprimer(matricule):
    talibe = db.session.get(Talibe, matricule)
    if not talibe:
        raise TalibeIntrouvableException(matricule)
    db.session.delete(talibe)
    db.session.commit()
    flash('Talibé supprimé avec succès.', 'success')
    return redirect(url_for('talibes.lister'))


@bp_talibes.route('/exporter')
def exporter():
    q = request.args.get('q', '').strip()
    classe_code = request.args.get('classe', '').strip()
    query = Talibe.query
    if classe_code:
        query = query.filter_by(classe_code=classe_code)
    if q:
        query = query.filter(
            Talibe.nom.ilike(f'%{q}%') | Talibe.prenom.ilike(f'%{q}%')
        )
    talibes = query.order_by(Talibe.nom).all()
    entetes = ['matricule', 'prenom', 'nom', 'date_naissance', 'nom_tuteur',
               'telephone_tuteur', 'classe']
    lignes = [
        [t.matricule, t.prenom, t.nom,
         str(t.date_naissance) if t.date_naissance else '',
         t.nom_tuteur or '', t.telephone_tuteur or '',
         t.classe_code]
        for t in talibes
    ]
    from app.utils.csv_exporter import exporter_csv
    return exporter_csv('talibes.csv', entetes, lignes)