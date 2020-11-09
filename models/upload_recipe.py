from models.base_model import BaseModel
import peewee as pw


class UploadRecipe(BaseModel):
    r_title = pw.CharField(unique=False)
    r_image_url = pw.TextField(null=True)
    r_cookingtime = pw.CharField(unique=False)
    r_serving = pw.CharField(unique=False)
    r_ingredient = pw.CharField(unique=False, max_length=20000)
    r_step = pw.CharField(unique=False, max_length=20000)
    r_about = pw.CharField(unique=False, max_length=20000)
    

