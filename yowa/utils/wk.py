#! /usr/bin/env python
import os
os.environ['DISPLAY'] = ':1'
import sys
import gtk
import webkit
import jswebkit

def run_webkit(url):
    webview = webkit.WebView()
    webview.connect('load-finished', lambda v, f: gtk.main_quit())
    webview.load_uri(url)
    gtk.main()
    js = jswebkit.JSContext(webview.get_main_frame().get_global_context())
    return str(js.EvaluateScript('document.documentElement.outerHTML'))

if __name__ == '__main__':
    url = 'http://roll.hexun.com/'
    url_list = sys.argv[1:]

    for u in url_list:
        print len(run_webkit(u))

