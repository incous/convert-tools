#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
from xml.dom.minidom import parse

def dateRewrite(text):
	matchObj = re.match(r'(\d{4})-(\d\d)-(\d\d)',text)
	if matchObj:
		return matchObj.group(3) + '/' + matchObj.group(2) + '/' + matchObj.group(1)
	else:
		return text

f = open(sys.argv[2], 'w')
xmlContent = parse(sys.argv[1])
hostList = xmlContent.getElementsByTagName('host')
f.write('''<html>
<head>
<title>Host assessment report</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<style>
table, td, th {
	border:1px solid black;
	border-collapse:collapse;
	padding: 3px;
}
</style>
</head>
<body>
''')

for host in hostList:
	nTotal = 0
	nHigh = 0
	nModerate = 0
	nLow = 0
	nWeb = 0
	nSvc = 0
	nCfg = 0
	nSof = 0
	nFix = 0
	hostname = 'N/A' if len(host.getElementsByTagName('hostname')[0].childNodes) == 0 else host.getElementsByTagName('hostname')[0].childNodes[0].data
	f.write(('''<hr /><h2>Máy %s</h2>
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
	if len(host.getElementsByTagName('alerts')) > 0:
		if len(host.getElementsByTagName('alerts')[0].getElementsByTagName('alert')) > 0:
			f.write('''<h3>Danh sách lỗi được phân loại theo mức độ nguy hiểm</h3>
		<table>
		<tr>
			<th><b>Danh sách lỗi</b></th><th><b>Phân loại lỗi</b></th><th><b>Mức độ nguy hiểm</b></th>
		</tr>
''')
			vulList = host.getElementsByTagName('alerts')[0].getElementsByTagName('alert')
			for vul in vulList:
				nTotal += 1
				vulName = vul.getElementsByTagName('name')[0].childNodes[0].data
				matchObj = re.match(r'(OVAL:\d+):.*',vulName)
				if matchObj: vulName = matchObj.group(1)
				# vulDescription = '' if len(vul.getElementsByTagName('descr')[0].childNodes) ==0 else vul.getElementsByTagName('descr')[0].childNodes[0].data
				vulCategory = vul.parentNode.nodeName
				if vulCategory == 'Software_Alerts':
					vulCategoryLabel = 'Phần mềm'
					nSof += 1
				elif vulCategory == 'Registry_Alerts':
					vulCategoryLabel = 'Cấu hình hệ thống'
					nCfg += 1
				elif vulCategory == 'Services_Alerts' or vulCategory == 'Miscellaneous_Alerts':
					vulCategoryLabel = 'Dịch vụ ứng dụng'
					nSvc += 1
				elif vulCategory == 'Web_Alerts':
					vulCategoryLabel = 'Trình duyệt Web'
					nWeb += 1
				elif vulCategory == 'Information_Alerts' or vulCategory == 'MalwareProtection_Alerts':
					nTotal -= 1
					continue
				else:
					vulCategoryLabel = vulCategory
				vulSeverity = vul.parentNode.parentNode.getAttribute('level')
				if vulSeverity == ' 0':
					vulSeverityLabel = 'Nghiêm trọng'
					nHigh += 1
				elif vulSeverity == ' 1':
					vulSeverityLabel = 'Trung bình'
					nModerate += 1
				elif vulSeverity == ' 2':
					vulSeverityLabel = 'Thấp'
					nLow += 1
				else:
					vulSeverityLabel = 'N/A'
				f.write(('''<tr>
			<td>%s</td><td align="center">%s</td><td align="center">%s</td>
		</tr>
''' % (vulName, vulCategoryLabel.decode('utf-8'), vulSeverityLabel.decode('utf-8'))).encode('utf-8'))
			f.write('''</table>
''')
		if len(host.getElementsByTagName('alerts')[0].getElementsByTagName('hotfix')) > 0:
			f.write('''<h3>Thông tin bản vá còn thiếu</h3>
		<table>
		<tr>
			<th><b>Danh sách bản vá</b></th><th><b>Ngày phát hành</b></th><th><b>Mức độ nguy hiểm</b></th>
		</tr>
''')
			hotfixes = host.getElementsByTagName('alerts')[0].getElementsByTagName('hotfix')
			for hotfix in hotfixes:
				nFix += 1
				nTotal += 1
				hotfixBID = hotfix.getElementsByTagName('bulletinid')[0].childNodes[0].data
				hotfixTitle = hotfix.getElementsByTagName('title')[0].childNodes[0].data
				matchObj = re.match(r'.*\s(\(KB\d+\))',hotfixTitle)
				if hotfixBID == 'Not Available':
					hotfixBID = hotfixTitle
				elif matchObj:
					hotfixBID += ' ' + matchObj.group(1)
				hotfixDate = hotfix.getElementsByTagName('date')[0].childNodes[0].data
				hotfixSeverity = 'N/A' if len(hotfix.getElementsByTagName('severity')[0].childNodes) == 0 else hotfix.getElementsByTagName('severity')[0].childNodes[0].data
				if hotfixSeverity == 'Critical' or hotfixSeverity == 'Important':
					hotfixSeverityLabel = 'Nghiêm trọng'
					nHigh += 1
				elif hotfixSeverity == 'Moderate':
					hotfixSeverityLabel = 'Trung bình'
					nModerate += 1
				elif hotfixSeverity == 'Low' or hotfixSeverity == 'N/A':
					hotfixSeverityLabel = 'Thấp'
					nLow += 1
				else:
					hotfixSeverityLabel = 'N/A'
				f.write(('''<tr>
			<td>%s</td><td align="center">%s</td><td align="center">%s</td>
		</tr>
''' % (hotfixBID, dateRewrite(hotfixDate), hotfixSeverityLabel.decode('utf-8'))).encode('utf-8'))
			f.write('</table>')
	f.write(('''<h3>Thống kê phân loại theo mức độ nguy hiểm</h3>
	<table>
		<tr><th>Tên máy</th><th>Tổng số lỗi</th><th>Nghiêm trọng</th><th>Trung bình</th><th>Thấp</th></tr>
		<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>
	</table>
'''.decode('utf-8') % (hostname, nTotal, nHigh, nModerate, nLow)).encode('utf-8'))
	f.write(('''<h3>Thống kê tổng hợp phân loại lỗ hổng</h3>
	<table>
		<tr><th>Tên máy</th><th>Trình duyệt Web</th><th>Dịch vụ ứng dụng</th><th>Cấu hình hệ thống</th><th>Phần mềm</th><th>Thiếu bản vá</th></tr>
		<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>
	</table>
'''.decode('utf-8') % (hostname, nWeb, nCfg, nSvc, nSof, nFix)).encode('utf-8'))
f.write('</body></html>')
f.close()
