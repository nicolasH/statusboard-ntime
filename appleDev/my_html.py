def to_simple_row(name, status):
    return """<tr><td class="noresize" width=45px"><img src="%s.png"></td><td>%s</td></tr>""" % (status,name)

def to_img_row(status_a, status_b, status_c):
    return """
    <tr>
        <td class="noresize" width=45px"><img src="%s.png"></td>
        <td class="noresize" width=45px"><img src="%s.png"></td>
        <td class="noresize" width=45px"><img src="%s.png"></td>
    </tr>""" % (status_a, status_b, status_c)


def panic_link(server_url,file_name,name):
    return """<a href="panicboard://?panel=table&sourceDisplayName=niconomicon&url=%s">%s</a>""" % (server_url + file_name, name)
