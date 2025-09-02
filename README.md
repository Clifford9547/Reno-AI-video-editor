# Reno AI Video Editor | Reno AI 视频编辑器

## Overview | 概述
Reno AI Video Editor is a Flask-based service that uses AI to assist with video editing. It provides endpoints to upload media, transcribe audio with Whisper, generate editing prompts via large language models, and apply FFmpeg effects to produce a final video.

Reno AI 视频编辑器是一个基于 Flask 的服务，利用 AI 完成视频编辑流程。它提供接口用于上传素材、使用 Whisper 转写音频、通过大语言模型生成编辑脚本，并借助 FFmpeg 添加特效生成最终视频。

## Features | 功能特点
- 🗂️ Upload videos, images, audio, fonts and more through `/api/upload/`.
- 🔊 Transcribe audio tracks with Whisper via `/api/transcribe/`.
- ✍️ Generate detailed editing prompts from subtitles using `/api/prompt/generate`.
- 🤖 Connect to multiple LLM providers (OpenAI, Gemini, Deepseek) through `/api/llm/generate`.
- 🎬 Apply text, audio, image and green-screen effects with FFmpeg at `/api/video/apply_effects`.

- 🗂️ 通过 `/api/upload/` 上传视频、图片、音频、字体等素材。
- 🔊 通过 `/api/transcribe/` 使用 Whisper 转写音频。
- ✍️ 通过 `/api/prompt/generate` 根据字幕生成详细的编辑提示词。
- 🤖 使用 `/api/llm/generate` 连接不同的大语言模型（OpenAI、Gemini、Deepseek）。
- 🎬 通过 `/api/video/apply_effects` 调用 FFmpeg 添加字幕、音效、图片叠加和绿幕等特效。

## Installation | 安装
1. **Clone** the repository and create a Python environment.
   克隆代码仓库并创建 Python 环境。
2. **Install dependencies** (Flask, requests, whisper, ffmpeg etc.).
   安装依赖（Flask、requests、whisper、ffmpeg 等）。
   ```bash
   pip install -r requirements.txt  # 或按需手动安装
   ```
3. Make sure `ffmpeg` is installed and accessible on your system.
   确保系统已安装并可访问 `ffmpeg`。

## Usage | 使用方法
1. Start the service 启动服务:
   ```bash
   python run.py
   ```
2. Open `http://localhost:5000` in your browser to access the web interface.
   在浏览器中打开 `http://localhost:5000` 访问界面。
3. Use the API endpoints to upload media, transcribe, generate prompts and apply effects.
   使用 API 接口上传素材、转写字幕、生成提示词并添加特效。

## Project Structure | 项目结构
```
.
├── api/                 # Flask blueprints for uploading, transcription, LLM, effects
├── core/                # FFmpeg effect pipeline and Whisper transcriber
├── llm/                 # LLM manager and prompt generator
├── static/              # Frontend assets
├── user_uploads/        # Uploaded files
└── run.py               # Application entry point
```
项目结构如上。

## License | 许可证
This project is released under the MIT License.
本项目基于 MIT 许可证发布。
