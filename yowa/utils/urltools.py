from urlparse import urlparse

host_prefix = ['com', 'cn', 'com.cn', 'net', 'org', 'net.cn', 'gov.cn', 'org.cn', 'info', 'biz', 'cc', 'ac']

def get_domain(url):
    if not url.startswith('http'):
        url = 'http://%s' % url

    host = urlparse(url).hostname
    return [i for i in host.split('.') if i not in host_prefix][-1].replace('-', '_')

if __name__ == '__main__':
    import sys
    url = sys.argv[1]
    #url = 'http://www.shcaoan.com/wy/satellite/'
    print get_domain(url)
