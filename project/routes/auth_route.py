from flask import Blueprint, render_template, redirect, url_for, flash
from project.forms.auth_form import LoginForm, RegisterForm

NAME = 'auth'

bp = Blueprint(NAME, __name__, url_prefix='/auth')

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
        return f'{user_id} {password}'
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
        return f'{user_id} {user_name} {password} {repassword}'
        
    else:
        flash_form_errors(form)
    
    return render_template(f'{NAME}/register.html', form=form)
    
@bp.route('/logout')
def logout():
    return 'logout'

def flash_form_errors(form):
    for _, errors in form.errors.items():
        for e in errors:
            flash(e)
    