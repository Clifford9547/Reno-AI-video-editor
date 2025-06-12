import os

UPLOADS_ROOT = os.path.join(os.getcwd(), 'user_uploads')
UPLOADS_FOLDERS = {
    'video': os.path.join(UPLOADS_ROOT, 'videos'),
    'image': os.path.join(UPLOADS_ROOT, 'images'),
    'bgm': os.path.join(UPLOADS_ROOT, 'bgm'),
    'sfx': os.path.join(UPLOADS_ROOT, 'sfx'),
    'font': os.path.join(UPLOADS_ROOT, 'fonts'),
    'greenscreen': os.path.join(UPLOADS_ROOT, 'greenscreen'),
}

ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv', 'mp3', 'wav', 'jpg', 'png', 'ttf', 'otf'}
PROCESSED_FOLDER = os.path.join(os.getcwd(), 'processed_videos')
