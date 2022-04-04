from flask import Flask
from flask import request
from flask import render_template
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app():
    print('run: create_app()')
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'secretkey'
    
    if app.config['DEBUG']:
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = None
        
    ''' Routes INIT '''
    from project.routes import base_route, auth_route
    app.register_blueprint(base_route.bp)
    app.register_blueprint(auth_route.bp)
    
    ''' CSRF INIT '''
    csrf.init_app(app)
    
    @app.errorhandler(404)
    def page_404(error):
        return render_template('/404.html'), 404
    
    return app