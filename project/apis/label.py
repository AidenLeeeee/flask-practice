from flask_restx import Namespace, fields
from project.models.labels import Label as LabelModel

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