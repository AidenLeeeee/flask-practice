from project.models.memo import Memo as MemoModel
from project.models.user import User as UserModel
from flask_restx import Namespace, fields, Resource
from flask import g

ns = Namespace(
    'memos',
    description='Memo API'
)

memo = ns.model('Memo', {
    'id': fields.Integer(required=True, description='memo_num'),
    'user_id': fields.Integer(required=True, description='user_num'),
    'title': fields.String(required=True, description='memo_title'),
    'content': fields.String(required=True, description='memo_content'),
    'created_at': fields.DateTime(description='memo_created'),
    'updated_at': fields.DateTime(description='memo_updated'),
})


@ns.route('')
class MemoList(Resource):
    @ns.marshal_list_with(memo, skip_none=True)
    def get(self):
        '''Get All Memos'''
        data = MemoModel.query.join(
            UserModel,
            UserModel.id == MemoModel.user_id
        ).filter(
            UserModel.id == g.user.id
        ).order_by(
            MemoModel.created_at.desc()
        ).limit(10).all()
        return data
    

@ns.route('/<int:id>')
@ns.param('id', 'memo_num')
class Memo(Resource):
    @ns.marshal_list_with(memo, skip_none=True)
    def get(self, id):
        '''Get One Memo'''
        data = MemoModel.query.get_or_404(id)
        if g.user.id != data.user_id:
           ns.abort(403)
        return data 