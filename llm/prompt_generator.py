import os

def list_files_in_dir(folder_path: str) -> list:
    if not os.path.exists(folder_path):
        return []
    return sorted([
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ])

class PromptGenerator:
    def __init__(self):
        pass

    def generate_prompt(
        self,
        segments,
        theme: str,
        target_audience: str,
        video_purpose: str,
        user_config: dict
    ) -> str:
        # 拼接字幕文本
        transcript = ""
        for seg in segments:
            start = seg['start']
            end = seg['end']
            text = seg['text']
            transcript += f"[{start:.3f} - {end:.3f}] {text}\n"

        # 动态获取各素材文件
        material_dirs = {
            'bgm': 'user_uploads/bgm',
            'fonts': 'user_uploads/fonts',
            'greenscreen': 'user_uploads/greenscreen',
            'images': 'user_uploads/images',
            'sfx': 'user_uploads/sfx',
            'videos': 'user_uploads/videos'
        }

        materials = {key: list_files_in_dir(folder) for key, folder in material_dirs.items()}

        # 定义一个辅助函数，用于生成素材段落
        def format_files(category):
            files = materials.get(category, [])
            if files:
                return "\n".join([f"- {os.path.join('user_uploads', category, f)}" for f in files])
            else:
                return "- 无可用文件"

        # 生成 prompt
        prompt = f"""
你是一个专业的视频后期编辑 AI。以下是用户上传视频的转写脚本（带时间戳）：
---
{transcript}
---
视频主题: {theme}
目标人群: {target_audience}
视频用途: {video_purpose}

以下是 3 种可用的字幕样式（FFmpeg drawtext 格式）：
✅ 1 级字幕（普通字幕）:
drawtext=text='{{文本}}':fontfile='user_uploads/fonts/simhei.ttf':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=h-100:borderw=2:bordercolor=black:box=1:boxcolor=black@0.5
✅ 2 级字幕（小节标题）:
drawtext=text='{{小节标题}}':fontfile='user_uploads/fonts/simhei.ttf':fontcolor=yellow:fontsize=60:x=(w-text_w)/2:y=(h-text_h)/2:borderw=2:bordercolor=black:box=1:boxcolor=black@0.5
✅ 3 级字幕（阶段性标题）:
drawtext=text='{{阶段性标题}}':fontfile='user_uploads/fonts/simhei.ttf':fontcolor=cyan:fontsize=72:x=(w-text_w)/2:y=50:borderw=2:bordercolor=black:box=1:boxcolor=black@0.5

🎵 当 2 级或 3 级字幕出现时，**自动插入合适的音效**。以下是可用音效文件：
{format_files('sfx')}
示例：[3.000 - 5.000] {{FX_AUDIO(path='user_uploads/sfx/audio1.mp3', start=3.0, end=5.0)}}

🎶 以下是可用作背景音乐 (BGM) 的文件：
{format_files('bgm')}

🎥 以下是可用于绿幕特效的文件：
{format_files('greenscreen')}
示例：[10.000 - 20.000] {{FX_GREENSCREEN(path='user_uploads/greenscreen/gs1.mp4', start=10.0, end=20.0)}}

🖼️ 以下是可叠加在视频中的图片文件：
{format_files('images')}
示例：[5.000 - 8.000] {{FX_IMAGE(path='user_uploads/images/img1.png', start=5.0, end=8.0, x=100, y=50)}}


🔤 以下是可用的字体文件：
{format_files('fonts')}

⚠️ **输出要求**：
- 字幕：必须使用上面 3 个 drawtext 样式之一
- 其他特效用 {{FX_...}} 格式
- 每个片段都要有时间戳行头：
[start - end] drawtext=...
[start - end] {{FX_...}}
- 只输出最终可执行的特效脚本，不要包含任何多余解释
"""
        return prompt
