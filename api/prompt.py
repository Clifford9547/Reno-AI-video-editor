from flask import Blueprint, request, jsonify
from llm.prompt_generator import PromptGenerator

bp = Blueprint('prompt', __name__, url_prefix='/api/prompt')

@bp.route('/generate', methods=['POST'])
def generate_prompt():
    data = request.get_json()
    segments = data.get('segments')
    theme = data.get('theme', '')
    target_audience = data.get('target_audience', '')
    video_purpose = data.get('video_purpose', '')
    user_config = data.get('user_config', {})

    if not segments:
        return jsonify({'error': '缺少字幕 segments'}), 400

    pg = PromptGenerator()
    prompt = pg.generate_prompt(
        segments=segments,
        theme=theme,
        target_audience=target_audience,
        video_purpose=video_purpose,
        user_config=user_config
    )

    return jsonify({'prompt': prompt})
