from flask import Blueprint, request, jsonify, current_app
from core.effect_applier import apply_effects_ffmpeg
import os
import uuid

bp = Blueprint('video', __name__, url_prefix='/api/video')

@bp.route('/apply_effects', methods=['POST'])
def apply_effects():
    """
    前端提交：
    {
        "video_path": "uploads/my_video.mp4",
        "effects_list": [
            {
                "start": 0.0,
                "end": 2.0,
                "type": "text",
                "params": {
                    "text": "你好世界",
                    "fontfile": "app/lib/fonts/simhei.ttf",
                    "fontcolor": "white",
                    "fontsize": 48,
                    "x": "(w-text_w)/2",
                    "y": "h-100",
                    "borderw": 4,
                    "bordercolor": "black",
                    "box": 1,
                    "boxcolor": "black@0.5"
                }
            },
            ...
        ]
    }
    """

    data = request.get_json()
    video_path = data.get('video_path')
    effects_list = data.get('effects_list')

    if not video_path or not effects_list:
        return jsonify({"error": "Missing video_path or effects_list"}), 400

    # 生成输出文件路径
    output_dir = os.path.join(current_app.config['PROCESSED_FOLDER'], str(uuid.uuid4()))
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'final_video.mp4')

    try:
        apply_effects_ffmpeg(video_path, output_path, effects_list)
        return jsonify({
            "message": "视频特效处理完成！",
            "output_path": output_path
        })
    except Exception as e:
        current_app.logger.error(f"生成视频失败: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
