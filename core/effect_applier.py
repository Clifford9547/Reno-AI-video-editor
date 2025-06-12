import os
import subprocess
import shutil
import re
from typing import List, Dict

def parse_fx_zoom_in(params_str):
    params = dict(re.findall(r'(\w+)=([\d\.]+)', params_str))
    start = params.get('start', '0')
    end = params.get('end', '0')
    final_zoom = params.get('final_zoom', '1.2')
    enable_expr = f"enable='between(t,{start},{end})'"
    return f"scale=iw*{final_zoom}:ih*{final_zoom},{enable_expr},crop=w:h:(in_w-w)/2:(in_h-h)/2"

def parse_fx_fade_out(params_str):
    params = dict(re.findall(r'(\w+)=([\d\.]+)', params_str))
    start = params.get('start', '0')
    end = params.get('end', '0')
    duration = str(float(end) - float(start))
    return f"fade=t=out:st={start}:d={duration}"

def apply_effects_ffmpeg(video_path: str, output_path: str, effects_list: List[Dict]):
    print("🔍 effects_list:", effects_list)
    current_video = video_path

    for idx, effect in enumerate(effects_list):
        start = effect.get('start', 0)
        end = effect.get('end', 0)
        code = effect.get('code', '').strip()
        e_type = effect.get('type')

        if not e_type:
            if code.startswith('drawtext='):
                e_type = 'text'
            elif '{FX_' in code:
                e_type = 'ai_fx'
            else:
                e_type = 'unknown'

        temp_output = f"{os.path.splitext(output_path)[0]}_temp_{idx}.mp4"

        try:
            if e_type == "text":
                drawtext = f"{code}:enable='between(t,{start},{end})'"
                cmd = [
                    'ffmpeg', '-y', '-i', current_video,
                    '-vf', drawtext,
                    '-c:v', 'libx264', '-c:a', 'copy', temp_output
                ]
                print(f"🎥 执行字幕特效[{idx}]：", " ".join(cmd))
                subprocess.run(cmd, check=True)
                current_video = temp_output

            elif e_type == "ai_fx":
                if '{FX_AUDIO' in code:
                    audio_match = re.search(r"path='([^']+)'", code)
                    if audio_match:
                        audio_path = audio_match.group(1)
                        cmd = [
                            'ffmpeg', '-y',
                            '-i', current_video, '-i', audio_path,
                            '-filter_complex', f"[0:a][1:a]amix=inputs=2:duration=longest:dropout_transition=2[aout]",
                            '-map', '0:v', '-map', '[aout]',
                            '-c:v', 'libx264', '-c:a', 'aac', temp_output
                        ]
                        print(f"🎵 执行音效混音[{idx}]：", " ".join(cmd))
                        subprocess.run(cmd, check=True)
                        current_video = temp_output

                elif '{FX_IMAGE' in code:
                    file_match = re.search(r"path='([^']+)'", code)
                    xy_match = re.findall(r"(\w+)=([\d]+)", code)
                    if file_match:
                        image_path = file_match.group(1)
                        x = next((v for k, v in xy_match if k == 'x'), '0')
                        y = next((v for k, v in xy_match if k == 'y'), '0')
                        cmd = [
                            'ffmpeg', '-y',
                            '-i', current_video, '-i', image_path,
                            '-filter_complex', f"[0:v][1:v]overlay={x}:{y}:enable='between(t,{start},{end})'",
                            '-c:v', 'libx264', '-c:a', 'copy', temp_output
                        ]
                        print(f"🖼️ 执行图片叠加[{idx}]：", " ".join(cmd))
                        subprocess.run(cmd, check=True)
                        current_video = temp_output

                elif '{FX_GREENSCREEN' in code:
                    file_match = re.search(r"path='([^']+)'", code)
                    if file_match:
                        gs_path = file_match.group(1)
                        cmd = [
                            'ffmpeg', '-y',
                            '-i', current_video, '-i', gs_path,
                            '-filter_complex', f"[1:v]colorkey=0x00FF00:0.3:0.2[fg];[0:v][fg]overlay=enable='between(t,{start},{end})'",
                            '-c:v', 'libx264', '-c:a', 'copy', temp_output
                        ]
                        print(f"🎥 执行绿幕合成[{idx}]：", " ".join(cmd))
                        subprocess.run(cmd, check=True)
                        current_video = temp_output

                else:
                    print(f"⚠️ 跳过未知 AI 特效: {code}")

            else:
                print(f"⚠️ 跳过未知特效类型: {e_type}")

        except subprocess.CalledProcessError as e:
            print(f"❌ 特效[{idx}] 失败，跳过。\n{e.stderr}")

    shutil.move(current_video, output_path)
    print("✅ 所有可用特效已处理，生成文件:", output_path)
