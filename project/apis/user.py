from flask import g, request, jsonify
from flask_restx import Namespace, Resource, abort, fields, reqparse
from project.models.user import User as UserModel
from werkzeug import security


ns = Namespace(
    'users',
    description='User API'
)

user = ns.model('User', {
    'id': fields.Integer(required=True, description='user_num'),
    'user_id': fields.String(required=True, description='user_id'),
    'user_name': fields.String(required=True, description='user_name'),
    'created_at': fields.DateTime(description='sign_in_date')
})

post_parser = reqparse.RequestParser()
post_parser.add_argument('user_id', required=True, help='user_id', location='form')
post_parser.add_argument('user_name', required=True, help='user_name', location='form')
post_parser.add_argument('password', required=True, help='user_password', location='form')

# /api/users
@ns.route('')
@ns.response(409, 'User Id already exists!')
@ns.deprecated
class UserList(Resource):
    @ns.marshal_list_with(user, skip_none=True)
    def get(self):
        """Get All Users"""
        data = UserModel.query.all()
        return data
    
    @ns.expect(post_parser)
    @ns.marshal_list_with(user, skip_none=True)
    def post(self):
        """Create User"""
        args = post_parser.parse_args()
        user_id = args['user_id']
        user = UserModel.find_one_by_user_id(user_id)
        if user:
            ns.abort(409)
        user = UserModel(
            user_id=user_id,
            user_name=args['user_name'],
            password=security.generate_password_hash(args['password'])
        )
        g.db.add(user)
        g.db.commit()
        return user, 201
    

# /api/users/{id}
@ns.route('/<int:id>')
@ns.param('id', 'user_num')
@ns.deprecated
class User(Resource):
    @ns.marshal_list_with(user, skip_none=True)
    def get(self, id):
        """Get One User"""
        data = UserModel.query.get_or_404(id)
        return data