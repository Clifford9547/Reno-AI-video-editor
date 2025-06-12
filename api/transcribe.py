import os
from flask import Blueprint, request, jsonify
from core.transcriber import transcribe_audio

bp = Blueprint('transcribe', __name__, url_prefix='/api/transcribe')

@bp.route('/', methods=['POST'])
def transcribe():
    data = request.get_json()
    video_path = data.get('video_path')
    if not video_path or not os.path.exists(video_path):
        return jsonify({'error': '无效的 video_path'}), 400

    try:
        result = transcribe_audio(video_path)
        # 只返回 segments，避免太大
        segments = result.get('segments', [])
        return jsonify({'segments': segments})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
