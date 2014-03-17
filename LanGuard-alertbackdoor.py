import sys
from xml.dom.minidom import parse

xmlContent = parse(sys.argv[1])
hostList = xmlContent.getElementsByTagName('host')
for host in hostList:
	nTotal = 0
	hostname = 'N/A' if len(host.getElementsByTagName('hostname')[0].childNodes) == 0 else host.getElementsByTagName('hostname')[0].childNodes[0].data
	ip = host.getElementsByTagName('ip')[0].childNodes[0].data
	if len(host.getElementsByTagName('alerts')) > 0:
		if len(host.getElementsByTagName('alerts')[0].getElementsByTagName('backdoors')) > 0:
			for backdoor in host.getElementsByTagName('alerts')[0].getElementsByTagName('backdoors')[0].childNodes:
				print hostname + ' - ' + ip + ' - ' + backdoor.childNodes[0].data