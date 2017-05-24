# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canale per http://www.subzero.it
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# By MrTruth
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "subzero"
__category__ = "A, T"
__type__ = "generic"
__title__ = "SubZero"
__language__ = "IT"

host = "http://www.subzero.it"

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:51.0) Gecko/20100101 Firefox/51.0'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Referer', host]
]

def isGeneric():
    return True

# ----------------------------------------------------------------------------------------------------------------
def mainlist(item):
    logger.info("[SubZero.py]==> mainlist")
    itemlist = [Item(channel=__channel__,
                     action="torrent",
                     title=color("Lista torrent", "azure"),
                     url="%s/torrent" % host,
                     thumbnail="https://raw.githubusercontent.com/MrTruth0/imgs/master/SOD/Channels/SubZero.png")
                ]

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def torrent (item):
    logger.info("[SubZero.py]==> torrent")
    itemlist = []

    data = scrapertools.cache_page(item.url, headers=headers)
    patron = r'<p><font size=\d+>\s*<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip();
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=color(".torrent ", "darkkhaki") + color(scrapedtitle, "deepskyblue"),
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=item.thumbnail,
                 folder=True), tipo="tv"))

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def findvideos(item):
    logger.info("[SubZero.py]==> findvideos")
    itemlist = []

    data = scrapertools.cache_page(item.url, headers=headers)
    patron = r'<p><a href="([^"]+)">([^<]+)</a></p>'
    blocco = scrapertools.get_match(data, r'<br\s*/>Torrent:</p>(.*?)<hr size=\d+>\s*</table>')
    matches = re.compile(patron, re.DOTALL).findall(blocco)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        itemlist.append(
            Item(channel=__channel__,
                 action="play",
                 server="torrent",
                 title=color(scrapedtitle, "azure"),
                 url=scrapedurl,
                 thumbnail=item.thumbnail,
                 folder=False))

    return itemlist

# ================================================================================================================

# ----------------------------------------------------------------------------------------------------------------
def color(text, color):
    return "[COLOR "+color+"]"+text+"[/COLOR]"

# ================================================================================================================
