from flask import Blueprint, request, jsonify, send_file, render_template
import json
import os
import sqlite3
from datetime import datetime
from werkzeug.utils import secure_filename

video_bp = Blueprint('video', __name__)
VIDEO_DB = 'data/videos.db'
UPLOAD_FOLDER = 'data/videos'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'wmv'}

# 确保目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_video_database():
    """初始化视频数据库"""
    conn = sqlite3.connect(VIDEO_DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            upload_time TEXT NOT NULL,
            file_size INTEGER,
            description TEXT,
            tags TEXT,
            used_in_training BOOLEAN DEFAULT FALSE
        )
    ''')
    conn.commit()
    conn.close()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 初始化数据库
init_video_database()

@video_bp.route('/upload_video', methods=['GET', 'POST'])
def upload_video():
    """视频上传页面和接口"""
    if request.method == 'POST':
        if 'video' not in request.files:
            return jsonify({'error': '没有选择文件'}), 400
        
        file = request.files['video']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            # 记录到数据库
            file_size = os.path.getsize(file_path)
            upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            description = request.form.get('description', '')
            tags = request.form.get('tags', '')
            
            conn = sqlite3.connect(VIDEO_DB)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO videos (filename, upload_time, file_size, description, tags)
                VALUES (?, ?, ?, ?, ?)
            ''', (filename, upload_time, file_size, description, tags))
            conn.commit()
            conn.close()
            
            return jsonify({
                'success': True,
                'message': f'视频 {filename} 上传成功',
                'filename': filename,
                'file_size': file_size
            })
    
    return render_template('upload_video.html')

@video_bp.route('/api/videos/list')
def list_videos():
    """获取视频列表API"""
    conn = sqlite3.connect(VIDEO_DB)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM videos ORDER BY upload_time DESC')
    videos = cursor.fetchall()
    conn.close()
    
    video_list = []
    for video in videos:
        video_list.append({
            'id': video[0],
            'filename': video[1],
            'upload_time': video[2],
            'file_size': video[3],
            'description': video[4],
            'tags': video[5],
            'used_in_training': bool(video[6])
        })
    
    return jsonify(video_list)

@video_bp.route('/api/videos/download/<filename>')
def download_video(filename):
    """下载视频文件"""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': '文件不存在'}), 404

@video_bp.route('/api/videos/new_since')
def get_new_videos():
    """获取新视频列表 - 供OTA系统调用"""
    last_check = request.args.get('last_check', '2000-01-01 00:00:00')
    
    conn = sqlite3.connect(VIDEO_DB)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM videos 
        WHERE upload_time > ? 
        ORDER BY upload_time DESC
    ''', (last_check,))
    new_videos = cursor.fetchall()
    conn.close()
    
    video_list = []
    for video in new_videos:
        video_list.append({
            'id': video[0],
            'filename': video[1],
            'upload_time': video[2],
            'file_size': video[3],
            'description': video[4],
            'tags': video[5]
        })
    
    return jsonify({
        'success': True,
        'new_videos': video_list,
        'total_count': len(video_list)
    })
