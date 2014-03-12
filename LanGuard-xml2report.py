#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
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
	f.write(('''<h1>Host %s</h1>
''' % (hostname)).encode('utf-8'))
	
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
	if len(host.getElementsByTagName('alerts')) == 0: continue
	f.write('''<h2>List of vulnerabilities</h2>
<table border="1">
<tr>
	<td>Title</td><td>Description</td><td>Category</td><td>Severity</td>
</tr>
''')
	vulList = host.getElementsByTagName('alerts')[0].getElementsByTagName('alert')
	for vul in vulList:
		vulName = vul.getElementsByTagName('name')[0].childNodes[0].data
		vulDescription = '' if len(vul.getElementsByTagName('descr')[0].childNodes) ==0 else vul.getElementsByTagName('descr')[0].childNodes[0].data
		vulCategory = vul.parentNode.nodeName
		if vulCategory == 'Information_Alerts':
			break
		else:
			vulSeverity = vul.parentNode.parentNode.getAttribute('level')
		f.write(('''<tr>
	<td>%s</td><td>%s</td><td>%s</td><td>%s</td>
</tr>
''' % (vulName, vulDescription, vulCategory, vulSeverity)).encode('utf-8'))
	f.write('''</table>
''')
	if len(host.getElementsByTagName('hotfixes')[0].getElementsByTagName('hotfix')) == 0: continue
	f.write('''<h2>List of available hotfixes</h2>
<table border="1">
<tr>
	<td>Bulletin ID</td><td>Name</td><td>Release date</td><td>Severity</td>
</tr>
''')
	hotfixes = host.getElementsByTagName('hotfixes')[0].getElementsByTagName('hotfix')
	for hotfix in hotfixes:
		hotfixBID = hotfix.getElementsByTagName('bulletinid')[0].childNodes[0].data
		hotfixTitle = hotfix.getElementsByTagName('title')[0].childNodes[0].data
		hotfixDate = hotfix.getElementsByTagName('date')[0].childNodes[0].data
		hotfixSeverity = 'N/A' if len(hotfix.getElementsByTagName('severity')[0].childNodes) == 0 else hotfix.getElementsByTagName('severity')[0].childNodes[0].data
		f.write(('''<tr>
	<td>%s</td><td>%s</td><td>%s</td><td>%s</td>
</tr>
''' % (hotfixBID, hotfixTitle, hotfixDate, hotfixSeverity)).encode('utf-8'))
	f.write('</table><hr />')
f.write('</body></html>')
f.close()
