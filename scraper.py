#!python3.4
from lxml import html
import urllib.request
import sys

def scrape(url):
    src = urllib.request.urlopen(url);
    src_html = src.read();
    tree = html.fromstring(src_html)
    e = tree.xpath("//div[strong='Dayvie']")
    result = []
    for post in e:
        m = post.getparent().getparent().getparent().getparent().getparent().getparent().getparent()
        s = m[1][0].text
        for para in m[1][0]:
            if para.tail:
                s += "\n" + para.tail
        result.append(s)
    return result

if __name__ == '__main__':
    print(scrape(sys.argv[1]))