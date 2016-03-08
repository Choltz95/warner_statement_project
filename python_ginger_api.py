#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib
import urlparse
from urllib2 import HTTPError
from urllib2 import URLError
import json

def get_ginger_url(text):
    """Get URL for checking grammar using Ginger.
    @param text English text
    @return URL
    """
    API_KEY = "6ae0c3a0-afdc-4532-a810-82ded0054236"

    scheme = "http"
    netloc = "services.gingersoftware.com"
    path = "/Ginger/correct/json/GingerTheText"
    params = ""
    query = urllib.urlencode([
        ("lang", "US"),
        ("clientVersion", "2.0"),
        ("apiKey", API_KEY),
        ("text", text)])
    fragment = ""

    return(urlparse.urlunparse((scheme, netloc, path, params, query, fragment)))

def get_ginger_result(text):
    """Get a result of checking grammar.
    @param text English text
    @return result of grammar check by Ginger
    """
    url = get_ginger_url(text)

    try:
        response = urllib.urlopen(url)
    except HTTPError as e:
            print("HTTP Error:", e.code)
            quit()
    except URLError as e:
            print("URL Error:", e.reason)
            quit()
    except IOError, (errno, strerror):
        print("I/O error (%s): %s" % (errno, strerror))
        quit
    try:
        result = json.loads(response.read().decode('utf-8'))
    except ValueError:
        print("Value Error: Invalid server response.")
        quit()
    return(result)

def wrap(text):
    """main function"""
    if len(text) > 600:
        return -1 # no more than 600 characters
    results = get_ginger_result(text)

    # Correct grammar
    if(not results["LightGingerTheTextResult"]):
        return 0
    else:
        return len(results["LightGingerTheTextResult"])
