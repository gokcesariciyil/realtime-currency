import os, sys
import requests
import datetime
import pytz
from bs4 import BeautifulSoup

import monitor
monitor.start(interval=0.01)
monitor.track(os.path.dirname(__file__))

sys.path.insert(0, os.path.dirname(__file__))

r = requests.get('https://www.yapikredi.com.tr/yatirimci-kosesi/doviz-bilgileri')
soup = BeautifulSoup(r.content, 'html.parser')
currencyArea = soup.find("tbody", id="currencyResultContent")

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])

    output = ""
    output += "<html><body>" \
                "<head> " \
                    "<meta charset=\"utf-8\">" \
                    "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">" \
                    "<title>Daily Currency Rates</title>" \
                    "<meta name=\"description\" content=\"Current exchange information for Turkish lira\">" \
                "</head>" \
                "<body>" \
                "<h1>Daily Currency Rates</h1>"

    output += "<table>"
    for currencyLine in currencyArea.find_all('tr'):
        output += "<tr>"
        output += "<td>" + currencyLine.find_all('td')[1].contents[0] + "</td>"
        output += "<td>" + currencyLine.find_all('td')[2].contents[0] + "</td>"
        output += "<td>" + currencyLine.find_all('td')[3].contents[0] + "</td>"
        output += "<td>" + currencyLine.find_all('td')[4].contents[0] + "</td>"
        output += "</tr>"
    output += "</table>" \
	      "<h3>" + datetime.datetime.now(pytz.timezone('Turkey')).strftime("%H:%M:%S") + "</h3>" \
              "<h2>BAU | Gökçe Sarıçiyil</h2>" \
              "</body></html>"

    return [output.encode()]
