#!/usr/bin/env python3
import re 
import json

CHROME_VERSION = 88
FIREFOX_VERSION = 87

def replace_browser_versions(random_header):
    try:
        if (type(random_header) is dict) and 'User-Agent' in random_header:
            random_header['User-Agent'] = re.sub(r"Chrome\/\d+\.", 'Chrome/'+str(CHROME_VERSION)+'.', random_header['User-Agent'], 1, re.MULTILINE)
            random_header['User-Agent'] = re.sub(r"Firefox\/\d+\.", 'Firefox/'+str(FIREFOX_VERSION)+'.', random_header['User-Agent'], 1, re.MULTILINE)

        return random_header
    except Exception as e:
        print(e)
