import project0

def test_extract_incidents(url):
    incident_data = project0.fetchincidents(url)
    incidents = project0.extractincidents(incident_data)
    return incidents


if __name__ == '__main__':
    url = url = 'https://www.normanok.gov/sites/default/files/documents/2023-02/2023-02-02_daily_incident_summary.pdf'
    incidents = test_extract_incidents(url)
    if incidents is not None:
        print('Extract incidents successfully, some data is as below:')
        if len(incidents) > 10:
            print(incidents[:10])
        else:
            print(incidents)
