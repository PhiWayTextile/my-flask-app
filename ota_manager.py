from flask import Blueprint, request, jsonify, send_file
import json
import os

ota_bp = Blueprint('ota', __name__)
VERSIONS_FILE = 'data/versions.json'

def safe_json_load(file_path):
    '''安全地读取JSON文件，处理BOM问题'''
    try:
        # 方法1: 尝试无BOM读取
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except UnicodeDecodeError:
        # 方法2: 尝试带BOM读取
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                return json.load(f)
        except Exception as e:
            raise e
    except Exception as e:
        raise e

@ota_bp.route('/api/ota/check_update', methods=['POST'])
def check_update():
    '''检查更新接口'''
    try:
        client_data = request.json
        client_version = client_data.get('version', '1.0.0')
        
        print('收到更新检查请求，客户端版本: ' + client_version)
        
        # 读取版本数据库
        if os.path.exists(VERSIONS_FILE):
            versions = safe_json_load(VERSIONS_FILE)
        else:
            # 如果文件不存在，创建默认版本
            versions = {
                'latest': {
                    'version': '1.0.0',
                    'release_date': '2024-01-15',
                    'package': 'textile_vision_v1.0.0.zip',
                    'changelog': ['初始版本'],
                    'min_required_version': '1.0.0'
                }
            }
        
        latest_version = versions['latest']
        
        # 简单的版本比较
        def compare_versions(v1, v2):
            v1_parts = list(map(int, v1.split('.')))
            v2_parts = list(map(int, v2.split('.')))
            return (v1_parts > v2_parts) - (v1_parts < v2_parts)
        
        if compare_versions(client_version, latest_version['version']) < 0:
            return jsonify({
                'has_update': True,
                'latest_version': latest_version,
                'download_url': '/api/ota/download/' + latest_version['package']
            })
        
        return jsonify({'has_update': False, 'message': '已经是最新版本'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ota_bp.route('/api/ota/download/<package_name>')
def download_update(package_name):
    '''下载更新包'''
    try:
        package_path = os.path.join('ota_packages', package_name)
        if os.path.exists(package_path):
            return send_file(package_path, as_attachment=True)
        else:
            return jsonify({'error': '更新包不存在'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ota_bp.route('/api/ota/versions')
def get_versions():
    '''获取所有版本信息'''
    try:
        if os.path.exists(VERSIONS_FILE):
            versions = safe_json_load(VERSIONS_FILE)
            return jsonify(versions)
        else:
            return jsonify({'error': '版本文件不存在'})
    except Exception as e:
        return jsonify({'error': '读取版本文件失败: ' + str(e)}), 500
