from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import time
import logging
import requests
from functools import wraps

import config
import login
import api_handlers
import course

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__, static_folder='/workspace')
CORS(app)

sessions = {}

def get_headers(token):
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        "token": token,
        "authToken": token,
        "siteId": "95",
        "Content-Type": "application/json",
    }

def _load_credentials_store():
    if not os.path.exists(config.CREDENTIALS_FILE):
        return {}
    try:
        with open(config.CREDENTIALS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        logging.error(f"加载凭证失败：{e}")
        return {}
    
    if not isinstance(data, dict):
        return {}
    
    if "loginName" in data and "token" in data:
        login_name = data["loginName"]
        return {login_name: data}
    
    return data

def _save_credentials_store(store):
    with open(config.CREDENTIALS_FILE, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)

def save_credentials(loginName, passWord, token):
    store = _load_credentials_store()
    store[loginName] = {
        "loginName": loginName,
        "passWord": passWord,
        "token": token,
        "timestamp": int(time.time()),
    }
    _save_credentials_store(store)
    logging.info(f"凭证已保存：{loginName}")

def get_saved_account(loginName):
    return _load_credentials_store().get(loginName)

def get_all_saved_accounts():
    store = _load_credentials_store()
    return list(store.values())

def check_login(token):
    url = "https://www.baomi.org.cn/laile-api/i/user/current"
    headers = get_headers(token)
    try:
        response = requests.get(url, headers=headers, timeout=10)
        logging.info(f"检查登录响应状态码：{response.status_code}")
        logging.info(f"检查登录响应内容：{response.text[:200]}")
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 200:
                return data["data"].get("nickname", "Unknown")
    except Exception as e:
        logging.error(f"检查登录失败：{e}")
    return None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    login_name = data.get('loginName')
    password = data.get('password')
    
    if not login_name or not password:
        return jsonify({"success": False, "message": "用户名和密码不能为空"}), 400
    
    try:
        result = login.login(login_name, password)
        if result and len(result) > 0:
            token = result
            save_credentials(login_name, password, token)
            sessions[login_name] = token
            
            nickname = check_login(token)
            return jsonify({
                "success": True,
                "message": "登录成功",
                "data": {
                    "loginName": login_name,
                    "nickname": nickname,
                    "token": token
                }
            })
        else:
            return jsonify({"success": False, "message": "登录失败，请检查账号密码是否正确。如多次失败，账号可能被临时锁定。"}), 401
    except Exception as e:
        logging.error(f"登录异常：{e}")
        error_msg = str(e)
        if "密码" in error_msg or "输错" in error_msg:
            full_msg = error_msg
        else:
            full_msg = f"登录失败：{str(e)}"
        return jsonify({"success": False, "message": full_msg}), 500

@app.route('/api/accounts', methods=['GET'])
def api_get_accounts():
    accounts = get_all_saved_accounts()
    valid_accounts = []
    for account in accounts:
        login_name = account.get("loginName")
        token = account.get("token")
        if login_name and token:
            nickname = check_login(token)
            if nickname:
                valid_accounts.append({
                    "loginName": login_name,
                    "nickname": nickname,
                    "label": account.get("label", "")
                })
    return jsonify({"success": True, "data": valid_accounts})

@app.route('/api/select-account', methods=['POST'])
def api_select_account():
    data = request.json
    login_name = data.get('loginName')
    
    if not login_name:
        return jsonify({"success": False, "message": "用户名不能为空"}), 400
    
    saved = get_saved_account(login_name)
    if saved and saved.get("token"):
        token = saved["token"]
        if check_login(token):
            sessions[login_name] = token
            return jsonify({
                "success": True,
                "message": "切换成功",
                "data": {
                    "loginName": login_name,
                    "token": token
                }
            })
    
    return jsonify({"success": False, "message": "账号不存在或 token 已过期"}), 400

@app.route('/api/course/list', methods=['GET'])
def api_course_list():
    token = request.headers.get('token')
    if not token:
        return jsonify({"success": False, "message": "未登录"}), 401
    
    try:
        headers = get_headers(token)
        course_packet_id = config.course_packet_id
        
        # 使用 portal/main-api/v2 而不是 laile-api
        url = "https://www.baomi.org.cn/portal/main-api/v2/coursePacket/getCourseDirectoryList"
        params = {
            "scale": 1,
            "coursePacketId": course_packet_id
        }
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        logging.info(f"课程目录响应状态码：{response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get("data"):
                    courses = data.get("data", [])
                    return jsonify({"success": True, "data": courses})
                else:
                    return jsonify({"success": False, "message": "未找到课程数据"}), 500
            except json.JSONDecodeError as je:
                logging.error(f"JSON 解析失败：{je}, 响应内容：{response.text[:200]}")
                return jsonify({"success": False, "message": "服务器返回了无效的响应格式"}), 500
        
        return jsonify({"success": False, "message": f"获取课程列表失败，状态码：{response.status_code}"}), 500
    except Exception as e:
        logging.error(f"获取课程列表失败：{e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/course/progress', methods=['GET'])
def api_course_progress():
    token = request.headers.get('token')
    if not token:
        return jsonify({"success": False, "message": "未登录"}), 401
    
    try:
        course_packet_id = config.course_packet_id
        url = f"https://www.baomi.org.cn/laile-api/i/newStudyMethod/studyRate?coursePacketId={course_packet_id}"
        headers = get_headers(token)
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 200:
                return jsonify({"success": True, "data": data.get("data", {})})
        
        return jsonify({"success": False, "message": "获取进度失败"}), 500
    except Exception as e:
        logging.error(f"获取进度失败：{e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/course/study', methods=['POST'])
def api_course_study():
    token = request.headers.get('token')
    if not token:
        return jsonify({"success": False, "message": "未登录"}), 401
    
    data = request.json
    lesson_id = data.get('lessonId')
    
    if not lesson_id:
        return jsonify({"success": False, "message": "课程 ID 不能为空"}), 400
    
    try:
        session = requests.Session()
        result = api_handlers.study_lesson(session, token, lesson_id)
        if result:
            return jsonify({"success": True, "message": "课程学习完成"})
        else:
            return jsonify({"success": False, "message": "学习失败"}), 500
    except Exception as e:
        logging.error(f"学习课程失败：{e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/course/study-all', methods=['POST'])
def api_course_study_all():
    token = request.headers.get('token')
    if not token:
        return jsonify({"success": False, "message": "未登录"}), 401
    
    try:
        course_packet_id = config.course_packet_id
        
        # 使用原始的 CourseManager
        session = requests.Session()
        manager = course.CourseManager(session, token)
        
        # 学习课程
        logging.info("开始学习课程...")
        study_result = manager.study_course(course_packet_id)
        logging.info(f"课程学习完成：{study_result}")
        
        # 完成考试
        logging.info("开始完成考试...")
        exam_result = manager.complete_exam(course_packet_id)
        logging.info(f"考试完成：{exam_result}")
        
        return jsonify({
            "success": True,
            "message": "课程学习和考试完成",
            "data": {
                "study": study_result,
                "exam": exam_result
            }
        })
        
    except Exception as e:
        logging.error(f"批量学习失败：{e}")
        import traceback
        logging.error(traceback.format_exc())
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/exam/submit', methods=['POST'])
def api_exam_submit():
    token = request.headers.get('token')
    if not token:
        return jsonify({"success": False, "message": "未登录"}), 401
    
    data = request.json
    lesson_id = data.get('lessonId')
    
    if not lesson_id:
        return jsonify({"success": False, "message": "课程 ID 不能为空"}), 400
    
    try:
        session = requests.Session()
        result = api_handlers.submit_exam(session, token, lesson_id)
        if result.get('success'):
            return jsonify({"success": True, "message": "考试提交成功", "data": result})
        else:
            return jsonify({"success": False, "message": result.get('message', '考试提交失败')}), 500
    except Exception as e:
        logging.error(f"提交考试失败：{e}")
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
