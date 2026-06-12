import time
import logging
import urllib.parse
from colorama import Fore, Style
import requests

def study_lesson(session, token, lesson_id):
    """学习单个课程 - 使用 portal/main-api"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        "token": token,
        "authToken": token,
        "siteId": "95",
        "Content-Type": "application/json",
    }

    try:
        logging.info(f"{Fore.GREEN}开始学习课程：{lesson_id}{Style.RESET_ALL}")
        
        current_time = int(time.time() * 1000)
        
        # 使用 portal/main-api 的 API
        url = "https://www.baomi.org.cn/portal/main-api/v2/studyTime/saveStudyTimeNew.do"
        data = {
            "courseId": lesson_id,
            "resourceId": lesson_id,
            "resourceDirectoryId": lesson_id,
            "resourceLength": 3600,
            "studyLength": 3600,
            "studyTime": 3600,
            "startTime": current_time - 3600000,
            "resourceName": "课程学习",
            "resourceType": "1",
            "resourceLibId": "3",
        }
        
        response = session.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        if result and result.get("status") == 0:
            logging.info(f"{Fore.GREEN}课程学习完成：{lesson_id}{Style.RESET_ALL}")
            return True
        else:
            logging.error(f"{Fore.RED}课程学习失败：{lesson_id}, 响应：{result}{Style.RESET_ALL}")
            return False
            
    except Exception as e:
        logging.error(f"{Fore.RED}学习课程异常：{e}{Style.RESET_ALL}")
        return False

def study_single_resource(session, token, course_id, resource_id, directory_id, resource_name, resource_length):
    """学习单个资源"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        "token": token,
        "authToken": token,
        "siteId": "95",
        "Content-Type": "application/json",
    }

    try:
        current_time = int(time.time() * 1000)
        
        url = "https://www.baomi.org.cn/portal/main-api/v2/studyTime/saveStudyTimeNew.do"
        data = {
            "courseId": course_id,
            "resourceId": resource_id,
            "resourceDirectoryId": directory_id,
            "resourceLength": resource_length,
            "studyLength": resource_length,
            "studyTime": resource_length,
            "startTime": current_time - (resource_length * 1000),
            "resourceName": urllib.parse.quote(resource_name),
            "resourceType": "1",
            "resourceLibId": "3",
        }
        
        response = session.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        if result and result.get("status") == 0:
            logging.info(f"{Fore.GREEN}资源学习完成：{resource_name}{Style.RESET_ALL}")
            return True
        else:
            logging.error(f"{Fore.RED}资源学习失败：{resource_name}, 响应：{result}{Style.RESET_ALL}")
            return False
            
    except Exception as e:
        logging.error(f"{Fore.RED}学习资源异常：{e}{Style.RESET_ALL}")
        return False

def submit_exam(session, token, lesson_id):
    """提交考试"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        "token": token,
        "authToken": token,
        "siteId": "95",
        "Content-Type": "application/json",
    }
    
    try:
        logging.info(f"{Fore.GREEN}开始提交考试：{lesson_id}{Style.RESET_ALL}")
        
        import hashlib
        import json
        import random
        
        def generate_custom_random_id():
            base_string = f"founder{random.randint(1, 500)}"
            md5_hash_object = hashlib.md5()
            md5_hash_object.update(base_string.encode("utf-8"))
            return md5_hash_object.hexdigest()
        
        random_id = generate_custom_random_id()
        
        url = "https://www.baomi.org.cn/portal/main-api/v2/coursePacket/getCourseRelateExam"
        params = {"coursePacketId": lesson_id, "token": token}
        response = session.get(url, headers=headers, params=params)
        exam_info = response.json()
        
        if not exam_info or not exam_info.get("data"):
            return {"success": False, "message": "未找到考试信息"}
        
        exam_id = exam_info["data"][0].get("examId")
        if not exam_id:
            return {"success": False, "message": "考试 ID 不存在"}
        
        url = "https://www.baomi.org.cn/portal/main-api/v2/activity/exam/getExamContentData.do"
        params = {"examId": exam_id, "randomId": random_id}
        response = session.get(url, headers=headers, params=params)
        exam_paper = response.json()
        
        if not exam_paper or not exam_paper.get("data"):
            return {"success": False, "message": "获取试卷失败"}
        
        random_id = exam_paper["data"].get("randomId", random_id)
        answers = []
        
        for type_item in exam_paper["data"].get("typeList", []):
            for question in type_item.get("questionList", []):
                correct_answer = question["answer"]
                answers.append({
                    "answer": correct_answer,
                    "parentId": "0",
                    "qstId": question["id"],
                    "resultFlag": 0,
                    "standardAnswer": correct_answer,
                    "subCount": 0,
                    "tqId": question["tqId"],
                    "userAnswer": correct_answer,
                    "userScoreRate": "100%",
                    "viewTypeId": type_item.get("type", 1),
                })
        
        start_date = time.strftime("%Y-%m-%d %H:%M:%S")
        
        url = "https://www.baomi.org.cn/portal/main-api/v2/activity/exam/saveExamResultJc.do"
        data = {
            "examId": exam_id,
            "examResult": json.dumps(answers),
            "randomId": random_id,
            "startDate": start_date,
        }
        response = session.post(url, headers=headers, json=data)
        result = response.json()
        
        if result and result.get("status") == 0:
            logging.info(f"{Fore.GREEN}考试提交成功{Style.RESET_ALL}")
            
            url = "https://www.baomi.org.cn/portal/main-api/v2/studyTime/updateCoursePackageExamInfo.do"
            params = {
                "courseId": lesson_id,
                "orgId": "",
                "isExam": 1,
                "isCertificate": 0,
                "examResult": 100,
                "token": token,
            }
            response = session.get(url, headers=headers, params=params)
            
            return {"success": True, "message": "考试完成", "score": 100}
        else:
            return {"success": False, "message": "考试提交失败"}
            
    except Exception as e:
        logging.error(f"{Fore.RED}考试异常：{e}{Style.RESET_ALL}")
        return {"success": False, "message": str(e)}
