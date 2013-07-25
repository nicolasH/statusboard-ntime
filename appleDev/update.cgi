import bs4
import requests
from traceback import print_exc
import json
from datetime import datetime
import os.path, time
from datetime import timedelta
url = "https://developer.apple.com/support/system-status/"
path_all = 'current/all.html'
path = 'current/'

server_url = "http://niconomicon.net/statusboard-ntime/appleDev/"
max_delta = timedelta(minutes=5)

# def should_update():
#     now = datetime.now()
#     then = os.path.getmtime(path)
#     then = datetime.fromtimestamp(then)
#     should_update = now - then > max_delta
#     print "last modified: %s should update: %s " % (then, str(should_update))
#     return should_update

def refresh_data():
    try:
        result = requests.get(url)
        if result.status_code == 200:
            parse_and_update_table(result.content)
    except Exception:
        print_exc()
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


if __name__ == '__main__':
    #with_date()
    refresh_data()
