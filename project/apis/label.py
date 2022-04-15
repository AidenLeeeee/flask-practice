from flask_restx import Namespace, fields, reqparse, Resource
from flask import g
from project.models.labels import Label as LabelModel
from project.models.user import User as UserModel

ns = Namespace(
    'labels',
    description='Label API'
)

label = ns.model('Label', {
    'id': fields.Integer(required=True, description="label_num"),
    'user_id': fields.Integer(required=True, description="user_num"),
    'content': fields.String(required=True, description="label_content"),
    'created_at': fields.DateTime(description="label_created")
})

parser = reqparse.RequestParser()
parser.add_argument('content', required=True, type=str, help='label_content', location='form')

@ns.route('')
class LabelList(Resource):
    @ns.marshal_list_with(label, skip_none=True)
    def get(self):
        '''Get All Labels'''
        query = LabelModel.query.join(
            UserModel,
            UserModel.id == LabelModel.user_id
        ).filter(
            UserModel.id == g.user.id
        )
        
        return query.all()
        
    
    @ns.expect(parser)
    @ns.marshal_list_with(label, skip_none=True)
    def post(self):
        '''Create Label'''
        args = parser.parse_args()
        content = args['content']
        label = LabelModel.query.join(
            UserModel,
            UserModel.id == LabelModel.user_id
        ).filter(
            UserModel.id == g.user.id,
            LabelModel.content == content
        ).first()
        
        if label:
            ns.abort(409)
        
        label = LabelModel(
            content=content,
            user_id=g.user.id
        )
        
        g.db.add(label)
        g.db.commit()
        
        return label, 201
    
    
@ns.route('/<int:id>')
@ns.param('id', 'label_num')
class Label(Resource):
    def delete(self, id):
        '''Delete Label'''
        label = LabelModel.query.get_or_404(id)
        if label.user_id != g.user.id:
            ns.abort(403)
            
        g.db.delete(label)
        g.db.commit()
        
        return '', 204