# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand - XBMC Plugin
# Netflix search
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# ------------------------------------------------------------

import re
import urllib
import urlparse

from core import config
from core import logger
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "netflixsrc"
__category__ = "S"
__type__ = "generic"
__title__ = "netflix search (IT)"
__language__ = "IT"

DEBUG = config.get_setting("debug")

host = "http://www.netflixlovers.it"

TIMEOUT_TOTAL = 60

def isGeneric():
    return True

def mainlist(item):
    logger.info("streamondemand.netflixsrc mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR red]Serie Netflix[/COLOR]",
                     url="%s/classifiche/top-10-serie-tv-le-migliori-serie-tv-su-netflix-italia/" % host,
                     action="serietv",
                     thumbnail="http://www.netflixlovers.it/img/logo-dark.png?v=2"),
                Item(channel=__channel__,
                     title="[COLOR red]Film Netflix[/COLOR]",
                     action="film",
                     url="%s/classifiche/top-10-film-i-migliori-film-su-netflix-italia/" % host,
                     thumbnail="http://www.netflixlovers.it/img/logo-dark.png?v=2"),
                Item(channel=__channel__,
                     title="[COLOR red]Documentari Netflix[/COLOR]",
                     action="film",
                     url="%s/classifiche/top-10-documentari-i-migliori-documentari-su-netflix-italia/" % host,
                     thumbnail="http://www.netflixlovers.it/img/logo-dark.png?v=2")]

    return itemlist

def serietv(item):
    logger.info("streamondemand.netflixsrc serietv")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = '<span class="thumb-info-title">\s*<span class="thumb-info-caption-text">([^<]+)</span>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle in matches:
        scrapedurl = ""
        scrapedthumbnail = ""
        scrapedtv = "Netflix Original"
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedtitle = scrapedtitle.split("(")[0]

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="do_search",
                 extra=urllib.quote_plus(scrapedtitle) + '{}' + 'serie',
                 title=scrapedtitle + "[COLOR red]   " + scrapedtv + "[/COLOR]",
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 folder=True), tipo="tv"))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)" class="btn btn-borders btn-primary mr-xs mb-sm center">Mostra'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="serietv",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 folder=True))

    return itemlist

def film(item):
    logger.info("streamondemand.netflixsrc film")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = '<span class="thumb-info-title">\s*<span class="thumb-info-caption-text">([^<]+)</span>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle in matches:
        scrapedurl = ""
        scrapedthumbnail = ""
        scrapedtv = "Netflix Original"
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        scrapedtitle = scrapedtitle.split("(")[0]

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="do_search",
                 extra=urllib.quote_plus(scrapedtitle) + '{}' + 'movie',
                 title=scrapedtitle + "[COLOR red]   " + scrapedtv + "[/COLOR]",
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 folder=True), tipo="movie"))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)" class="btn btn-borders btn-primary mr-xs mb-sm center">Mostra'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="film",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 folder=True))

    return itemlist

# Esta es la función que realmente realiza la búsqueda

def do_search(item):
    from channels import buscador
    return buscador.do_search(item)

def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand)")

