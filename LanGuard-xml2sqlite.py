import sys
from xml.dom.minidom import parse
import sqlite3
import re

xmlContent = parse(sys.argv[1])
db = sqlite3.connect('ovalkb.db')

hostList = xmlContent.getElementsByTagName('host')
for host in hostList:
	if len(host.getElementsByTagName('alerts')) > 0:
		if len(host.getElementsByTagName('alerts')[0].getElementsByTagName('alert')) > 0:
			alerts = host.getElementsByTagName('alerts')[0].getElementsByTagName('alert')
			for alert in alerts:
				vulCategory = alert.parentNode.nodeName
				if vulCategory == 'Information_Alerts' or vulCategory == 'MalwareProtection_Alerts':
					continue
				name = alert.getElementsByTagName('name')[0].childNodes[0].data
				matchObj = re.match(r'(OVAL:\d+):.*',name)
				if matchObj: name = matchObj.group(1)
				description = alert.getElementsByTagName('descr')[0].childNodes[0].data
				name = re.sub('\"', '\'', name)
				description = re.sub('\"', '\'', description)
				# print "Looking for alert %s...\n" % name
				result = db.execute('SELECT COUNT(*) FROM vul WHERE name="%s"' % name)
				if result.fetchone()[0] == 0:
					# print ("Adding alert %s %s...\n" % (name, description)).encode('utf-8')
					db.execute('INSERT INTO vul VALUES ("%s","%s")' % (name, description))
					db.commit()
		if len(host.getElementsByTagName('alerts')[0].getElementsByTagName('hotfix')) > 0:
			hotfixes = host.getElementsByTagName('alerts')[0].getElementsByTagName('hotfix')
			for hotfix in hotfixes:
				name = hotfix.getElementsByTagName('bulletinid')[0].childNodes[0].data
				description = hotfix.getElementsByTagName('title')[0].childNodes[0].data
				matchObj = re.match(r'(.*)(\s\(KB\d+\))',description)
				if matchObj: 
					if name == 'Not Available':
						name = matchObj.group(2)[2:-1]
					else:
						name += matchObj.group(2)
					description = matchObj.group(1)
				name = re.sub('\"', '\'', name)
				description = re.sub('\"', '\'', description)
				# print "Looking for hotfix %s...\n" % name
				result = db.execute('SELECT COUNT(*) FROM fix WHERE name="%s"' % name)
				if result.fetchone()[0] == 0:
					# print "Adding alert %s %s...\n" % (name, description)
					db.execute('INSERT INTO fix VALUES ("%s","%s")' % (name, description))
					db.commit()

db.close()