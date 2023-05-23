from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import UserForm, LoginForm
from app.models import User, Role
from app import db, flask_bcrypt
from flask_security import login_user, current_user, logout_user, login_required

user_bp = Blueprint('user_bp', __name__)

# Route pour la page de connexion
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Rediriger l'utilisateur déjà connecté vers une autre page
        return redirect(url_for('appartement_bp.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not flask_bcrypt.check_password_hash(user.password, form.password.data):
            flash('Identifiants incorrects', 'danger')
            return redirect(url_for('user_bp.login'))

        # login_user(user, remember=form.remember_me.data)
        login_user(user)
        flash('Connexion réussie', 'success')
        return redirect(url_for('appartement_bp.index'))
    return render_template('login.html', form=form)

@user_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user_bp.login'))

# Route pour la page de connexion
@user_bp.route('/index')
def index():
    return redirect(url_for('appartement_bp.index'))

@user_bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    # Récupérer tous les rôles disponibles
    roles = db.session.query(Role).all()
    # Trier les roles par nom
    roles_tries = sorted(roles, key=lambda x: x.name)
    form = UserForm()
    form.role.choices = [(role.id, role.name) for role in roles_tries]
    if form.validate_on_submit():
        # hashage password
        hashed_password = flask_bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Créer un nouvel utilisateur
        user = User(username=form.username.data, password=hashed_password, active=1)
        
        # Récupérer le rôle associé
        # role = db.session.get(Role, form.role.data)
        # Ajouter le rôle à l'utilisateur
        # user.user_roles.append(role)

        db.session.add(user)
        db.session.commit()
        # Message flash ok
        flash('L\'utilisateur a bien été créé', 'success')
        return redirect(url_for('user_bp.index'))
    return render_template('user/add.html', form=form, title='Ajouter un utilisateur', route='user_bp')
