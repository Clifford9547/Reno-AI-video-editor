import os
import uuid
from flask import Blueprint, request, jsonify, current_app

bp = Blueprint('upload', __name__, url_prefix='/api/upload')

@bp.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'type' not in request.form:
        return jsonify({'error': '缺少 file 或 type'}), 400

    file = request.files['file']
    file_type = request.form['type'].lower()

    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400

    # 校验文件类型和保存目录
    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext not in current_app.config['ALLOWED_EXTENSIONS']:
        return jsonify({'error': '不支持的文件格式'}), 400

    save_dir = current_app.config['UPLOADS_FOLDERS'].get(file_type)
    if not save_dir:
        return jsonify({'error': f'未知文件类型: {file_type}'}), 400

    os.makedirs(save_dir, exist_ok=True)
    filename = f"{uuid.uuid4()}.{ext}"
    save_path = os.path.join(save_dir, filename)
    file.save(save_path)

    return jsonify({
        'message': '文件上传成功',
        'path': os.path.relpath(save_path, os.getcwd())
    })
