#!/usr/local/bin/python
print "Content-Type: text/html\n"
print # blank line required to denote end of header

import bs4
import urllib2
from traceback import print_exception
import sys
url = "https://developer.apple.com/support/system-status/"
path_all = 'current/all.html'
path = 'current/'

server_url = "http://niconomicon.net/statusboard-ntime/appleDev/"

def refresh_data():
    try:
        result = urllib2.urlopen(url)
        print "fetched the data"
        if result.getcode() == 200:
            parse_and_update_table(result.read())
    except Exception:
        print_exception(sys.exc_type, sys.exc_value, sys.exc_traceback, limit, sys.stdout)
        pass

def to_row(name, status):
    return """<tr><td class="noresize" width=45px"><img src="%s.png"></td><td>%s</td></tr>""" % (status,name)

def parse_and_update_table(page_text):
    bs = bs4.BeautifulSoup(page_text)
    status = {}
    for td in bs.find_all('td'):
        key = td.text
        value = td['class'][0]
        #print key,value
        status[key] = value
        single = key.strip().lower()
        single = single.replace(' ','-').replace(',','').replace('&','')
        single = path + single+".html"
        f = open(single,'w')
        f.write("<table>")
        f.write(to_row(key, value))
        f.write("</table>")
        f.close()
        print """<a href="panicboard://?panel=table&sourceDisplayName=niconomicon&url=%s">%s</a>""" % (server_url + single, key)

    keys = sorted(status.keys(),key=lambda k:k.lower())
    f = open(path_all,'w')
    f.write("<table>")
    for k in keys:
        f.write(to_row(k, status[k]))
    # f.write(json.dumps(status))
    f.write("</table>")
    f.close()

print "refreshing"
refresh_data()
print "done"
