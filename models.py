from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# إعدادات قاعدة البيانات
db = SQLAlchemy()
ma = Marshmallow()

# تعريف نموذج FileItem لتخزين المعلومات المتعلقة بالملفات
class FileItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filetype = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)

    def __init__(self, filename, filetype, file_path):
        self.filename = filename
        self.filetype = filetype
        self.file_path = file_path

# تعريف الـ schema لـ FileItem
class FileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FileItem
        load_instance = True

# إنشاء كائنات الـ schema
file_schema = FileSchema()
files_schema = FileSchema(many=True)
