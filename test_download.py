import project0

def test_download(url):
    incident_data = project0.fetchincidents(url)
    return incident_data


if __name__ == '__main__':
    url = url = 'https://www.normanok.gov/sites/default/files/documents/2023-02/2023-02-02_daily_incident_summary.pdf'
    incident_data = test_download(url)
    if incident_data is not None:
        print('Download successfully!')
