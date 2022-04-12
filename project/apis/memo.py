from email import parser
from project.models.memo import Memo as MemoModel
from project.models.user import User as UserModel
from flask_restx import Namespace, fields, Resource, reqparse
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

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, help='title', location='form')
parser.add_argument('content', required=True, help='content', location='form')

put_parser = parser.copy()
put_parser.replace_argument('title', required=False, help='memo_title', location='form')
put_parser.replace_argument('content', required=False, help='memo_content', location='form')

get_parser = reqparse.RequestParser()
get_parser.add_argument('page', required=False, type=int, help='page_num', location='args')


@ns.route('')
class MemoList(Resource):
    @ns.expect(get_parser)
    @ns.marshal_list_with(memo, skip_none=True)
    def get(self):
        '''Get All Memos'''
        args = get_parser.parse_args()
        page = args['page']
        per_page = 15
        
        base_query = MemoModel.query.join(
            UserModel,
            UserModel.id == MemoModel.user_id
        ).filter(
            UserModel.id == g.user.id
        )
        
        pages = base_query.order_by(
            MemoModel.created_at.desc()
        ).paginate(
            page=page,
            per_page=per_page,
        )
        return pages.items
    
    @ns.expect(parser)
    @ns.marshal_list_with(memo, skip_none=True)
    def post(self):
        '''Create Memo'''
        args = parser.parse_args()
        memo = MemoModel(
            title=args['title'],
            content = args['content'],
            user_id = g.user.id
        )
        g.db.add(memo)
        g.db.commit()
        return memo, 201
    

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
    
    @ns.expect(put_parser)
    @ns.marshal_list_with(memo, skip_none=True)
    def put(self, id):
        '''Update Memo'''
        args = put_parser.parse_args()
        memo = MemoModel.query.get_or_404(id)
        if g.user.id != memo.user_id:
            ns.abort(403)
        if args['title'] is not None:
            memo.title = args['title']
        if args['content'] is not None:
            memo.content = args['content']
        g.db.commit()
        return memo
    
    def delete(self, id):
        '''Delete Memo'''
        memo = MemoModel.query.get_or_404(id)
        if g.user.id != memo.user_id:
            ns.abort(403)
        g.db.delete(memo)
        g.db.commit()
        return '', 204