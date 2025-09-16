from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from conf import *
import requests
import logging
import base64
import re

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_image():
	with open(IMAGE_PATH, 'rb') as f:
		return base64.b64encode(f.read()).decode()

def get_current_time(type='minute'): 
	now = datetime.now(ZoneInfo("Asia/Bangkok")) # format waktunya jadi gmt+7 WIB
	now = now - timedelta(days=1)
	if type == 'minute':# contoh formatnya : 18:44
		return now.strftime("%H:%M")
	elif type == 'year': # ccontoh formatnya : 2025-09-30
		return now.strftime("%Y-%m-%d")
	return False

def check_day_off()->bool:
	# return true kalau minggu dan sabtu
	now = datetime.now(ZoneInfo("Asia/Bangkok")) # format waktunya jadi gmt+7 WIB
	now = now.strftime("%A").lower()
	if now == 'sunday' or now == 'saturday':
		return True
	return False

def do_attendance(cookies, csrf_token):
	if check_day_off():
		logging.warning("Hari libur tidak perlu absen !")
		return False
	else:
		data = {
			'token' : csrf_token,
			'id_internship' : int(ID_INTERNSHIP),
			'nim' : int(USERNAME),
			'attendance_date' : get_current_time(type='year'),
			'attendance_type': 'Present',
			'check_in': CHECK_IN,
			'check_out':CHECK_OUT,
			'description': DESCRIPTION,
			'validation': "data:image/png;base64," + read_image()
		}
		response = requests.post(url=URL+'index.php?form=attendance&action=add_history', data=data, cookies=cookies)
		logging.info("add new attandance")
		return response 

def get_csrf_and_cookie():
	def filter_csrf(text_data: str):
		regex_pattern = r'<meta\s+name=["\']csrf-token["\']\s+content=["\']([^"\']+)["\']\s*/?>'
		csrf_token = re.search(regex_pattern, text_data)
		csrf_token = csrf_token.group(1).strip()
		return csrf_token
	
	#static var
	path_login = "index.php?form=new_student_login"
	path = 'index.php?page=student_identity'
	
	# request login
	r = requests.get(url=URL+path_login)
	cookies = r.cookies.get_dict()
	csrf_token = filter_csrf(r.text)
	data = {
		"nim": USERNAME,
		"password": PASSWORD,
		"token":csrf_token
	}
	r = requests.post(url=URL+path_login, data=data, cookies=cookies)
	if r.status_code == 200:
		logging.info(f"Login sukses: {USERNAME}")
	else:
		logging.error(f"Login failed: {USERNAME}")
		return False
	
	# get csrf_token after login (beda csrf token sama yang login nya)
	x = requests.get(url=URL+path, cookies=cookies)
	csrf_token = filter_csrf(x.text)
	return csrf_token, cookies


if __name__ == '__main__':
	csrf_token, cookies = get_csrf_and_cookie()
	resp = do_attendance(csrf_token=csrf_token, cookies=cookies)
	print(resp.status_code)