from flask import Blueprint, request, jsonify
from llm.llm_manager import LLMManager

bp = Blueprint('llm', __name__, url_prefix='/api/llm')

@bp.route('/generate', methods=['POST'])
def generate_effects_script():
    data = request.get_json()
    provider = data.get('provider')
    model = data.get('model')
    api_key = data.get('api_key')
    prompt = data.get('prompt')

    if not all([provider, model, api_key, prompt]):
        return jsonify({'error': '缺少必要参数'}), 400

    llm = LLMManager(provider=provider, model=model, api_key=api_key)
    try:
        generated_script = llm.generate_text(prompt)
        return jsonify({
            'message': 'AI 生成成功',
            'script': generated_script
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
