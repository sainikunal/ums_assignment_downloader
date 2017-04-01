from selenium import webdriver
from pyvirtualdisplay import Display
import os, getpass, sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib2

display = Display()
display.start()

print '\n\tStudent UMS Assignment Downloader'
print '\n\tInstructions: [*] UMS ID must be of length 8'
print '\t              [*] Password would not be visible while typing'
print '\t              [*] Internet connection of 1 MB/s is recommended'
print '\t              [*] Downloaded files would be saved in current directory'
print ''

# Student UMS ID must be of 8 digit
username = raw_input('UMS ID  : ')
while len(''.join(username.split())) != 8 :
	username = raw_input('Enter Valid Student UMS ID : ')

# Password must have minimum length of 6
password = getpass.getpass()
while len(password) < 6 :
	password = getpass.getpass('Enter Valid UMS Password : ')

print ''
option = webdriver.ChromeOptions()
option.add_argument('load.strategy=unstable')
driver = webdriver.Chrome(chrome_options = option)

try:
	driver.get('https://ums.lpu.in/lpuums')
except:
	print '[*] Either UMS is not responding OR check your Internet Connnection'
	driver.close()
	sys.exit()

print '{:>2}'.format('[*] Trying to Login')

# Javascript to fill username and password
script = "document.getElementById('TextBox1').value = '%s';\
                document.getElementById('TextBox2').value= '%s';"\
                % (username, password) 

try:
    submit_button = WebDriverWait(driver,3).until(
       EC.presence_of_element_located((By.ID, 'iBtnLogin'))
                    )
except :
    print '[*] Either UMS is not responding OR check your Internet Connnection'
    driver.close()
    sys.exit()

driver.execute_script(script) 
submit_button.click()

# Validating login details
title_after_login = 'Lovely Professional University :: University Management System (UMS)'
try:
	if driver.title != title_after_login:
		print '{:>2}'.format('[*] Login with valid Details.')
		driver.close()
		sys.exit()
except:
	print 'Incorrect Details'
	driver.close()
	sys.exit()

print '[*] Login Successful'
print '[*] Getting Course Files'
print ''
driver.get('https://ums.lpu.in/lpuums/frmstudentdownloadassignment.aspx')

table_id = driver.find_element(By.ID,'ctl00_cphHeading_GridView1')
rows = table_id.find_elements(By.TAG_NAME, "tr")

splitedText = {}

index = 1
total = 1

print '{:>10} {:>10}'.format('Options', 'Courses')
for i,row in enumerate(rows):
	if i == 0: continue
	text = row.text.encode('utf-8').split('-')[0]
	Text = (text).split(' ')
	splitedText[i] = Text
	
	print '{:>7} {:>5} {:>21}'.format(i, ': ',text)
	total += 1

print ''
option = int(raw_input("[*] Your Option : "))

while option not in range(1,total):
	option = int(raw_input('[*] Valid Option : '))

text = splitedText[option]
if 'LABORATORY' in text:
	print 'No assignment available for download'
	sys.exit()




input_id = table_id.find_elements(By.TAG_NAME, "input")


for i,input_tag in enumerate(input_id):
	if i+1 == option:
		input_tag.click()
		directory = ' '.join(splitedText[i+1])
		break

alt_id = driver.find_elements_by_tag_name('alt')

# download link starts from this 'tr' id
t_id = 'ctl00_cphHeading_rgAssignment_ctl00'
tr_id = driver.find_element(By.ID, t_id)
all_rows = tr_id.find_elements(By.TAG_NAME, "tr")

def download_message(message,ext):
	print '[*] Downloading "%s.%s"' %(message,ext)

try:
	os.mkdir(directory)
	os.chdir(os.getcwd()+'/'+directory)
except:
	os.chdir(directory)

char1 = 10
xpath_id = 0
count = 5
total_downloaded = 0
listfiles = os.listdir(os.getcwd())

for row in range(len(all_rows)):
	
	try:
		
		string = 'ctl00_cphHeading_rgAssignment_ctl00_ctl0'+str(count)+'_lblFileUplaodByTeacher'
		anchor = driver.find_element_by_id(string)
		link = anchor.get_attribute('href')
		
		split_link = link.split('.')[-1]
		response = urllib2.urlopen(link)
		xpath = '//*[@id="ctl00_cphHeading_rgAssignment_ctl00__%s"]/td[7]' %xpath_id
		filename = driver.find_element_by_xpath(xpath) #%str(xpath_id)
		
		# Skip if file already exists
		if filename.text + '.' + split_link in listfiles:
			continue

		with open(filename.text +'.' + split_link,'w') as f:
			download_message(filename.text, split_link)
			f.write(response.read())
			total_downloaded += 1
			                  
	except:
			
		try:
			string = 'ctl00_cphHeading_rgAssignment_ctl00_ctl'+str(char1)+'_lblFileUplaodByTeacher'
			anchor1 = driver.find_element_by_id(string)
			
			link1 = anchor1.get_attribute('href')
			split_link = link1.split('.')[-1]
			response = urllib2.urlopen(link1)
			xpath = '//*[@id="ctl00_cphHeading_rgAssignment_ctl00__%s"]/td[7]' %xpath_id
			filename = driver.find_element_by_xpath(xpath)
			
			# Skip if file already exists
			if filename.text + '.' + split_link in listfiles:
				continue

			with open(filename.text +'.' + split_link,'w') as f:
				download_message(filename.text, split_link)
				f.write(response.read())
				total_downloaded += 1
				
		except:
			
			try:
				string = 'ctl00_cphHeading_rgAssignment_ctl00_ctl'+str(char1)+'_lblNotRequired'
				anchor1 = driver.find_element_by_id(string)
		
				link1 = anchor1.get_attribute('href')
				split_link = link1.split('.')[-1]
				response = urllib2.urlopen(link1)
				xpath = '//*[@id="ctl00_cphHeading_rgAssignment_ctl00__%s"]/td[7]' %xpath_id
				filename = driver.find_element_by_xpath(xpath)
				
				# Skip if file already exists
				if filename.text + '.' + split_link in listfiles:
					continue
				
				with open(filename.text +'.' + split_link,'w') as f:
					download_message(filename.text, split_link)
					f.write(response.read())
					total_downloaded += 1
										
			except:
				pass
	
	xpath_id += 1

	char1 += 2
	
	count += 2

if total_downloaded == 0:
	print 'No latest file available to download'
else:
	print '\nTotal Files Downloaded : ' + str(total_downloaded)

# print 'It might be possible that some files could be downloaded'
driver.close()

