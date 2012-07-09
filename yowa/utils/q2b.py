#coding: utf-8

#把全角字符串转半角
def strQ2B(ustring):
    try:
        ustring = ustring.decode("gb18030")
    except:
        pass
    rstring = ""

    for uchar in ustring:
        inside_code = ord(uchar)
        
        if inside_code == 0x3000:
            inside_code = 0x0020
        else:
            inside_code -= 0xfee0
        if inside_code < 0x0020 or inside_code > 0x7e:
            rstring += uchar
        else:
            rstring += (unichr(inside_code))

    return rstring
