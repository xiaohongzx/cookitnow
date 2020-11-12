from models.base_model import BaseModel
from models.user import User
import peewee as pw


class Favourite(BaseModel):
    user = pw.ForeignKeyField(User, backref="favourite", on_delete="CASCADE")
    recipe_id = pw.TextField(null=False)
    

