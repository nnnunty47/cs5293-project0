import project0

def test_status(url):
    incident_data = project0.fetchincidents(url)
    incidents = project0.extractincidents(incident_data)
    db = project0.createdb()
    project0.populatedb(db, incidents)
    project0.status(db)


if __name__ == '__main__':
    url = url = 'https://www.normanok.gov/sites/default/files/documents/2023-02/2023-02-02_daily_incident_summary.pdf'
    incidents = test_status(url)
