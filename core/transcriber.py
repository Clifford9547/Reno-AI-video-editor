import os
import subprocess
import whisper

def extract_audio(video_path, audio_output):
    """
    用 ffmpeg 从视频中提取音频，输出为 WAV 格式。
    """
    cmd = [
        'ffmpeg', '-y', '-i', video_path,
        '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', audio_output
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    if result.returncode != 0:
        print("❌ 音频提取失败:", result.stderr)
        return False
    return True

def transcribe_audio(video_path):
    """
    从视频提取音频，调用 Whisper，返回带时间戳的转写结果（JSON）。
    """
    audio_output = f"{os.path.splitext(video_path)[0]}_audio.wav"
    if not extract_audio(video_path, audio_output):
        raise RuntimeError("音频提取失败")

    model = whisper.load_model("base")  # 你也可以换成 tiny/small/medium
    print("🟢 Whisper 模型加载成功，开始转写...")

    result = model.transcribe(audio_output, word_timestamps=True, verbose=True)
    print("✅ 转写完成！")
    return result
