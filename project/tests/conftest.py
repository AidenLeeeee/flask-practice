import sys
sys.path.append('.')

from project.configs import TestingConfig
from project import create_app
import pytest


@pytest.fixture
def client():
    app = create_app(TestingConfig())
    
    with app.test_client() as client:
        yield client