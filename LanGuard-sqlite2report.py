import sys
import sqlite3

db = sqlite3.connect('ovalkb.db')
f = open(sys.argv[1],'w')

f.write('''
<html>
	<head>
		<title>Report reference</title>
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
	<table>
		<tr>
			<th>Name</th><th>Description</th>
		</tr>
''')

result = db.execute('SELECT * FROM vul')
while (1):
	row = result.fetchone()
	try:
		name = row[0]
		description = row[1]
		f.write(('''		<tr><td>%s</td><td>%s</td></tr>
''' % (name, description)).encode('utf-8'))
	except:
		break

f.write('''	</table><hr />
	<table>
		<tr>
			<th>Name</th><th>Description</th>
		</tr>
''')

result = db.execute('SELECT * FROM fix')
while (1):
	row = result.fetchone()
	try:
		name = row[0]
		description = row[1]
		f.write(('''		<tr><td>%s</td><td>%s</td></tr>
''' % (name, description)).encode('utf-8'))
	except:
		break

f.write('''
	</table>
</body>
</html>
''')

f.close()
db.close()