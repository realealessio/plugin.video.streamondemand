# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# nikla
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# ------------------------------------------------------------
import re
import urlparse

from core import config
from core import logger
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "nikla"
__category__ = "F"
__type__ = "generic"
__title__ = "nikla (IT)"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "https://www.nikla.net/categoria/youtube-film/lista-film-completi-liberamente-accessibili-su-youtube/"

def isGeneric():
    return True

def mainlist(item):
    logger.info("streamondemand.nikla mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Lista Film Completi su Youtube[/COLOR]",
                     action="peliculas",
                     url=host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png")]

    return itemlist

from itertools import islice

def peliculas(item):
    logger.info("streamondemand.nikla peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = '<li><span style[^>]+>([^<]+)<[^=]+=[^=]+="([^"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl in matches:
        scrapedthumbnail = ""
        scrapedplot = ""
        scrapedtitle = scrapedtitle[2:]
        scrapedtitle = scrapedtitle.title()
        scrapedtitle = scrapedtitle.replace("Film Completo in italiano", "")
        scrapedtitle = scrapedtitle.replace("Film Completo", "")
        #scrapedtitle = scrapedtitle.replace['.', '']

        html = scrapertools.cache_page(scrapedurl)
        patron = '<meta property="og:image" content="([^"]+)"/>'
        matches = re.compile(patron, re.DOTALL).findall(html)

        for img in matches:
            scrapedthumbnail = img

        html = scrapertools.cache_page(scrapedurl)
        patron = '<div data-type="youtube" data-video-id="([^"]+)"></div>'
        matches = re.compile(patron, re.DOTALL).findall(html)

        for url in matches:
            if url is not None:
                   scrapedurl = scrapedurl
            else: continue

            itemlist.append(
                Item(channel=__channel__,
                     action="findvideos",
                     fulltitle=scrapedtitle,
                     show=scrapedtitle,
                     title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                     url=scrapedurl,
                     thumbnail=scrapedthumbnail,
                     plot=scrapedplot,
                     folder=True))

    return itemlist

