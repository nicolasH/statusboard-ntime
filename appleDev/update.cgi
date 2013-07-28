#!/usr/local/bin/python
print "Content-Type: text/html\n"
print # blank line required to denote end of header

import bs4
import urllib2
import json
from traceback import print_exception
import sys
import my_html

url = "https://developer.apple.com/support/system-status/"
path_all = 'current/all.html'
path = 'current/'
path_json = 'current/current.json'
server_url = "http://niconomicon.net/statusboard-ntime/appleDev/"


def refresh_data():
    try:
        result = urllib2.urlopen(url)
        print "fetched the data"
        if result.getcode() == 200:
            parse_and_update_tables(result.read())
    except Exception:
        print_exception(sys.exc_type, sys.exc_value, sys.exc_traceback, -1, sys.stdout)
        pass


def parse_and_update_tables(page_text):
    bs = bs4.BeautifulSoup(page_text)
    status = {}
    n = 0
    for td in bs.find_all('td'):
        name = td.text
        key = name
        value = td['class'][0]
        #print key,value
        key = str(n).zfill(2)+"_"+key
        status[key] = value
        #single = key.strip().lower()
        #single = single.replace(' ','-').replace(',','').replace('&','')
        single = key[:2]+".html"
        f = open(path+single,'w')
        f.write("<table>")
        f.write(my_html.to_simple_row(key[3:], value))
        f.write("</table>")
        f.close()
        #print my_html.panic_link(server_url, single, name)
        #"""<a href="panicboard://?panel=table&sourceDisplayName=niconomicon&url=%s">%s</a>""" % (server_url + single, name)
        n +=1

    ### All the status
    keys = sorted(status.keys(),key=lambda k:k.lower())
    f = open(path+"all.html",'w')
    f.write("<table>")
    for k in keys:
        f.write(my_html.to_simple_row(k[3:], status[k]))

    f.write("</table>")
    f.close()
    ### All the status as images
    f = open(path+"imgs.html",'w')
    f.write("<table>")

    for n in range(0,(len(keys)/3)):
        index = 3 * n

        status_a = status[keys[index]]
        status_b = status[keys[index+1]]
        status_c = status[keys[index+2]]
        f.write(my_html.to_img_row(status_a,status_b,status_c))

    f.write("</table>")
    f.close()

    ### Only down services
    keys = sorted(status.keys(),key=lambda k:k.lower())
    f = open(path+"down.html",'w')
    f.write("<table>")
    for k in keys:
        if status[k] == "offline":
            f.write(my_html.to_simple_row(k[3:], status[k]))
    f.write("</table>")
    f.close()

    f = open(path_json,'w')
    json.dump(status,f)
    f.close()

print "refreshing..."
refresh_data()
print "done"
