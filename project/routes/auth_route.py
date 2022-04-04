from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from project.forms.auth_form import LoginForm, RegisterForm

NAME = 'auth'

bp = Blueprint(NAME, __name__, url_prefix='/auth')

"""only for testing"""
from dataclasses import dataclass
USERS = []

@dataclass
class User:
    """
        class User:
            def __init__(self, user_id, user_name, password):
                self.user_id = user_id
                self.user_name = user_name
                self.password = password
    """
    user_id: str
    user_name: str
    password: str
    
    
USERS.append(User('aiden', 'aiden', '1234'))
USERS.append(User('admin', 'admin', '1234'))
USERS.append(User('tester', 'tester', '1234'))


@bp.route('/')
def index():
    return redirect(url_for(f'{NAME}.login'))
    

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    # POST, validate OK!
    if form.validate_on_submit():
        user_id = form.data.get('user_id')
        password = form.data.get('password')
        user = [user for user in USERS if user.user_id == user_id]
        if user:
            user = user[0]
            if user.password != password:
                flash('Password is not valid.')
            else:
                session['user_id'] = user_id
                return redirect(url_for('base.index'))
        else:
            flash('User ID does not exist.')   
    else:
        flash_form_errors(form)
        
    return render_template(f'/{NAME}/login.html', form=form)
        
        
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    # POST, validate OK!
    if form.validate_on_submit():
        user_id = form.data.get('user_id')
        user_name = form.data.get('user_name')
        password = form.data.get('password')
        repassword = form.data.get('repassword')
        user = [user for user in USERS if user.user_id == user_id]
        if user:
            flash('User ID already exists.')
            return redirect(request.path)
        else:
            USERS.append(
                User(
                    user_id=user_id,
                    user_name=user_name,
                    password=password,
                )
            )
            session['user_id'] = user_id
            return redirect(url_for('base.index'))
    else:
        flash_form_errors(form)
    
    return render_template(f'{NAME}/register.html', form=form)
    
    
@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for(f'{NAME}.login'))


def flash_form_errors(form):
    for _, errors in form.errors.items():
        for e in errors:
            flash(e)
    