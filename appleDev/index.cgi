#!/usr/local/bin/python
import json
import my_html

import cgitb
cgitb.enable()
import cgi

server_url = "http://niconomicon.net/statusboard-ntime/appleDev/"
#server_url = "http://192.168.1.103/~niko/statusboard-ntime/appleDev/"
path_json = 'current/current.json'


def print_form_page():
    print "Content-Type: text/html\n"
    print ""# blank line required to denote end of header
    print "<html><head><title></title></head><body>"
    json_file = open(path_json,'rb')
    status = json.load(json_file)
    #print status
    keys = sorted(status.keys(),key=lambda k:k.lower())

    print """<form action="index.cgi">"""
    for key in keys:
        print """<input type="checkbox" name="%s">%s</input><br>""" % (key[:2],key[3:])

    print """<input type="submit" value="Panic Table"></form>"""
    print "</form>"
    print my_html.panic_link(server_url,"current/all.html","Everything")+"<br>"
    print my_html.panic_link(server_url,"current/imgs.html","Everything as images") +"<br>"
    print my_html.panic_link(server_url,"current/down.html","Only Down")+"<br>"
    print "</body></html>"


args = "06=on&08=on&12=on"
form = cgi.FieldStorage()

if len(form)>0:
    print form
    args = form.keys()
    print args
    json_file = open(path_json,'rb')
    status = json.load(json_file)
    #print status
    keys = sorted(status.keys(),key=lambda k:k.lower())

    print "<table>"
    for k in keys:
        if k[:2] in args:
            value = status[k]
            print my_html.to_simple_row(k[3:], value)
    print "</table>"

else:
    print_form_page()
