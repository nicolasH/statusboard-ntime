#!/usr/local/bin/python
print "Content-Type: text/html\n"
print ""# blank line required to denote end of header

import json
import my_html

import cgitb
cgitb.enable()
import cgi

server_url = "http://niconomicon.net/statusboard-ntime/appleDev/"
#server_url = "http://192.168.1.103/~niko/statusboard-ntime/appleDev/"
path_json = 'current/current.json'


def print_form_page():
    print """
<html>
    <head>
        <title>Status Board snippet(s)</title>
        <link rel="stylesheet" media="all" href="/index.css" />
    </head>
    <body>
        <div id="wrapper">
        <div id="blog">
            <br/>
            <div class="post">
                <div class="title">Apple Developer Systems Status Widget</div>
                <div class="content">
    <p>This was made after the Apple Developer Center and related sites were taken offline for maintenance after an intrusion. It allows you to see the status of the different sub-system <a href="https://developer.apple.com/support/system-status/">published by Apple</a> in a <a href="http://panic.com/statusboard/">Panic's Status Board</a> "table" widget.</p>
    <p>The form bellow allow you to select which parts of the system you want to see in your widget. Click on "Status Board Table" to add the table with the status of the selected sub-systems to your Status Board app.</p>
    <p>The 3 links bellow the form will also open in statusboard with their respective information.</p>
    <p>The Status Board table widget minimum dimension is 4 x 4 so you might want to choose at least 4 sub-systems to monitor.</p>
    <p>The data is read from <a href="https://developer.apple.com/support/system-status/">Apple server's</a> every 5 minutes</p>
    """
    json_file = open(path_json,'rb')
    status = json.load(json_file)
    #print status
    keys = sorted(status.keys(),key=lambda k:k.lower())

    print """<form action="index.cgi">"""
    for key in keys:
        print """<input type="checkbox" class="checkbox" name="%s">%s</input><br>""" % (key[:2],key[3:])

    print """<input type="button" onclick="panic_table()" value="Status Board Table"></form>"""
    print "</form>"
    print my_html.panic_link(server_url,"current/all.html","Everything")+"<br>"
    print my_html.panic_link(server_url,"current/imgs.html","Everything as images") +" ( in the same order as on the original page)<br>"
    print my_html.panic_link(server_url,"current/down.html","Only Down")+"<br>"
    print """
                </div>
            </div>
        </div>
        <div id="pre_footer"> &mdash; ~ &mdash; </div>
        <div id="footer">
          <a href="https://github.com/nicolasH/statusboard-ntime">source</a>
          &copy; Nicolas Hoibian (<a href="http://creativecommons.org/licenses/by-nc-sa/3.0/">by-nc-sa</a>) 2013<br>
          <a href="http://www.niconomicon.net">@nico_h</a> on
          <a href="https://alpha.app.net/nico_h">app.net</a> & <a href="https://twitter.com/nico_h">twitter</a><br>

        </div>
    """
    print """
        <script type="text/javascript">
    """
    print """var server_url = "%s"; """ % server_url;
    print """
    function panic_table(){
        var selected_elements = document.getElementsByTagName("input");
        var complements = "index.cgi?";
        len = selected_elements.length;
        for(var i=0; i<len; i++){
            var e = selected_elements.item(i);
            if (e.type=='checkbox' && e.checked){
                complements += e.name+"=on&";
            }
        }
        target_url = "panicboard://?panel=table&sourceDisplayName=niconomicon&url=";
        target_url += encodeURIComponent(server_url + complements);
        document.location = target_url;
    }
    </script>"""

    print """
    <script type="text/javascript">
        var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
        document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
    </script>
    <script type="text/javascript">
        var pageTracker = _gat._getTracker("UA-3650019-1");
        pageTracker._initData();
        pageTracker._trackPageview();
    </script>"""
    print """
</body>
</html>"""



form = cgi.FieldStorage()

if len(form)>0:
    args = form.keys()
    json_file = open(path_json,'rb')
    status = json.load(json_file)
    #print status
    keys = sorted(status.keys(),key=lambda k:k.lower())

    print "<table>"
    for k in keys:
        if k[:2] in args:
            value = status[k]
            print my_html.to_simple_row(k[3:], "current/"+value)
    print "</table>"

else:
    print_form_page()
