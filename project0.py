import urllib.request
import pypdf
import io
import sqlite3

def fetchincidents(url):
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    data = urllib.request.urlopen(urllib.request.Request(url, headers = headers)).read()
    return data

#judge a string has lower case
def hasLower(line):
    for c in line:
        if c >= 'a' and c <= 'z':
            return True
    return False

def get_incident(incident_text):
    time_idx = incident_text.find(':')
    #No time find, it is considered as invalid row
    if time_idx == -1:
        return None
    incident_time = incident_text[:time_idx + 3]
    time_idx = time_idx + 3
    while time_idx < len(incident_text) and incident_text[time_idx] == ' ':
        time_idx += 1
    data = incident_text[time_idx:].split(' ')
    #if it is not a good incident number
    if len(data[0]) != 13:
        return None
    incident_number = data[0]
    n = len(data)
    i = 1
    while i < n and not hasLower(data[i]):
        i += 1
    #location is None or incident_ori is None
    if i == 1 or i >= n - 1:
        return None

    incident_location = ''
    for j in range(1, i):
        incident_location = incident_location + data[j] + ' '

    nature = ''
    for j in range(i, n - 1):
        nature = nature + ' ' + data[j]
    incident_ori = data[-1]
    
    return (incident_time, incident_number, incident_location, nature, incident_ori)

def extractincidents(incident_data):
    #change io
    incident_data_t = io.BytesIO(incident_data)
    reader = pypdf.PdfReader(incident_data_t)
    data = []
    for page in reader.pages:
        lines = page.extract_text().split('\n')
       
        for line in lines:
            incident = get_incident(line)
            if incident is not None:
                data.append(incident)   
    return data

def createdb():
    con = sqlite3.connect("normanpd.db")
    db = con.cursor()
    #drop old table
    db.execute('DROP TABLE IF EXISTS incidents;')
    #create new table
    db.execute('CREATE TABLE incidents(incident_time TEXT, incident_number TEXT, incident_location TEXT, nature TEXT, incident_ori TEXT);')
    return db

def populatedb(db, incidents):
    for incident in incidents:
        db.execute(f"INSERT INTO incidents VALUES('{incident[0]}','{incident[1]}','{incident[2]}','{incident[3]}','{incident[4]}')")

def status(db):
    for row in db.execute("SELECT COUNT(*) as e, nature FROM incidents GROUP BY nature ORDER BY e DESC, nature ASC;"):
        print(row[1], row[0], sep = '|')

    
    
