from flask import Blueprint, redirect, render_template, g, url_for

NAME = 'base'

bp = Blueprint(NAME, __name__)

@bp.route('/')
def index():
    if not g.user:
        return redirect(url_for('auth.login'))
    return render_template('index.html')