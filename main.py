import os
import sys
import re
from urllib import urlretrieve
from selenium import webdriver
from getpass import getpass
from selenium.webdriver.common.keys import Keys

try:
	from configparser import SafeConfigParser
except ImportError:
	from ConfigParser import SafeConfigParser

chrome_options = webdriver.ChromeOptions()
path = "/home/ravinder/Downloads/chromedriver"
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(path,chrome_options = chrome_options)
driver.set_window_size(1080,800)  #Required, removes the "element not found" bug

try:
	input = raw_input
except NameError:
	pass

def clear():
	if os.name == 'nt':
		os.system('cls')
	else : 
		os.system('clear')

def sendBirthdayWish():
	driver.implicitly_wait(10)
	element = driver.find_elements_by_css_selector('._4-u2._tzh._fbBirthdays__todayCard._4-u8')[0]
	element = element.find_elements_by_css_selector('._tzm._fbBirthdays__todayItem')
	for i in element:
		command = i.find_elements_by_css_selector('.enter_submit.uiTextareaNoResize.uiTextareaAutogrow.uiStreamInlineTextarea.inlineReplyTextArea.mentionsTextarea.textInput')
		text="Happpppiiieee Birthhhhday :)"
		command[0].send_keys(text)
		command[0].send_keys(Keys.ENTER)
		
def init():
	cont = False
	clear()

	credentials_from_file = False

	credentials = SafeConfigParser();

	if os.path.isfile('settings.txt') and os.name != 'nt':
		os.system('chmod +r settings.txt')

	credentials.read('settings.txt')
	if (credentials.has_option('main','email') 
		  and credentials.has_option('main','password')):
		credentials_from_file = True

	while not cont:
		driver.get('https://www.facebook.com/')
	
		if credentials_from_file:
			email = credentials.get('main', 'email')
			password = credentials.get('main', 'password')
		else:
			email = input('Email : ')
			password = getpass('Password : ')

		inputs=driver.find_elements_by_tag_name('input')
		inputs[1].send_keys(email)
		inputs[2].send_keys(password)
		driver.implicitly_wait(10)
		inputs[3].click()

		if str(driver.current_url).split('=')[0] == 'https://www.facebook.com/login.php?login_attempt':
			clear()
			print('Invalid Email/Password')
			if credentials_from_file:
				print('Switching to manual input')
				credentials_from_file = False
		else: 
			cont = True

	print('Loading...\n')

	if os.path.isfile('settings.txt') and os.name != 'nt':
			os.system('chmod -r settings.txt')
	
	profile_url = [x for x in driver.find_elements_by_tag_name('a') if x.get_attribute('title') == 'Profile'][0].get_attribute('href')
	re_search = re.search(r'(\?id=\d+)$', profile_url)
	profile = ''
	
	if re_search:
		profile = re_search.group(0)
		profile = profile.replace('?id=', '')
	else:
		profile = profile_url[profile_url.rfind('/')+1:]
		
	driver.get('https://www.facebook.com/events/birthdays/')
	
	print('\033[92mReady!\033[0m\n\n-------------- COMMANDS --------------')


if __name__ == '__main__':
	init()
	sendBirthdayWish()
	