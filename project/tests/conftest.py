import sys

from requests import session
sys.path.append('.')

from project.configs import TestingConfig
from project import create_app, db
from project.models.user import User as UserModel
from project.models.memo import Memo as MemoModel
import pytest
import os


@pytest.fixture(scope='session')
def user_data():
    yield dict(
        user_id='tester',
        user_name='tester',
        password='tester'
    )
    
    
@pytest.fixture(scope='session')
def memo_data():
    yield dict(
        title='title',
        content='content',
    )
    

@pytest.fixture(scope='session')
def app(user_data, memo_data):
    app = create_app(TestingConfig())
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = UserModel(**user_data)
        db.session.add(user)
        db.session.flush()
        memo_data['user_id'] = user.id
        memo = MemoModel(**memo_data)
        db.session.add(memo)
        db.session.commit()
        yield app
        # delete test_client in db
        db.drop_all()
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace(
            'sqlite:///',
            ''
        )
        if os.path.isfile(db_path):
            os.remove(db_path)


@pytest.fixture(scope='session')
def client(app, user_data):
    with app.test_client() as client:
        # Add user_id to session
        with client.session_transaction() as session:
            session['user_id'] = user_data.get('user_id')
        yield client