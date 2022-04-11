from project.models.memo import Memo as MemoModel
from flask_restx import Namespace

ns = Namespace(
    'memos',
    description='Memo API'
)