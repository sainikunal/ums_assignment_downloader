from mechanize import Browser
import cssselect
import lxml.html, webbrowser
import os, sys, getpass, urllib

print '\n\tStudent UMS Assignment Downloader'
print '\n\tInstructions: [*] UMS ID must be of length 8'
print '\t              [*] Password would not be visible while typing'
print '\t              [*] Internet connection of 1 MB/s is recommended'
print '\t              [*] Downloaded files would be saved in current directory'
print ''

# Student UMS ID must be of 8 digit
username = raw_input('[*] UMS ID   : ')
while len(''.join(username.split())) != 8 :
	username = raw_input('Enter Valid Student UMS ID : ')

# Password must have minimum length of 6
password = getpass.getpass('[*] Password : ')
while len(password) < 6 :
	password = getpass.getpass('Enter Valid UMS Password : ')

print ''
br = Browser()
br.set_handle_robots(False)

try:
	br.open('https://ums.lpu.in/lpuums')
except:
	print '[*] Either UMS is not responding OR check your Internet Connnection'
	br.close()
	sys.exit()

# https://ums.lpu.in/lpuums/errorpages/GeneralError.aspx?aspxerrorpath=/lpuums/loginnew.aspx
# when we are able to open the ums but the error page is displayed
# then we can't select form
try:
	br.select_form(name='form1')
	br['TextBox1'] = username
	br['TextBox2'] = password
except:
	print '[*] UMS encountered error page'
	br.close()
	sys.exit()

print '[*] Validating Login Details'
resp = br.submit()

title_after_login = 'Lovely Professional University :: University Management System (UMS)'

if br.title() != title_after_login:
	print '{:>2}'.format('[*] Login with valid Details.')
	br.close()
	sys.exit()


print '[*] Login Successful'
print '[*] Getting Course Files'
print ''
br.open('https://ums.lpu.in/lpuums/frmstudentdownloadassignment.aspx')

#resp = br.submit()
br.select_form(name='aspnetForm')

cour = lxml.html.fromstring(br.response().read())
courses = ['empty']
for tr in cour.cssselect('#ctl00_cphHeading_GridView1 tr'):
	td = tr.cssselect('td')
	if len(td) < 9: continue
	name = td[1].text_content() + ' '
	name += td[2].text_content()
	courses.append(name)

print '{:>10} {:>10}'.format('Options', 'Courses')
for i, course in enumerate(courses):
	if not i: 
		print '{:>7} {:>5} {:>21}'.format(i, ': ','Download content of every course')
		continue
	print '{:>7} {:>5} {:>21}'.format(i, ': ', course)

print ''
option = int(raw_input("[*] Your Option : "))

while option not in range(0,len(courses)):
	option = int(raw_input('[*] Valid Option : '))

parent_path = os.getcwd()

def download_file(opt):

	def download_message(message):
		print '{} {:30}'.format('[*] Downloading', message),

	listfiles = os.listdir(os.getcwd())
	total_downloaded = 0

	for i in range(opt,len(courses)):
		if i < 9:
			detail_button = 'ctl00$cphHeading$GridView1$ctl0'+ str(i+1) +'$btnViewDetails'
		else:
			detail_button = 'ctl00$cphHeading$GridView1$ctl'+ str(i+1) +'$btnViewDetails'
		
		if i == opt:
			br.submit(name=detail_button, label='View Details')
			break

	directory = courses[opt]
	if 'LABORATORY' in directory.split():
		#print 'No assignment available for download in',directory
		br.open('https://ums.lpu.in/lpuums/frmstudentdownloadassignment.aspx')
		br.select_form(name='aspnetForm')
		return


	#resp = br.submit(name='ctl00$cphHeading$GridView1$ctl02$btnViewDetails',label='View Details')
	html = br.response().read()
	root = lxml.html.fromstring(html)
	links = root.xpath('//div[@id="ctl00_cphHeading_Panel1"]//a//@href')

	names = []
	for tr in root.cssselect('#ctl00_cphHeading_rgAssignment_ctl00 tbody tr'):
		td = tr.cssselect('td')
		if len(td) < 12 : continue
		names.append(td[6].text_content())

	try:
		os.mkdir(directory)
		os.chdir(os.getcwd()+'/'+directory)
	except:
		os.chdir(directory)
	files = os.listdir(os.getcwd())
	total_size = 0

	print 'Downloading Files under', directory

	for index, link in enumerate(links):
		if link.split('/')[-2] == 'Student':
			continue

		ext = link.split('.')[-1]
		filename = names[index].split(':')[-1] + '.' + ext
		if filename not in files:
			
			print '{} {:30}'.format('[*] Downloading', filename),
			with open(filename, 'wb') as f:
				data = urllib.urlopen(link)
				meta = data.info()
				filesize = int(meta.getheaders("Content-Length")[0])
				total_size += filesize
				print '({} {})'.format((filesize/1024), 'KB')
				f.write(data.read())
				total_downloaded += 1

		else:
			pass


	if total_downloaded == 0:
		print 'No latest file available to download in',directory
	else:
		print '\nTotal Files Downloaded : %d (%d KB) ' %(total_downloaded, total_size/1024)
		print ''

	br.open('https://ums.lpu.in/lpuums/frmstudentdownloadassignment.aspx')

	br.select_form(name='aspnetForm')

	os.chdir(parent_path)


if option == 0:
	for x in range(1,len(courses)):
		download_file(x)
else:
	download_file(option)
br.close()
