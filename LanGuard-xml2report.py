#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
from xml.dom.minidom import parse

f = open(sys.argv[2], 'w')
xmlContent = parse(sys.argv[1])
hostList = xmlContent.getElementsByTagName('host')
f.write('''<html>
<head>
<title>Host assessment report</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>
<body>
''')

for host in hostList:
	hostname = 'N/A' if len(host.getElementsByTagName('hostname')[0].childNodes) == 0 else host.getElementsByTagName('hostname')[0].childNodes[0].data
	f.write(('''<h1>Máy %s</h1>
'''.decode('utf-8') % (hostname)).encode('utf-8'))
	
# 	if len(host.getElementsByTagName('apps_installed')) == 0: continue
# 	f.write('''<h2>List of installed applications</h2>
# <table border="1">
# <tr>
# 	<td>Name</td><td>Version</td><td>Publisher</td><td>Up-to-date</td>
# </tr>
# ''')
# 	installedApps = host.getElementsByTagName('apps_installed')[0]
# 	for app in installedApps.childNodes:
# 		appName = app.getAttribute('name')
# 		appVersion = app.getAttribute('version')
# 		appVendor = app.getAttribute('publisher')
# 		appUp2date = app.getAttribute('is_up_to_date')
# 		f.write(('''<tr>
# 	<td>%s</td><td>%s</td><td>%s</td><td>%s</td>
# </tr>
# ''' % (appName, appVersion, appVendor, appUp2date)).encode('utf-8'))
# 	f.write('''</table>
# ''')
	if len(host.getElementsByTagName('alerts')) > 0 and len(host.getElementsByTagName('alerts')[0].getElementsByTagName('alert')) > 0:
		f.write('''<h2>Danh sách lỗi được phân loại theo mức độ nguy hiểm</h2>
	<table border="1">
	<tr>
		<td>Danh sách lỗi</td><td>Phân loại lỗi</td><td>Mức độ nguy hiểm</td>
	</tr>
''')
		vulList = host.getElementsByTagName('alerts')[0].getElementsByTagName('alert')
		for vul in vulList:
			vulName = vul.getElementsByTagName('name')[0].childNodes[0].data
			matchObj = re.match(r'(OVAL:\d+):.*',vulName)
			if matchObj: vulName = matchObj.group(1)
			# vulDescription = '' if len(vul.getElementsByTagName('descr')[0].childNodes) ==0 else vul.getElementsByTagName('descr')[0].childNodes[0].data
			vulCategory = vul.parentNode.nodeName
			if vulCategory == 'Software_Alerts':
				vulCategoryLabel = 'Phần mềm'
			elif vulCategory == 'Registry_Alerts':
				vulCategoryLabel = 'Cấu hình hệ thống'
			elif vulCategory == 'Services_Alerts' or vulCategory == 'Miscellaneous_Alerts':
				vulCategoryLabel = 'Dịch vụ ứng dụng khác'
			elif vulCategory == 'Web_Alerts':
				vulCategoryLabel = 'Trình duyệt Web'
			elif vulCategory == 'MalwareProtection_Alerts':
				vulCategoryLabel = 'Chưa cập nhật Anti-Virus'
			elif vulCategory == 'Information_Alerts':
				continue
			else:
				vulCategoryLabel = vulCategory
			vulSeverity = vul.parentNode.parentNode.getAttribute('level')
			if vulSeverity == ' 0':
				vulSeverityLabel = 'Nghiêm trọng'
			elif vulSeverity == ' 1':
				vulSeverityLabel = 'Trung bình'
			elif vulSeverity == ' 2':
				vulSeverityLabel = 'Thấp'
			else:
				vulSeverityLabel = 'N/A'
			f.write(('''<tr>
		<td>%s</td><td>%s</td><td>%s</td>
	</tr>
''' % (vulName, vulCategoryLabel.decode('utf-8'), vulSeverityLabel.decode('utf-8'))).encode('utf-8'))
		f.write('''</table>
''')
	if len(host.getElementsByTagName('hotfixes')) == 0: continue
	if len(host.getElementsByTagName('hotfixes')[0].getElementsByTagName('hotfix')) > 0:
		f.write('''<h2>Thông tin bản vá còn thiếu</h2>
	<table border="1">
	<tr>
		<td>Danh sách bản vá</td><td>Ngày phát hành</td><td>Mức độ nguy hiểm</td>
	</tr>
''')
		hotfixes = host.getElementsByTagName('hotfixes')[0].getElementsByTagName('hotfix')
		for hotfix in hotfixes:
			hotfixBID = hotfix.getElementsByTagName('bulletinid')[0].childNodes[0].data
			hotfixTitle = hotfix.getElementsByTagName('title')[0].childNodes[0].data
			if hotfixBID == 'Not Available':
				hotfixBID = hotfixTitle
			hotfixDate = hotfix.getElementsByTagName('date')[0].childNodes[0].data
			hotfixSeverity = 'N/A' if len(hotfix.getElementsByTagName('severity')[0].childNodes) == 0 else hotfix.getElementsByTagName('severity')[0].childNodes[0].data
			if hotfixSeverity == 'Critical' or hotfixSeverity == 'Important':
				hotfixSeverityLabel = 'Nghiêm trọng'
			elif hotfixSeverity == 'Moderate':
				hotfixSeverityLabel = 'Trung bình'
			elif hotfixSeverity == 'Low' or hotfixSeverity == 'N/A':
				hotfixSeverityLabel = 'Thấp'
			else:
				hotfixSeverityLabel = 'N/A'
			f.write(('''<tr>
		<td>%s</td><td>%s</td><td>%s</td>
	</tr>
''' % (hotfixBID, hotfixDate, hotfixSeverityLabel.decode('utf-8'))).encode('utf-8'))
		f.write('</table><hr />')
f.write('</body></html>')
f.close()
