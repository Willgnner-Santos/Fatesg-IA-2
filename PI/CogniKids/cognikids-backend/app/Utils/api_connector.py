import os
import requests

API_BASE = os.environ.get('API_BASE', 'http://localhost:5001/api')


def _headers(token=None):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return headers


def update_student(token, student_id, student_data):
    """Faz PUT para /api/students/<student_id>"""
    url = f"{API_BASE}/students/{student_id}"
    r = requests.put(url, json=student_data, headers=_headers(token))
    return r


def delete_student(token, student_id):
    """Faz DELETE para /api/students/<student_id>"""
    url = f"{API_BASE}/students/{student_id}"
    r = requests.delete(url, headers=_headers(token))
    return r


def create_activity(token, activity_data):
    """POST /api/challenges"""
    url = f"{API_BASE}/challenges"
    r = requests.post(url, json=activity_data, headers=_headers(token))
    return r


def update_activity(token, challenge_id, data):
    """PUT /api/challenges/<challenge_id>"""
    url = f"{API_BASE}/challenges/{challenge_id}"
    r = requests.put(url, json=data, headers=_headers(token))
    return r


def delete_activity(token, challenge_id):
    """DELETE /api/challenges/<challenge_id>"""
    url = f"{API_BASE}/challenges/{challenge_id}"
    r = requests.delete(url, headers=_headers(token))
    return r
