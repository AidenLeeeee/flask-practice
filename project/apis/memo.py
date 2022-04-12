from distutils.command.upload import upload
from project.models.memo import Memo as MemoModel
from project.models.user import User as UserModel
from flask_restx import Namespace, fields, Resource, reqparse
from flask import g, current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os
import shutil

ns = Namespace(
    'memos',
    description='Memo API'
)

memo = ns.model('Memo', {
    'id': fields.Integer(required=True, description='memo_num'),
    'user_id': fields.Integer(required=True, description='user_num'),
    'title': fields.String(required=True, description='memo_title'),
    'content': fields.String(required=True, description='memo_content'),
    'linked_image': fields.String(required=False, description='memo_image'),
    'created_at': fields.DateTime(description='memo_created'),
    'updated_at': fields.DateTime(description='memo_updated'),
})

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, help='title', location='form')
parser.add_argument('content', required=True, help='content', location='form')
parser.add_argument('linked_image', required=False, type=FileStorage, help='memo_image', location='files')

put_parser = parser.copy()
put_parser.replace_argument('title', required=False, help='memo_title', location='form')
put_parser.replace_argument('content', required=False, help='memo_content', location='form')

get_parser = reqparse.RequestParser()
get_parser.add_argument('page', required=False, type=int, help='page_num', location='args')
get_parser.add_argument('needle', required=False, help='memo_needle', location='args')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {
               'jpg',
               'jpeg',
               'png',
               'gif'
           }

def random_word(length):
    import random, string
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def save_file(file):
    if file.filename == '':
        ns.abort(400)
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        relative_path = os.path.join(
        current_app.static_url_path[1:],    # /static -> static
            current_app.config['USER_STATIC_BASE_DIR'],    # static/user_images  
            g.user.user_id,    # static/user_images/{user_id}
            'memos',    # static/user_images/{user_id}/memos
            random_word(5),    # static/user_images/{user_id}/memos/{random:str}
            filename    # static/user_images/{user_id}/memos/{random:str}/{filename}
        )
        
        upload_path = os.path.join(
            current_app.root_path,
            relative_path
        )
        os.makedirs(
            os.path.dirname(upload_path),
            exist_ok=True
        )
        file.save(upload_path)
        return relative_path, upload_path
    else:
        ns.abort(400)
    

@ns.route('')
class MemoList(Resource):
    @ns.expect(get_parser)
    @ns.marshal_list_with(memo, skip_none=True)
    def get(self):
        '''Get All Memos'''
        args = get_parser.parse_args()
        page = args['page']
        needle = args['needle']
        per_page = 15
        
        base_query = MemoModel.query.join(
            UserModel,
            UserModel.id == MemoModel.user_id
        ).filter(
            UserModel.id == g.user.id
        )
        
        if needle:
            needle = f'%{needle}%'
            base_query = base_query.filter(
                MemoModel.title.ilike(needle) | MemoModel.content.ilike(needle)
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
        file = args['linked_image']
        if file:
            relative_path, _ = save_file(file)
            memo.linked_image = relative_path
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
        file = args['linked_image']
        if file:
            relative_path, upload_path = save_file(file)
            if memo.linked_image:
                origin_path = os.path.join(
                    current_app.root_path,
                    memo.linked_image
                )
                if origin_path != upload_path:
                    if os.path.isfile(origin_path):
                        shutil.rmtree(os.path.dirname(origin_path))
            memo.linked_image = relative_path
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


@ns.route('/<int:id>/image')
@ns.param('id')
class MemoImage(Resource):
    def delete(self, id):
        '''Delete Memo Image'''
        memo = MemoModel.query.get_or_404(id)
        if g.user.id != memo.user_id:
            ns.abort(403)
        if memo.linked_image:
            origin_path = os.path.join(
                current_app.root_path,
                memo.linked_image
            )
            if os.path.isfile(origin_path):
                shutil.rmtree(os.path.dirname(origin_path))
            memo.linked_image = None
            g.db.commit()
        return '', 204