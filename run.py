from flask import Flask
from api.video import bp as video_bp
from api.upload import bp as upload_bp
from api.transcribe import bp as transcribe_bp
from api.prompt import bp as prompt_bp
from flask import send_from_directory
import os

from api.llm import bp as llm_bp

app = Flask(__name__)
app.config.from_pyfile('config.py')

from flask import send_file

@app.route('/download/<path:filename>')
def download_file(filename):
    file_path = os.path.join('processed_videos', filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "文件不存在", 404

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

# 注册蓝图
app.register_blueprint(video_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(transcribe_bp)
app.register_blueprint(prompt_bp)
app.register_blueprint(llm_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
