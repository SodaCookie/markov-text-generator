#!python3.4
from lxml import html
import urllib.request
import urllib
import sys

__all__ = ["scrape_post", "scrape_pages"]

# Url for B-Net
url = "http://us.battle.net/sc2/en/forum/blizztracker/"
query = "?page=%d"

def scrape_post(url):
    try:
        src = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        return ""
    src_html = src.read()
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
    return "\n".join(result)

def scrape_pages(user=None, number=1):
    """Searches over given number of pages on Bluepost Tracker"""
    global url
    results = []
    for i in range(1, number + 1):
        search = url + query % i
        src = urllib.request.urlopen(search)
        src_html = src.read()

        tree = html.fromstring(src_html)
        nodes = tree.xpath("//span/span[@class='author-name blizzard-post']")

        for node in nodes:
            scrape_url = "http://us.battle.net"
            if user:
                if node.text == user:
                    m = node.getparent().getparent().getparent()
                    scrape_url += m[1][0][0].get("href")
                else:
                    continue
            else:
                m = node.getparent().getparent().getparent()
                scrape_url += m[1][0][0].get("href")
            print("Querying: " + scrape_url, end=" - ")
            results.append(scrape_post(scrape_url))
            print("Complete")
    return "\n".join(results)


if __name__ == '__main__':
    import sys
    import codecs
    with codecs.open(sys.argv[1], "w", encoding='ascii', errors='ignore') \
            as file:
        file.write(scrape_pages("Dayvie", 5))