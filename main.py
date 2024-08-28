from flask import Flask, request, jsonify
from models import db, ma, FileItem, file_schema, files_schema
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# إعدادات قاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ربط كائنات قاعدة البيانات وMarshmallow مع التطبيق
db.init_app(app)
ma.init_app(app)

with app.app_context():
    db.create_all()
    print("Database tables created successfully.")

# تعريف route لاستقبال الصورة والفيديو من خلال الـ endpoint `/todo`
@app.route('/todo', methods=['POST'])
def add_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No file selected for uploading'}), 400

    if file:
        file_path = os.path.join(basedir, 'uploads', file.filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)
        
        # حفظ معلومات الملف في قاعدة البيانات
        new_file = FileItem(
            filename=file.filename,
            filetype=file.content_type,
            file_path=file_path
        )
        db.session.add(new_file)
        db.session.commit()
        
        return file_schema.jsonify(new_file)

# تعريف route للحصول على جميع الملفات
@app.route('/files', methods=['GET'])
def get_files():
    files = FileItem.query.all()
    return files_schema.jsonify(files)

# تشغيل التطبيق
if __name__ == '__main__':
    app.run(debug=True)
