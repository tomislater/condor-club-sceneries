import sys
import gevent
import requests

from lxml import html

from gevent import monkey

monkey.patch_all()


def find_scenery(url, name):
    response = requests.get(url)
    print response.content
    print
    print
    tree = html.fromstring(response.content)

    names_of_sceneries = [
        s_name.lower() for s_name in tree.xpath('//tr/th[1]/font/b/text()')
    ]
    print url
    print names_of_sceneries
    print name.lower()

    for s_name in names_of_sceneries:
        if name.lower() in s_name:
            print "You can find a scenery '{0}' here: {1}".format(name, url)


def gather_facts(name):
    # go to the start page and find how many pages exist
    url_base = "http://www.condor-club.eu/sceneries/0/?o=0&p={0}"

    response = requests.get(url_base.format(0))
    print response.content
    tree = html.fromstring(response.content)

    # get the number of the last page
    nr_of_the_last_page = int(
        tree.xpath('//div[@class="pagination"]/ul/li[last()]/a/b/text()')[0]
    )

    urls = [url_base.format(nr) for nr in range(nr_of_the_last_page + 1)]

    # now we can start parse each page and find the scenery
    jobs = [gevent.spawn(find_scenery, url, name) for url in urls]
    gevent.joinall(jobs)


if __name__ == '__main__':
    name = sys.argv[1]
    gather_facts(name)
