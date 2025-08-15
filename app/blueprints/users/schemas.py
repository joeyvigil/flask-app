from app.extensions import ma
from app.models import Users

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users #Creates a schema that validates that data defined in our user model
        
user_schema = UserSchema() #Creating an instance off my schema that can actually validate, Serialize and deserialize data
users_schema = UserSchema(many=True)