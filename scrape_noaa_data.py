import requests
from bs4 import BeautifulSoup
import csv
from numpy import genfromtxt

# Pass this in

def get_ia_data():
    gaugeId = '8465705'

    session = requests.Session()

    # This puts the gauge ID into the server-side session
    session.get( 'http://tidesandcurrents.noaa.gov/inundation/AnalysisParams?id='+gaugeId)

    payload = {
        'userReferrence': 8.239,
        'beginDate': 20090101,
        'endDate': 20131231
    }

    # Get the actual data. It'll use the querystring for height and dates, and get the gauge ID from the session
    response = session.get('http://tidesandcurrents.noaa.gov/inundation/Analysis?userReferrence=8.239&beginDate=20090101&endDate=20131231&submit=+Submit++', data=payload)

    # print '--------------------'
    # print ''
    # print response.content
    # print '--------------------'
    # print ''

    # check if it returned usable data
    if 'High Tides Analyzed' in response.content:
        print "FOUND STRING"
    else:
        print "NOT FOUND"

    #print response.content
    #print response.request.headers

    soup = BeautifulSoup(response.content)
    #print soup
    table = soup.find("table")

    #print table

    records = []
    # for tr in table.find_all('tr'):
    #     tds = tr.find_all('td')
    #     records.append([elem.text.encode('utf-8') for elem in tds])
    #
    # with open('all_records.csv','wb') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(records)

    rows = soup.find_all("tr", {'class': ["tableRowEven", "tableRowOdd"]})
    for row in rows:
        records.append([elem.text.encode('utf-8') for elem in row.find_all('td')])

        with open('all_records.csv','wb') as f:
            writer = csv.writer(f)
            writer.writerows(records)

        # with open('all_records.csv','rb') as f:
        #  reader = csv.reader(f)
        #  print(reader.count('2009'))
        #  # for row in reader:
        #  #     #print row[0]
        #  #     year_splits = row[0].split('-')


def count_flood_events():

    # create a csv file here with year and # flood events as the two cols
    # pass years in here as a range, like: for i> 1990 and i<2014...
        with open('all_records.csv','r') as content_file:
            content = content_file.read()
            print(content.count('2010')) # this gets 3 instances for each year b/c the year is listed in 3 cols.

    # write year and # flood events to the csv file


    # print "Cookies after request: " + repr( session.cookies.get_dict() )

    #